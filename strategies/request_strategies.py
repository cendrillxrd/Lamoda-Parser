import time
from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd

from dto.nomenclature_dto import NomenclatureDTO
from dto.stock_dto import StockDTO, asdict
from dto.order_dto import OrderDTO
from config import TIME_SLEEP_NOMENCLATURES, TIME_SLEEP_STOCK, TIME_SLEEP_ORDER, TIME_SLEEP_ORDER_INFO


class RequestStrategy(ABC):
    @abstractmethod
    def get_info(self, client: 'APIClient', **kwargs) -> list[dict]:
        pass


class ReqNomenclatureStrategy(RequestStrategy):
    endpoint = '/api/v1/nomenclatures'
    url_key = 'live'
    nomenclature_dto = NomenclatureDTO()

    def get_info(self, client: 'APIClient', **kwargs) -> list[dict]:
        result = []
        params = asdict(self.nomenclature_dto)
        print(self.nomenclature_dto.page)
        response = client.make_request(method='GET',
                                       url_key=self.url_key,
                                       params=params,
                                       endpoint=self.endpoint)
        result.extend(response['_embedded']['nomenclatures'])
        pages = response['pages']
        for page in range(self.nomenclature_dto.page + 1, pages + 1):
            time.sleep(TIME_SLEEP_NOMENCLATURES)
            print(page)
            params['page'] = page
            response = client.make_request(method='GET',
                                           url_key=self.url_key,
                                           params=params,
                                           endpoint=self.endpoint)
            result.extend(response['_embedded']['nomenclatures'])
        print(params['page'])
        return result


class ReqOrdersStrategy(RequestStrategy):
    endpoint = '/api/v1/orders'
    url_key = 'live'
    order_dto = OrderDTO()

    def get_info(self, client: 'APIClient', **kwargs) -> list[dict]:
        result = []
        params = asdict(self.order_dto)
        print(self.order_dto.page)
        response = client.make_request(method='GET',
                                       url_key=self.url_key,
                                       params=params,
                                       endpoint=self.endpoint)
        result.extend(response['_embedded']['orders'])

        pages = response['pages']
        print(f'всего {pages}')
        for page in range(self.order_dto.page + 1, pages + 1):
            time.sleep(TIME_SLEEP_ORDER)
            print(page)
            params['page'] = page
            response = client.make_request(method='GET',
                                           url_key=self.url_key,
                                           params=params,
                                           endpoint=self.endpoint)
            result.extend(response['_embedded']['orders'])
        return result


class ReqOrderInfoStrategy(RequestStrategy):
    endpoint = '/api/v1/orders'
    url_key = 'live'

    def get_info(self, client: 'APIClient', **kwargs) -> list[dict]:
        endpoint = f'{self.endpoint}/{kwargs['order_id']}'
        time.sleep(TIME_SLEEP_ORDER_INFO)
        response = client.make_request(method='GET',
                                       url_key=self.url_key,
                                       endpoint=endpoint)

        return response


class ReqStockStrategy(RequestStrategy):
    endpoint = '/api/v1/stock/goods'
    url_key = 'live'
    promo_dto = StockDTO()

    def get_info(self, client: 'APIClient', **kwargs) -> list[dict]:
        result = []
        params = asdict(self.promo_dto)
        print(self.promo_dto.page)
        response = client.make_request(method='GET',
                                       url_key=self.url_key,
                                       params=params,
                                       endpoint=self.endpoint)
        result.extend(response['_embedded']['stockStates'])
        pages = response['pages']
        for page in range(self.promo_dto.page + 1, pages + 1):
            time.sleep(TIME_SLEEP_STOCK)
            print(page)
            params['page'] = page
            response = client.make_request(method='GET',
                                           url_key=self.url_key,
                                           params=params,
                                           endpoint=self.endpoint)
            result.extend(response['_embedded']['stockStates'])
        return result
