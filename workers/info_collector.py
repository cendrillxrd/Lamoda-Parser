from dto.indo_update_dto import InfoUpdateDTO
from dto.info_dto import InfoDTO
from service.api_service import APIService, MedService
from api_key import ApiKeyManager
from utils.date_helper import get_today_date

today = get_today_date()


class InfoCollector:
    def __init__(self):
        self.api = ApiKeyManager()
        self.api = APIService(self.api)
        self.med = MedService()

    def collect_info(self) -> InfoDTO:
        prices_nomenclature = self.api.get_nomenclatures_prices()
        nomenclature = self.api.get_nomenclatures()
        # orders_day = self.api.get_orders_info_by_products()
        orders_month = self.api.get_orders_info_by_products(date_str=today, period='month')
        # stock = self.api.get_stocks()
        collections1 = self.med.get_med_collections_first()
        collections2 = self.med.get_med_collections_second()

        return InfoDTO(
            # orders_day=orders_day,
            orders_month=orders_month,
            # stock=stock,
            nomenclature=nomenclature,
            collection1=collections1,
            collection2=collections2,
            prices_nomenclature=prices_nomenclature
        )

    def collect_info_for_update(self, date_str: str) -> InfoUpdateDTO:
        orders = self.api.get_orders_info_by_products(date_str=date_str, period='day')
        return InfoUpdateDTO(
            orders=orders,
        )
