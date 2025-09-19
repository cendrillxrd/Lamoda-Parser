from dto.indo_update_dto import InfoUpdateDTO
from dto.info_dto import InfoDTO
from service.api_service import APIService
from api_key import ApiKeyManager
from utils.date_helper import get_today_date

today = get_today_date()


class InfoCollector:
    def __init__(self):
        self.api = ApiKeyManager()
        self.api = APIService(self.api)

    def collect_info(self) -> InfoDTO:
        orders_day = self.api.get_orders_info_by_products()
        orders_month = self.api.get_orders_info_by_products(date_str=today, period='month')
        stock = self.api.get_stocks()
        nomenclature = self.api.get_nomenclatures()
        return InfoDTO(
            orders_day=orders_day,
            orders_month=orders_month,
            stock=stock,
            nomenclature=nomenclature
        )

    def collect_info_for_update(self, date_str: str) -> InfoUpdateDTO:
        orders = self.api.get_orders_info_by_products(date_str=date_str, period='day')
        return InfoUpdateDTO(
            orders=orders,
        )
