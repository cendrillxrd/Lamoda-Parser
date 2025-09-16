import pandas as pd

from workers.api_client import APIClient
from workers.converter import Converter
from strategies.convert_strategies import (ConvNomenclaturesStrategy, ConvStockStrategy,
                                           ConvOrderStrategy, ConvOrderInfoStrategy)
from strategies.request_strategies import (ReqNomenclatureStrategy, ReqStockStrategy,
                                           ReqOrdersStrategy, ReqOrderInfoStrategy)


def with_strategies(wb_strategy_cls, converter_strategy_cls):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            self.api_client.set_strategy(wb_strategy_cls())
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

    @with_strategies(ReqStockStrategy, ConvStockStrategy)
    def get_stocks(self) -> pd.DataFrame:
        stocks = self.api_client.get_data()
        stocks_df = self.converter.convert(stocks)
        return stocks_df

    @with_strategies(ReqOrdersStrategy, ConvOrderStrategy)
    def get_orders(self) -> list:
        orders = self.api_client.get_data()
        orders_list = self.converter.convert(orders)
        return orders_list

    @with_strategies(ReqOrderInfoStrategy, ConvOrderInfoStrategy)
    def get_orders_info(self, order_id: list) -> pd.DataFrame:
        orders_info = []
        print(len(order_id))
        i = 1
        for id in order_id:
            print(i)
            i += 1
            orders_info.append(self.api_client.get_data(order_id=id))
        orders_info_df = self.converter.convert(orders_info)
        return orders_info_df

    def get_orders_info_by_products(self):
        orders_id = self.get_orders()
        orders_info_df = self.get_orders_info(orders_id)
        return orders_info_df
