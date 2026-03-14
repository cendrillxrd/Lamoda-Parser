import time
from abc import ABC, abstractmethod
from typing import Literal, Optional

import pandas as pd

from config import (TIME_SLEEP_NOMENCLATURES, TIME_SLEEP_ORDER,
                    TIME_SLEEP_ORDER_INFO, TIME_SLEEP_STOCK)
from dto.nomenclature_dto import NomenclatureDTO
from dto.order_dto import OrderDTO
from dto.stock_dto import StockDTO, asdict
from utils.create_id_helper import generate_uuid_id
from utils.log_helper import log_message


class RequestStrategy(ABC):
    @abstractmethod
    def get_info(self, client: 'APIClient', **kwargs) -> list[dict]:
        pass


class ReqOrdersStrategy(RequestStrategy):
    endpoint = '/api/v1/orders'
    url_key = 'live'

    def get_info(self, client: 'APIClient', date_str: str = None, period: Literal['day', 'month'] = None, **kwargs) -> \
            list[dict]:
        log_message('app', 'Запрос заказов', 'INFO')
        result = []
        if date_str is None:
            order_dto = OrderDTO()
        else:
            order_dto = OrderDTO.with_date(date_str, period)
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


class ReqMEDCollectionsFirst(RequestStrategy):
    url_key = "med_collections_1"

    def get_info(self, client: 'Client', **kwargs) -> list[dict]:
        log_message('app', 'Получение первого файла коллекций', 'INFO')
        response = client.make_request(url_key=self.url_key)
        return response


class ReqMEDCollectionsThird(RequestStrategy):
    url_key = "med_collections_3"

    def get_info(self, client: 'Client', **kwargs) -> list[dict]:
        log_message('app', 'Получение третьего файла коллекций', 'INFO')
        response = client.make_request(url_key=self.url_key)
        return response


class ReqMEDCollectionsFourth(RequestStrategy):
    url_key = "med_collections_4"

    def get_info(self, client: 'Client', **kwargs) -> list[dict]:
        log_message('app', 'Получение четвертого файла коллекций', 'INFO')
        response = client.make_request(url_key=self.url_key)
        return response


class ReqFullNomenclatureStrategy(RequestStrategy):
    endpoint = '/jsonrpc/v1/nomenclatures.list'
    method = 'v1.nomenclatures.list'
    url_key = 'b2b'
    nomenclature_dto = NomenclatureDTO()
    nomenclature_dto.method = method

    def get_info(self, client: 'APIClient', **kwargs) -> list[dict]:
        log_message('app', 'Запрос номенклатуры', 'INFO')
        result = []
        payload = asdict(self.nomenclature_dto)
        payload['id'] = generate_uuid_id()
        response = client.make_request(method='POST',
                                       url_key=self.url_key,
                                       payload=payload,
                                       endpoint=self.endpoint)
        result.extend(response['result']['nomenclatures'])
        pages = response['result']['pages']
        payload['id'] = generate_uuid_id()
        log_message('app', f'Всего страниц: {pages}', 'DEBUG')
        log_message('app', f'Загружено страниц: {self.nomenclature_dto.params['page']}', 'DEBUG')

        for page in range(self.nomenclature_dto.params['page'] + 1, pages + 1):
            time.sleep(TIME_SLEEP_NOMENCLATURES)
            payload['params']['page'] = page
            log_message('app', f'Загружено страниц: {page}', 'DEBUG')
            response = client.make_request(method='POST',
                                           url_key=self.url_key,
                                           payload=payload,
                                           endpoint=self.endpoint)
            result.extend(response['result']['nomenclatures'])
        return result


class ReqMEDCollectionsSecond(RequestStrategy):
    url_key = "med_collections_2"

    def get_info(self, client: 'Client', **kwargs) -> list[dict]:
        log_message('app', 'Получение второго файла коллекций', 'INFO')
        response = client.make_request(url_key=self.url_key)
        return response
