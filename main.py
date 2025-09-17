import os
from dataclasses import asdict

import pandas as pd

from api_key import ApiKeyManager
from service.api_service import APIService
from utils.date_helper import get_daily_date_range
from workers.info_collector import InfoCollector
from workers.info_redactor import InfoRedactor
from dto.columns_nomenclature_dto import ColumnsNomenclatureDTO


def main():
    info_collector = InfoCollector()
    info = info_collector.collect_info()
    info_redactor = InfoRedactor()
    result = info_redactor.redact_info(info)
    result['orders_stocks'].to_csv('final.csv', index=False, encoding='cp1251')
    result['nomenclature'].to_csv('nomenclature_final.csv', index=False, encoding='cp1251')


if __name__ == '__main__':
    main()
