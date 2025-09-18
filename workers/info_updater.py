import pandas as pd

from dto.info_dto import InfoDTO
from service.api_service import APIService
from api_key import ApiKeyManager
from workers.info_collector import InfoCollector
from workers.info_redactor import InfoRedactor
from config import FILE_PATH, ORDERS_FILE_NAME
from dto.columns_main_dto import ColumnsMainDTO
from dto.indo_update_dto import InfoUpdateDTO


class InfoUpdater:
    def __init__(self, file_path):
        self.info_collector = InfoCollector()
        self.info_reductor = InfoRedactor()
        self.file_path = file_path
        self.previous_table = pd.read_csv(self.file_path, encoding='cp1251')
        self.columns = ColumnsMainDTO()

    def update_info(self):
        dates = self.get_last_two_week_dates()
        for date in dates:
            info = self.info_collector.collect_info_for_update(date_str=date)
            updated_info = self.info_reductor.reduct_update_info(self.previous_table, info)
            self.previous_table = updated_info
        self.previous_table.to_csv(self.file_path, index=False, encoding='cp1251')

    def get_last_two_week_dates(self) -> list[str]:
        """Возвращает последние 14 дат из таблицы. Если дат меньше, вернет все, что есть."""
        dates = self.previous_table[self.columns.created_at].unique()
        sorted_dates = pd.to_datetime(dates).sort_values(ascending=False)
        sorted_str_dates = [str(date.date()) for date in sorted_dates]
        return sorted_str_dates[1:14]
