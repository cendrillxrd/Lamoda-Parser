"""
Одноразовая миграция старых CSV-файлов Lamoda (заказы / номенклатура) в MySQL.

Запускать из корня проекта, например:

    python scripts/migrate_csv_to_db.py --orders "C:/Users/user/Desktop/LAMODA DATA/Заказы.csv"
    python scripts/migrate_csv_to_db.py --nomenclature "C:/Users/user/Desktop/LAMODA DATA/Номенклатура.csv"

Перед запуском таблицы должны быть созданы (python db/create_tables.py),
.env с настройками MySQL должен быть заполнен.

Для заказов миграция сама посчитает 'position' — порядковый номер повторения
(Номер заказа, Артикул товара) внутри файла, той же логикой, что и при обычном
сохранении (см. LamodaOrdersRepository.upsert_dataframe).

Скрипт:
- читает CSV в кодировке cp1251;
- приводит дату (для номенклатуры) к единому формату 'YYYY-MM-DD';
- отбрасывает колонки, которых нет в текущей схеме DTO;
- заливает данные в БД через upsert (повторный запуск безопасен).
"""
import argparse
import sys
from dataclasses import asdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dto.columns_main_dto import ColumnsMainDTO
from dto.columns_nomenclature_dto import ColumnsNomenclatureDTO
from repositories.lamoda_nomenclature_repository import LamodaNomenclatureRepository
from repositories.lamoda_orders_repository import LamodaOrdersRepository
from utils.log_helper import log_message

CSV_ENCODING = 'cp1251'
DEFAULT_CHUNK_SIZE = 2000

# Если в старых CSV встретятся заголовки, отличающиеся от текущих значений в DTO
# (например, из-за переименований в коде), добавляй сюда алиасы.
LEGACY_COLUMN_ALIASES: dict[str, str] = {}


def _load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding=CSV_ENCODING)
    log_message('app', f'Загружено {len(df)} строк из {path}', 'INFO')
    return df


def _apply_legacy_aliases(df: pd.DataFrame) -> pd.DataFrame:
    found_aliases = {old: new for old, new in LEGACY_COLUMN_ALIASES.items() if old in df.columns}
    if found_aliases:
        log_message('app', f'Найдены устаревшие названия колонок, переименовываю: {found_aliases}', 'INFO')
        df = df.rename(columns=found_aliases)
    return df


def _drop_unknown_columns(df: pd.DataFrame, known_headers: list[str]) -> pd.DataFrame:
    unknown = [col for col in df.columns if col not in known_headers]
    if unknown:
        log_message('app', f'Колонки не из текущей схемы будут проигнорированы: {unknown}', 'WARNING')
        df = df.drop(columns=unknown)
    return df


def _normalize_date(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    parsed = pd.to_datetime(df[date_column], errors='coerce')
    invalid_count = int(parsed.isna().sum())
    if invalid_count:
        log_message('app', f'Не удалось распознать дату в {invalid_count} строках, они будут пропущены', 'WARNING')
        df = df[parsed.notna()].copy()
        parsed = parsed[parsed.notna()]
    df[date_column] = parsed.dt.strftime('%Y-%m-%d')
    return df


def migrate_orders(csv_path: str, chunk_size: int = DEFAULT_CHUNK_SIZE) -> None:
    columns = asdict(ColumnsMainDTO())
    df = _load_csv(csv_path)
    df = _apply_legacy_aliases(df)
    df = _drop_unknown_columns(df, list(columns.values()))

    repo = LamodaOrdersRepository()
    total = len(df)
    if total == 0:
        log_message('app', 'lamoda_orders: после очистки не осталось строк для миграции', 'WARNING')
        return

    for start in range(0, total, chunk_size):
        chunk = df.iloc[start:start + chunk_size]
        repo.upsert_dataframe(chunk)
        log_message('app', f'lamoda_orders: мигрировано {min(start + chunk_size, total)}/{total} строк', 'INFO')
    log_message('app', 'lamoda_orders: миграция завершена', 'INFO')


def migrate_nomenclature(csv_path: str, chunk_size: int = DEFAULT_CHUNK_SIZE) -> None:
    columns = asdict(ColumnsNomenclatureDTO())
    df = _load_csv(csv_path)
    df = _apply_legacy_aliases(df)
    df = _drop_unknown_columns(df, list(columns.values()))
    df = _normalize_date(df, columns['date'])

    repo = LamodaNomenclatureRepository()
    total = len(df)
    if total == 0:
        log_message('app', 'lamoda_nomenclature: после очистки не осталось строк для миграции', 'WARNING')
        return

    for start in range(0, total, chunk_size):
        chunk = df.iloc[start:start + chunk_size]
        repo.upsert_dataframe(chunk)
        log_message('app', f'lamoda_nomenclature: мигрировано {min(start + chunk_size, total)}/{total} строк', 'INFO')
    log_message('app', 'lamoda_nomenclature: миграция завершена', 'INFO')


def main() -> None:
    parser = argparse.ArgumentParser(description='Миграция старых CSV Lamoda (заказы/номенклатура) в MySQL')
    parser.add_argument('--orders', help='Путь к CSV с заказами', default=None)
    parser.add_argument('--nomenclature', help='Путь к CSV с номенклатурой', default=None)
    parser.add_argument('--chunk-size', type=int, default=DEFAULT_CHUNK_SIZE)
    args = parser.parse_args()

    if not args.orders and not args.nomenclature:
        parser.error('Нужно указать хотя бы один из параметров: --orders или --nomenclature')

    if args.orders:
        path = Path(args.orders)
        if not path.exists():
            parser.error(f'Файл не найден: {args.orders}')
        migrate_orders(str(path), args.chunk_size)

    if args.nomenclature:
        path = Path(args.nomenclature)
        if not path.exists():
            parser.error(f'Файл не найден: {args.nomenclature}')
        migrate_nomenclature(str(path), args.chunk_size)


if __name__ == '__main__':
    main()
