from dto.info_dto import InfoDTO
from service.api_service import APIService


class InfoCollector:
    def __init__(self):
        self.api = APIService()

    def collect_info(self) -> InfoDTO:
        orders = self.api.get_orders_info_by_products()
        stock = self.api.get_stocks()
        return InfoDTO(
            orders=orders,
            stock=stock
        )
