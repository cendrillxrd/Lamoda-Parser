from typing import Literal

import pandas as pd

from utils.log_helper import log_message
from workers.api_client import APIClient, MedClient
from workers.converter import Converter
from strategies.convert_strategies import (ConvNomenclaturesStrategy, ConvStockStrategy,
                                           ConvOrderStrategy, ConvOrderInfoStrategy, ConvMEDCollections,
                                           ConvNomenclaturesPricesStrategy)
from strategies.request_strategies import (ReqNomenclaturePricesStrategy, ReqStockStrategy,
                                           ReqOrdersStrategy, ReqOrderInfoStrategy, ReqMEDCollectionsFirst,
                                           ReqMEDCollectionsSecond, ReqNomenclatureStrategy)


def with_strategies(strategy_cls, converter_strategy_cls):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            self.api_client.set_strategy(strategy_cls())
            self.converter.set_strategy(converter_strategy_cls())
            return method(self, *args, **kwargs)

        return wrapper

    return decorator


class APIService:
    def __init__(self, api_key_manager: 'ApiKeyManager'):
        self.api_client = APIClient(api_key_manager=api_key_manager)
        self.converter = Converter()

    @with_strategies(ReqNomenclatureStrategy, ConvNomenclaturesStrategy)
    def get_nomenclatures(self) -> pd.DataFrame:
        nomenclatures = self.api_client.get_data()
        nomenclatures_df = self.converter.convert(nomenclatures)
        return nomenclatures_df

    @with_strategies(ReqNomenclaturePricesStrategy, ConvNomenclaturesPricesStrategy)
    def get_nomenclatures_prices(self) -> pd.DataFrame:
        nomenclatures = self.api_client.get_data()
        nomenclatures_df = self.converter.convert(nomenclatures)
        return nomenclatures_df

    @with_strategies(ReqStockStrategy, ConvStockStrategy)
    def get_stocks(self) -> pd.DataFrame:
        stocks = self.api_client.get_data()
        stocks_df = self.converter.convert(stocks)
        return stocks_df

    @with_strategies(ReqOrdersStrategy, ConvOrderStrategy)
    def get_orders(self, date_str: str = None, period: Literal['day', 'month'] = None) -> list:
        orders = self.api_client.get_data(date_str=date_str, period=period)
        orders_list = self.converter.convert(orders)
        return orders_list

    @with_strategies(ReqOrderInfoStrategy, ConvOrderInfoStrategy)
    def get_orders_info(self, order_ids: list) -> pd.DataFrame:
        orders_info = []
        log_message('app', f'Всего заказов {len(order_ids)}', 'INFO')
        i = 1
        for id in order_ids:
            log_message('app', f'{i}', 'INFO')
            i += 1
            orders_info.append(self.api_client.get_data(order_id=id))
        orders_info_df = self.converter.convert(orders_info)
        return orders_info_df

    def get_orders_info_by_products(self, date_str: str = None, period: Literal['day', 'month'] = None) -> pd.DataFrame:
        orders_id = self.get_orders(date_str=date_str, period=period)
        orders_info_df = self.get_orders_info(orders_id)
        return orders_info_df


def with_strategies_med(req_strategy_cls=None, converter_strategy_cls=None):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            if req_strategy_cls is not None:
                self.med_api_client.set_strategy(req_strategy_cls())
            if converter_strategy_cls is not None:
                self.converter.set_strategy(converter_strategy_cls())
            return method(self, *args, **kwargs)

        return wrapper

    return decorator


class MedService:
    def __init__(self):
        self.med_api_client = MedClient()
        self.converter = Converter()

    @with_strategies_med(req_strategy_cls=ReqMEDCollectionsFirst, converter_strategy_cls=ConvMEDCollections)
    def get_med_collections_first(self) -> pd.DataFrame:
        med_collections_csv = self.med_api_client.get_data()
        med_collections_df = self.converter.convert(med_collections_csv)
        return med_collections_df

    @with_strategies_med(req_strategy_cls=ReqMEDCollectionsSecond, converter_strategy_cls=ConvMEDCollections)
    def get_med_collections_second(self) -> pd.DataFrame:
        med_collections_csv = self.med_api_client.get_data()
        med_collections_df = self.converter.convert(med_collections_csv)
        return med_collections_df
