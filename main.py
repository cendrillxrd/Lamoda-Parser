import os

import pandas as pd

from api_key import ApiKeyManager
from service.api_service import APIService


def main():
    api = ApiKeyManager()
    # api.force_renew()
    service = APIService(api)
    result = service.get_orders()
    pd.DataFrame(result).to_csv('orders.csv', index=False, encoding='cp1251')


if __name__ == '__main__':
    main()
