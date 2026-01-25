import pandas as pd

from dto.info_dto import InfoDTO
from service.redaction import RedactionService
from config import ORDERS_FILE_NAME, NOMENCLATURE_FILE_NAME, NOMENCLATURE_DAY_FILE_NAME
from dto.columns_main_dto import ColumnsMainDTO
from dto.indo_update_dto import InfoUpdateDTO


class InfoRedactor:
    def __init__(self):
        self.red = RedactionService()
        self.columns = ColumnsMainDTO()

    def redact_info(self, info: InfoDTO) -> dict:
        # orders_stocks_by_day = self.red.merge_orders_with_stock(info.orders_day, info.stock)
        nomenclature = self.red.correct_nomenclatures(info.nomenclature, info.orders_month)
        nom_prices = self.red.merge_with_prices(nomenclature, info.prices_nomenclature)
        collections_merged = self.red.merge_collections(info.collection1, info.collection2)
        nomenclature_collections = self.red.merge_with_med_collections(nom_prices, collections_merged)
        return {NOMENCLATURE_FILE_NAME: nomenclature_collections}
        # return {ORDERS_FILE_NAME: orders_stocks_by_day,
        #         NOMENCLATURE_FILE_NAME: nomenclature,
        #         NOMENCLATURE_DAY_FILE_NAME: nomenclature_collections}

    def reduct_update_info(self, main_table: pd.DataFrame, info: InfoUpdateDTO) -> pd.DataFrame:
        columns_to_update = (
            self.columns.updated_at, self.columns.status, self.columns.status_product
        )
        updated_df = self.red.merge_main_and_new_info(main_table, info.orders, columns_to_update)
        return updated_df
