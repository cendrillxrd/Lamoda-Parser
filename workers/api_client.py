import time
from typing import Dict, Literal, Optional

import requests
import urllib3

from config import BASE_URLS, CLIENT_ID, CLIENT_SECRET
from strategies.request_strategies import RequestStrategy


class APIClient:
    def __init__(self, api_key_manager: "ApiKeyManager" = None):
        self.base_url = BASE_URLS
        self.api_key_manager = api_key_manager
        if api_key_manager is not None:
            self.api_key = api_key_manager.get_key()
        else:
            self.api_key = None
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        self.__strategy = None

    def set_strategy(self, strategy: RequestStrategy):
        self.__strategy = strategy

    def _update_auth_header(self):
        """Обновляет заголовок Authorization с текущим API ключом"""
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
        else:
            # Удаляем заголовок, если ключа нет
            self.session.headers.pop('Authorization', None)

    def make_request(
            self,
            url_key: Literal['live', 'b2b'],
            method: Literal['GET', 'POST'],
            endpoint: str,
            params: Optional[Dict] = None,
            payload: Optional[Dict] = None,
            retries: int = 5):
        url = f'{self.base_url[url_key]}{endpoint}'
        for attempt in range(retries):
            self._update_auth_header()
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=payload,
                timeout=(10, 60)
            )
            try:
                response.raise_for_status()
                if self.session.headers['Content-Type'] == 'application/zip':
                    return response
                response_json = response.json()
                if response_json.get('error'):
                    self.api_key_manager.force_renew()
                    self.api_key = self.api_key_manager.get_key()
                    self._update_auth_header()
                    time.sleep(10)
                    continue
                return response_json

            except requests.exceptions.HTTPError as err:
                print(response.json())
                if err.response.status_code == 401:
                    self.api_key_manager.force_renew()
                    self.api_key = self.api_key_manager.get_key()
                    self._update_auth_header()
                    time.sleep(10)
                    continue
                if err.response.status_code in (429, 500, 502, 503, 504, 443):
                    print('Retrying...')
                    wait_time = min(2 ** attempt, 10)
                    time.sleep(wait_time)
                    continue
                raise err

            except (requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectTimeout,
                    requests.exceptions.ConnectionError,
                    requests.exceptions.SSLError,) as err:
                print(response.json())
                time.sleep(10)
                continue

            except requests.exceptions.RequestException as err:
                if attempt == retries - 1:
                    raise err
                time.sleep(1)

            except urllib3.exceptions.ProtocolError as e:

                print(f"Ошибка соединения (попытка {attempt + 1}/{retries}): {e}")

                if attempt < retries - 1:
                    # Экспоненциальная задержка
                    wait_time = 2 ** attempt
                    print(f"Повтор через {wait_time} секунд...")
                    time.sleep(wait_time)
                else:
                    print("Превышено количество попыток")
                    raise

        return None

    def get_data(self, **kwargs) -> list[dict]:
        if self.__strategy is None:
            raise ValueError('Стратегия не выбрана, установите стратегию с помощью set_strategy')
        return self.__strategy.get_info(self, **kwargs)

    def get_new_api_key(self):
        endpoint = '/auth/token'
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'client_credentials',
        }
        response = self.make_request(method='GET',
                                     url_key='live',
                                     params=params,
                                     endpoint=endpoint)
        return response['access_token']


class MedClient:
    def __init__(self):
        self.base_url = BASE_URLS
        self.__strategy = None

    def make_request(self, url_key: Literal['med_collections_1', 'med_collections_2'], login: str = None,
                     password: str = None, ):
        url = f'{self.base_url[url_key]}'
        response = requests.get(url, auth=(login, password))
        return response

    def set_strategy(self, strategy: RequestStrategy):
        self.__strategy = strategy

    def get_data(self, **kwargs) -> list[dict]:
        if self.__strategy is None:
            raise ValueError('Стратегия не выбрана, установите стратегию с помощью set_strategy')
        return self.__strategy.get_info(self, **kwargs)
