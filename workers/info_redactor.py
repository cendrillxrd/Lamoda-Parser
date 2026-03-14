from config import (NOMENCLATURE_DAY_FILE_NAME, NOMENCLATURE_FILE_NAME,
                    ORDERS_FILE_NAME)
from dto.columns_main_dto import ColumnsMainDTO
from dto.info_dto import InfoDTO
from service.redaction import RedactionService


class InfoRedactor:
    def __init__(self):
        self.red = RedactionService()
        self.columns = ColumnsMainDTO()

    def redact_info(self, info: InfoDTO) -> dict:
        collections_merged_1_2 = self.red.merge_collections(info.collection1, info.collection2)
        collections_merged_1_2_3 = self.red.merge_collections(collections_merged_1_2, info.collection3)
        collections_merged_1_2_3_4 = self.red.merge_collections(collections_merged_1_2_3, info.collection4)

        nomenclature = self.red.correct_nomenclatures(info.nomenclature, info.orders_month)
        nomenclature_collections = self.red.merge_nomenclature_with_med_collections(nomenclature,
                                                                                    collections_merged_1_2_3_4)
        orders_stocks_by_day_collections = self.red.merge_orders_with_med_collections(info.orders_month,
                                                                                      collections_merged_1_2_3_4)
        actual_orders_info = self.red.merge_orders_info(info.orders_data_from_file, orders_stocks_by_day_collections)
        return {ORDERS_FILE_NAME: actual_orders_info,
                NOMENCLATURE_FILE_NAME: nomenclature_collections,
                NOMENCLATURE_DAY_FILE_NAME: nomenclature_collections}
