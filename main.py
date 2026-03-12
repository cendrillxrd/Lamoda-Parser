import os
from dataclasses import asdict

import pandas as pd

from api_key import ApiKeyManager
from config import FILE_PATH, ORDERS_FILE_NAME
from service.api_service import APIService
from utils.date_helper import get_daily_date_range
from utils.log_helper import log_message
from workers.info_collector import InfoCollector
from workers.info_redactor import InfoRedactor
from dto.order_dto import OrderDTO
from dto.columns_nomenclature_dto import ColumnsNomenclatureDTO
from workers.info_updater import InfoUpdater
from utils.save_helper import save_info, is_csv_empty


def main():
    info_collector = InfoCollector()
    info = info_collector.collect_info()

    info_redactor = InfoRedactor()
    result = info_redactor.redact_info(info)

    save_info(result)
    #
    # file_path = f'{FILE_PATH}{ORDERS_FILE_NAME}.csv'
    # if not is_csv_empty(file_path):
    #     updater = InfoUpdater(file_path)
    #     updater.update_info()
    # else:
    #     log_message('app', f'Обновление данных не произошло', 'INFO')


if __name__ == '__main__':
    main()
