import pandas as pd

from dto.info_dto import InfoDTO
from service.redaction import RedactionService
from config import ORDERS_FILE_NAME, NOMENCLATURE_FILE_NAME
from dto.columns_main_dto import ColumnsMainDTO
from dto.indo_update_dto import InfoUpdateDTO


class InfoRedactor:
    def __init__(self):
        self.red = RedactionService()
        self.columns = ColumnsMainDTO()

    def redact_info(self, info: InfoDTO) -> dict:
        orders_stocks_by_day = self.red.merge_orders_with_stock(info.orders_day, info.stock)
        nomenclature = self.red.correct_nomenclatures(info.nomenclature, info.orders_month)

        return {ORDERS_FILE_NAME: orders_stocks_by_day, NOMENCLATURE_FILE_NAME: nomenclature}

    def reduct_update_info(self, main_table: pd.DataFrame, info: InfoUpdateDTO) -> pd.DataFrame:
        columns_to_update = (
            self.columns.updated_at, self.columns.status, self.columns.status_product
        )
        updated_df = self.red.merge_main_and_new_info(main_table, info.orders, columns_to_update)
        return updated_df
