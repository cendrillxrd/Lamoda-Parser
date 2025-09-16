import os

import pandas as pd

from api_key import ApiKeyManager
from service.api_service import APIService
from utils.date_helper import get_daily_date_range
from workers.info_collector import InfoCollector
from workers.info_redactor import InfoRedactor


def main():
    info_collector = InfoCollector()
    info = info_collector.collect_info()
    info_redactor = InfoRedactor()
    result = info_redactor.redact_info(info)
    pd.DataFrame(result).to_csv('final.csv', index=False, encoding='cp1251')


if __name__ == '__main__':
    main()
