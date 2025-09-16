import logging

import pandas as pd

from strategies.correct_strategies import CorrMainTableStrategy
from strategies.merge_strategies import MergeOrdersStocksStrategy
from workers.corrector import Corrector
from workers.merger import Merger


def with_strategies(merge_strategy_cls: 'CorrectorStrategy',
                    correcter_strategy_cls: 'CorrectorStrategy' = None):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
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

    @with_strategies(MergeOrdersStocksStrategy, CorrMainTableStrategy)
    def merge_orders_with_stock(self, orders_df: pd.DataFrame, stock_df: pd.DataFrame) -> pd.DataFrame:
        merged_df = self.merger.merge(orders_df, stock_df)
        corrected_df = self.corrector.correct(merged_df)
        return corrected_df
    #
    # @with_strategies(MergePricesStrategy, CorrPricesStrategy)
    # def merge_with_med_prices(self, wb_df: pd.DataFrame, med_df: pd.DataFrame) -> pd.DataFrame:
    #     logger.info('Обработка данных по ценам WB и MED')
    #     prices_merged = self.merger.merge(wb_df, med_df)
    #     prices_corrected = self.corrector.correct(prices_merged)
    #     return prices_corrected
