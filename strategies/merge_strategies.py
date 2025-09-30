from abc import ABC, abstractmethod

import pandas as pd

from dto.columns_main_dto import ColumnsMainDTO
from dto.columns_nomenclature_dto import ColumnsNomenclatureDTO
from config import ON_THE_WAY_SHIP_STATUS, ON_THE_WAY_GOODS_SHIPS_STATUS

columns_main = ColumnsMainDTO()
columns_nomenclature = ColumnsNomenclatureDTO()


class MergeStrategies(ABC):
    @abstractmethod
    def merge(self, *args) -> pd.DataFrame:
        pass


class MergeOrdersStocksStrategy(MergeStrategies):
    def __init__(self, merge_on: str = columns_main.sku):
        self.merge_on = merge_on

    def merge(self, orders: pd.DataFrame, stock: pd.DataFrame) -> pd.DataFrame:
        merged_df = pd.merge(orders, stock, on=self.merge_on, how='left')
        return merged_df


class MergeNewInfoStrategy(MergeStrategies):
    def __init__(self, merge_on: tuple[str] = (columns_main.id, columns_main.sku, columns_main.created_at)):
        self.merge_on = merge_on

    def merge(self, previous_table: pd.DataFrame, new_info: pd.DataFrame, columns_to_update: tuple) -> pd.DataFrame:
        merged_df = pd.merge(
            previous_table, new_info[list(self.merge_on + columns_to_update)],
            on=self.merge_on,
            how='left',
            suffixes=('', '_new')
        )
        return merged_df


class MergeByShipStrategy(MergeStrategies):
    def __init__(self, merge_on: str = columns_main.sku):
        self.merge_on = merge_on

    def merge(self, nomenclature: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
        filtered_df = orders[(orders[columns_main.status].isin(ON_THE_WAY_SHIP_STATUS))
                             & (orders[columns_main.status_product].isin(ON_THE_WAY_GOODS_SHIPS_STATUS))].copy()
        article_counts = filtered_df[columns_main.sku].value_counts().reset_index().copy()
        merged_df = pd.merge(nomenclature, article_counts, on=self.merge_on, how='left')
        merged_df.rename({'count': columns_nomenclature.on_the_way}, inplace=True, axis=1)

        return merged_df
