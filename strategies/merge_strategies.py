from abc import ABC, abstractmethod

import pandas as pd


class MergeStrategies(ABC):
    @abstractmethod
    def merge(self, *args) -> pd.DataFrame:
        pass


class MergeOrdersStocksStrategy(MergeStrategies):
    def __init__(self, merge_on: str = 'Артикул товара'):
        self.merge_on = merge_on

    def merge(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        merged_df = pd.merge(df1, df2, on=self.merge_on, how='left')
        return merged_df
