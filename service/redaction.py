import logging

import pandas as pd

from strategies.correct_strategies import CorrMainTableStrategy, CorrNomenclatureTableStrategy
from strategies.merge_strategies import MergeOrdersStocksStrategy
from workers.corrector import Corrector
from workers.merger import Merger


def with_strategies(merge_strategy_cls: 'CorrectorStrategy' = None,
                    correcter_strategy_cls: 'CorrectorStrategy' = None):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            if merge_strategy_cls is not None:
                self.merger.set_strategy(merge_strategy_cls())
            if correcter_strategy_cls is not None:
                self.corrector.set_strategy(correcter_strategy_cls())
            return method(self, *args, **kwargs)

        return wrapper

    return decorator


class RedactionService:
    def __init__(self):
        self.merger = Merger()
        self.corrector = Corrector()

    @with_strategies(merge_strategy_cls=MergeOrdersStocksStrategy,
                     correcter_strategy_cls=CorrMainTableStrategy)
    def merge_orders_with_stock(self, orders_df: pd.DataFrame, stock_df: pd.DataFrame) -> pd.DataFrame:
        merged_df = self.merger.merge(orders_df, stock_df)
        corrected_df = self.corrector.correct(merged_df)
        return corrected_df

    @with_strategies(correcter_strategy_cls=CorrNomenclatureTableStrategy)
    def correct_nomenclatures(self, nomenclature_df: pd.DataFrame) -> pd.DataFrame:
        nomenclature_corrected = self.corrector.correct(nomenclature_df)
        return nomenclature_corrected
