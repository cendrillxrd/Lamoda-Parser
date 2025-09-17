import pandas as pd

from dto.info_dto import InfoDTO
from service.redaction import RedactionService


class InfoRedactor:
    def __init__(self):
        self.red = RedactionService()

    def redact_info(self, info: InfoDTO) -> dict:
        orders_stocks = self.red.merge_orders_with_stock(info.orders, info.stock)
        nomenclature = self.red.correct_nomenclatures(info.nomenclature)
        return {'orders_stocks': orders_stocks, 'nomenclature': nomenclature}
