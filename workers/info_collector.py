from dto.indo_update_dto import InfoUpdateDTO
from dto.info_dto import InfoDTO
from service.api_service import APIService
from api_key import ApiKeyManager


class InfoCollector:
    def __init__(self):
        self.api = ApiKeyManager()
        self.api = APIService(self.api)

    def collect_info(self) -> InfoDTO:
        orders = self.api.get_orders_info_by_products()
        stock = self.api.get_stocks()
        nomenclature = self.api.get_nomenclatures()
        return InfoDTO(
            orders=orders,
            stock=stock,
            nomenclature=nomenclature
        )

    def collect_info_for_update(self, date_str: str) -> InfoUpdateDTO:
        orders = self.api.get_orders_info_by_products(date_str=date_str)
        return InfoUpdateDTO(
            orders=orders,
        )
