from dto.columns_main_dto import ColumnsMainDTO
from dto.info_dto import InfoDTO
from service.redaction import RedactionService
from utils.db_helper import TABLE_LAMODA_NOMENCLATURE, TABLE_LAMODA_ORDERS


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
        orders_info = self.red.merge_orders_with_med_collections(info.orders_month,
                                                                  collections_merged_1_2_3_4)

        return {TABLE_LAMODA_ORDERS: orders_info,
                TABLE_LAMODA_NOMENCLATURE: nomenclature_collections}
