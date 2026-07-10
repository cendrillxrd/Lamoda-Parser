from dataclasses import asdict

import pandas as pd

from db.models import LamodaOrdersModel
from dto.columns_main_dto import ColumnsMainDTO
from repositories.base_repository import BaseRepository

_main_columns = asdict(ColumnsMainDTO())


class LamodaOrdersRepository(BaseRepository):
    model = LamodaOrdersModel
    unique_columns = ('id', 'sku', 'position')
    column_mapping = {russian: english for english, russian in _main_columns.items()}

    def upsert_dataframe(self, df: pd.DataFrame, chunk_size: int = 500) -> None:
        """
        Внутри одного заказа товар может встречаться несколько раз как отдельные позиции —
        (Номер заказа, Артикул товара) сам по себе не уникален. 'position' — порядковый
        номер повторения такой пары внутри батча (аналог решения из order_collector).
        Стабильность позиции опирается на то, что Lamoda возвращает позиции заказа в
        одном и том же порядке при каждом запросе.
        """
        if df is not None and not df.empty:
            df = df.copy()
            df['position'] = df.groupby([_main_columns['id'], _main_columns['sku']]).cumcount()
        super().upsert_dataframe(df, chunk_size=chunk_size)
