from abc import ABC, abstractmethod
from dataclasses import asdict

import pandas as pd

from dto.columns_dto import ColumnsDTO


class CorrectorStrategy(ABC):
    def __init__(self):
        self.columns = ColumnsDTO()

    @abstractmethod
    def correcting(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


class CorrMainTableStrategy(CorrectorStrategy):
    def correcting(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.fillna(0).infer_objects(copy=False)
        df = df[asdict(self.columns).values()].copy()
        columns = [self.columns.stock, self.columns.total_discount, self.columns.sale_price, self.columns.paid_price,
                   self.columns.base_price, self.columns.coupon_discount, self.columns.loyalty_discount,
                   self.columns.partner_agreed_price, self.columns.partner_agreed_discount,
                   self.columns.other_discounts]
        for column in columns:
            df[column] = pd.to_numeric(df[column], downcast="integer")
        return df
