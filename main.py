import os

import pandas as pd

from api_key import ApiKeyManager
from service.api_service import APIService
from utils.date_helper import get_daily_date_range


def main():
    api = ApiKeyManager()
    # api.force_renew()
    service = APIService(api)
    orders_id = service.get_orders()
    result = service.get_orders_info(orders_id)
    pd.DataFrame(result).to_csv('orders.csv', index=False, encoding='cp1251')
    # print(result)


if __name__ == '__main__':
    main()
