import time
from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd

from dto.nomenclature_dto import NomenclatureDTO
from dto.stock_dto import StockDTO, asdict
from dto.order_dto import OrderDTO
from config import TIME_SLEEP_NOMENCLATURES, TIME_SLEEP_STOCK, TIME_SLEEP_ORDER, TIME_SLEEP_ORDER_INFO
from utils.log_helper import log_message


class RequestStrategy(ABC):
    @abstractmethod
    def get_info(self, client: 'APIClient', **kwargs) -> list[dict]:
        pass


class ReqNomenclatureStrategy(RequestStrategy):
    endpoint = '/api/v1/nomenclatures'
    url_key = 'live'
    nomenclature_dto = NomenclatureDTO()

    def get_info(self, client: 'APIClient', **kwargs) -> list[dict]:
        log_message('app', 'Запрос номенклатуры', 'INFO')
        result = []
        params = asdict(self.nomenclature_dto)
        response = client.make_request(method='GET',
                                       url_key=self.url_key,
                                       params=params,
                                       endpoint=self.endpoint)
        result.extend(response['_embedded']['nomenclatures'])
        pages = response['pages']
        log_message('app', f'Всего страниц: {pages}', 'DEBUG')
        log_message('app', f'Загружено страниц: {self.nomenclature_dto.page}', 'DEBUG')

        for page in range(self.nomenclature_dto.page + 1, pages + 1):
            time.sleep(TIME_SLEEP_NOMENCLATURES)
            params['page'] = page
            log_message('app', f'Загружено страниц: {page}', 'DEBUG')
            response = client.make_request(method='GET',
                                           url_key=self.url_key,
                                           params=params,
                                           endpoint=self.endpoint)
            result.extend(response['_embedded']['nomenclatures'])
        return result


class ReqOrdersStrategy(RequestStrategy):
    endpoint = '/api/v1/orders'
    url_key = 'live'

    def get_info(self, client: 'APIClient', date_str: str = None, **kwargs) -> list[dict]:
        log_message('app', 'Запрос заказов', 'INFO')
        result = []
        if date_str is None:
            order_dto = OrderDTO()
        else:
            order_dto = OrderDTO.with_date(date_str)
        params = asdict(order_dto)
        response = client.make_request(method='GET',
                                       url_key=self.url_key,
                                       params=params,
                                       endpoint=self.endpoint)
        result.extend(response['_embedded']['orders'])
        pages = response['pages']
        log_message('app', f'Всего страниц: {pages}', 'DEBUG')
        log_message('app', f'Загружено страниц: {order_dto.page}', 'DEBUG')

        for page in range(order_dto.page + 1, pages + 1):
            time.sleep(TIME_SLEEP_ORDER)
            log_message('app', f'Загружено страниц: {page}', 'DEBUG')
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
        log_message('app', f'Запрос подробной информации о заказе {kwargs['order_id']}', 'INFO')
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
        log_message('app', 'Запрос остатков', 'INFO')
        result = []
        params = asdict(self.promo_dto)
        print(self.promo_dto.page)
        response = client.make_request(method='GET',
                                       url_key=self.url_key,
                                       params=params,
                                       endpoint=self.endpoint)
        result.extend(response['_embedded']['stockStates'])
        pages = response['pages']

        log_message('app', f'Всего страниц: {pages}', 'DEBUG')
        log_message('app', f'Загружено страниц: {self.promo_dto.page}', 'DEBUG')
        for page in range(self.promo_dto.page + 1, pages + 1):
            time.sleep(TIME_SLEEP_STOCK)
            params['page'] = page
            log_message('app', f'Загружено страниц: {page}', 'DEBUG')
            response = client.make_request(method='GET',
                                           url_key=self.url_key,
                                           params=params,
                                           endpoint=self.endpoint)
            result.extend(response['_embedded']['stockStates'])
        return result
