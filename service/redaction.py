import logging

import pandas as pd

from strategies.correct_strategies import CorrMainTableStrategy, CorrNomenclatureTableStrategy, \
    CorrNewInfoTableStrategy, CorrCollections, CorrPrices
from strategies.merge_strategies import MergeOrdersStocksStrategy, MergeNewInfoStrategy, MergeByShipStrategy, \
    MergeLamodaCollections, MergeCollections, MergeWithPricesStrategy
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

    @with_strategies(merge_strategy_cls=MergeByShipStrategy,
                     correcter_strategy_cls=CorrNomenclatureTableStrategy)
    def correct_nomenclatures(self, nomenclature_df: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
        merged_df = self.merger.merge(nomenclature_df, orders)
        nomenclature_corrected = self.corrector.correct(merged_df)
        return nomenclature_corrected

    @with_strategies(merge_strategy_cls=MergeNewInfoStrategy,
                     correcter_strategy_cls=CorrNewInfoTableStrategy)
    def merge_main_and_new_info(self, main_tabel: pd.DataFrame, new_info: pd.DataFrame,
                                columns_to_update: tuple) -> pd.DataFrame:
        merged_df = self.merger.merge(main_tabel, new_info, columns_to_update)
        corrected_df = self.corrector.correct(merged_df)
        return corrected_df

    @with_strategies(merge_strategy_cls=MergeWithPricesStrategy, correcter_strategy_cls=CorrPrices)
    def merge_with_prices(self, nomenclature: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
        prices_merged = self.merger.merge(nomenclature, prices)
        prices_corrected = self.corrector.correct(prices_merged)
        return prices_corrected

    @with_strategies(merge_strategy_cls=MergeLamodaCollections, correcter_strategy_cls=CorrCollections)
    def merge_with_med_collections(self, lamoda_df: pd.DataFrame, med_df: pd.DataFrame) -> pd.DataFrame:
        collections_merged = self.merger.merge(lamoda_df, med_df)
        collections_corrected = self.corrector.correct(collections_merged)
        return collections_corrected

    @with_strategies(merge_strategy_cls=MergeCollections)
    def merge_collections(self, col1_df: pd.DataFrame, col2_df: pd.DataFrame) -> pd.DataFrame:
        collections_merged = self.merger.merge(col1_df, col2_df)
        return collections_merged
