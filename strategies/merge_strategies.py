from abc import ABC, abstractmethod

import pandas as pd

from dto.columns_main_dto import ColumnsMainDTO

columns = ColumnsMainDTO()


class MergeStrategies(ABC):
    @abstractmethod
    def merge(self, *args) -> pd.DataFrame:
        pass


class MergeOrdersStocksStrategy(MergeStrategies):
    def __init__(self, merge_on: str = columns.sku):
        self.merge_on = merge_on

    def merge(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        merged_df = pd.merge(df1, df2, on=self.merge_on, how='left')
        return merged_df


class MergeNewInfoStrategy(MergeStrategies):
    def __init__(self, merge_on: tuple[str] = (columns.id, columns.sku, columns.created_at)):
        self.merge_on = merge_on

    def merge(self, df1: pd.DataFrame, df2: pd.DataFrame, columns_to_update: tuple) -> pd.DataFrame:
        merged_df = pd.merge(
            df1, df2[list(self.merge_on + columns_to_update)],
            on=self.merge_on,
            how='left',
            suffixes=('', '_new')
        )
        return merged_df
