from api_key import ApiKeyManager
from dto.info_dto import InfoDTO
from service.api_service import APIService, MedService
from utils.date_helper import get_today_date

today = get_today_date()


class InfoCollector:
    def __init__(self):
        self.api_key = ApiKeyManager()
        self.api = APIService(self.api_key)
        self.med = MedService()

    def collect_info(self) -> InfoDTO:
        nomenclature = self.api.get_all_nomenclatures()
        orders_month = self.api.get_orders_info_by_products(date_str=today, period='month')
        collections1 = self.med.get_med_collections_first()
        collections2 = self.med.get_med_collections_second()
        collections3 = self.med.get_med_collections_third()
        collections4 = self.med.get_med_collections_fourth()

        return InfoDTO(
            orders_month=orders_month,
            nomenclature=nomenclature,
            collection1=collections1,
            collection2=collections2,
            collection3=collections3,
            collection4=collections4,
        )
