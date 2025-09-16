from api_client import APIClient
from converter import Converter
from strategies.convert_strategies import ConvNomenclaturesStrategy, ConvStockStrategy, ConvOrderStrategy
from strategies.request_strategies import ReqNomenclatureStrategy, ReqStockStrategy, ReqOrdersStrategy


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
    def get_nomenclatures(self) -> list:
        nomenclatures = self.api_client.get_data()
        nomenclatures_df = self.converter.convert(nomenclatures)
        return nomenclatures_df

    @with_strategies(ReqStockStrategy, ConvStockStrategy)
    def get_stocks(self) -> list:
        stocks = self.api_client.get_data()
        stocks_df = self.converter.convert(stocks)
        return stocks_df

    @with_strategies(ReqOrdersStrategy, ConvOrderStrategy)
    def get_orders(self) -> list:
        orders = self.api_client.get_data()
        orders_df = self.converter.convert(orders)
        return orders_df
