import json
from typing import Dict, Sequence, Type

import pandas as pd
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.orm import DeclarativeMeta

from db.session import SessionLocal
from utils.log_helper import log_message


class BaseRepository:
    """
    Общая логика upsert'а pandas.DataFrame в MySQL и чтения таблицы обратно в DataFrame.

    column_mapping: {'Русское название колонки в DataFrame': 'english_column_in_db'}
    unique_columns: колонки, по которым определяется конфликт при upsert (не обновляются).
    """

    model: Type[DeclarativeMeta] = None
    unique_columns: Sequence[str] = ()
    column_mapping: Dict[str, str] = {}

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def _pk_columns(self) -> set:
        """
        Имя PK-колонки определяем динамически (а не хардкодим 'id'), потому что в
        некоторых таблицах (например, заказы Lamoda) бизнес-колонка сама называется 'id',
        и surrogate PK там называется иначе (record_id).
        """
        return {c.name for c in self.model.__table__.primary_key.columns}

    def _to_db_records(self, df: pd.DataFrame) -> list[dict]:
        renamed = df.rename(columns=self.column_mapping)
        pk_columns = self._pk_columns()
        db_columns = [c.name for c in self.model.__table__.columns if c.name not in pk_columns]
        existing_columns = [c for c in db_columns if c in renamed.columns]
        renamed = renamed[existing_columns].copy()

        # Некоторые колонки (например, created_at после pd.to_datetime в корректорах)
        # могут содержать pd.Timestamp вместо строк — приводим к ISO-строке, иначе
        # вставка в текстовую колонку может упасть на несовместимости типов.
        for col in renamed.columns:
            if renamed[col].apply(lambda v: isinstance(v, pd.Timestamp)).any():
                renamed[col] = renamed[col].apply(lambda v: v.isoformat() if pd.notna(v) else None)

        # Дата может прийти в разных форматах — приводим к единому '%Y-%m-%d', иначе
        # MySQL роняет вставку с ошибкой "Incorrect date value". Сначала пробуем строгий
        # ISO-формат: dayfirst=True на скаляре может сломать и уже корректную '2026-07-06',
        # приняв её за day-first и переставив месяц/день (реальный баг pandas/dateutil).
        if 'date' in renamed.columns:
            def _parse_date(value):
                if pd.isna(value):
                    return None
                parsed = pd.to_datetime(value, format='%Y-%m-%d', errors='coerce')
                if pd.isna(parsed):
                    parsed = pd.to_datetime(value, dayfirst=True, errors='coerce')
                return parsed

            parsed_dates = renamed['date'].apply(_parse_date)
            invalid_mask = parsed_dates.isna() & renamed['date'].notna()
            if invalid_mask.any():
                log_message(
                    'app',
                    f'Не удалось распознать дату в {int(invalid_mask.sum())} строках при сохранении в '
                    f'{self.model.__tablename__}: {renamed.loc[invalid_mask, "date"].unique().tolist()}',
                    'WARNING',
                )
            renamed['date'] = parsed_dates.apply(lambda d: d.strftime('%Y-%m-%d') if pd.notna(d) else None)

        # Некоторые колонки (например, списки после агрегации) содержат списки/словари —
        # сериализуем их в JSON для текстовой колонки.
        for col in renamed.columns:
            if renamed[col].apply(lambda v: isinstance(v, (list, dict))).any():
                renamed[col] = renamed[col].apply(
                    lambda v: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v
                )

        records = renamed.to_dict(orient='records')

        # df.where(df.notnull(), None) не годится: на float/int-колонках None тут же
        # обратно превращается в NaN (numpy-массив просто не может хранить None), и
        # NaN благополучно долетает до MySQL, где ломается с ошибкой "nan can not be used".
        # Поэтому чистим уже после to_dict, на уровне обычных python-объектов.
        for record in records:
            for key, value in record.items():
                if isinstance(value, (list, dict)):
                    continue
                try:
                    if pd.isna(value):
                        record[key] = None
                except (TypeError, ValueError):
                    pass

        return records

    def upsert_dataframe(self, df: pd.DataFrame, chunk_size: int = 500) -> None:
        """Вставляет новые строки и обновляет существующие (по unique_columns)."""
        if df is None or df.empty:
            log_message('app', f'Пустой DataFrame, upsert в {self.model.__tablename__} пропущен', 'WARNING')
            return

        records = self._to_db_records(df)
        if not records:
            log_message('app', f'Нет колонок для сохранения в {self.model.__tablename__}', 'WARNING')
            return

        pk_columns = self._pk_columns()
        update_columns = [
            c.name for c in self.model.__table__.columns
            if c.name not in pk_columns and c.name not in self.unique_columns
        ]

        with self.session_factory() as session:
            for i in range(0, len(records), chunk_size):
                chunk = records[i:i + chunk_size]
                stmt = mysql_insert(self.model).values(chunk)
                update_dict = {col: getattr(stmt.inserted, col) for col in update_columns if col in chunk[0]}
                if update_dict:
                    stmt = stmt.on_duplicate_key_update(**update_dict)
                else:
                    stmt = stmt.prefix_with('IGNORE')
                session.execute(stmt)
            session.commit()
        log_message('app', f'Сохранено {len(records)} строк в таблицу {self.model.__tablename__}', 'INFO')

    def _rows_to_dataframe(self, rows) -> pd.DataFrame:
        pk_columns = self._pk_columns()
        columns = [c.name for c in self.model.__table__.columns if c.name not in pk_columns]
        data = [{col: getattr(row, col) for col in columns} for row in rows]
        df = pd.DataFrame(data, columns=columns)

        if 'date' in df.columns:
            df['date'] = df['date'].astype(str)

        inverse_mapping = {english: russian for russian, english in self.column_mapping.items()}
        df.rename(columns=inverse_mapping, inplace=True)
        return df

    def fetch_all_as_dataframe(self) -> pd.DataFrame:
        """Читает всю таблицу и возвращает DataFrame с русскими названиями колонок (как раньше в CSV)."""
        with self.session_factory() as session:
            rows = session.query(self.model).all()
        return self._rows_to_dataframe(rows)

    def fetch_since_as_dataframe(self, since) -> pd.DataFrame:
        """Читает только строки с date >= since — чтобы не тащить в память всю таблицу."""
        with self.session_factory() as session:
            rows = session.query(self.model).filter(self.model.date >= since).all()
        return self._rows_to_dataframe(rows)

    def is_empty(self) -> bool:
        with self.session_factory() as session:
            return session.query(self.model).first() is None
