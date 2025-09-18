from abc import ABC, abstractmethod
from dataclasses import asdict

import pandas as pd

from dto.columns_main_dto import ColumnsMainDTO
from dto.columns_nomenclature_dto import ColumnsNomenclatureDTO


class CorrectorStrategy(ABC):
    def __init__(self):
        self.columns_main = ColumnsMainDTO()
        self.columns_nomenclature = ColumnsNomenclatureDTO()

    @abstractmethod
    def correcting(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        pass


class CorrMainTableStrategy(CorrectorStrategy):
    def correcting(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        df = df.fillna(0).infer_objects(copy=False)  # Сначала заполняем пропуски
        df = df[asdict(self.columns_main).values()].copy()
        columns = [self.columns_main.stock, self.columns_main.total_discount, self.columns_main.sale_price,
                   self.columns_main.paid_price,
                   self.columns_main.base_price, self.columns_main.coupon_discount, self.columns_main.loyalty_discount,
                   self.columns_main.partner_agreed_price, self.columns_main.partner_agreed_discount,
                   self.columns_main.other_discounts]
        for column in columns:
            df[column] = pd.to_numeric(df[column], downcast="integer")
        return df


class CorrNewInfoTableStrategy(CorrectorStrategy):
    def correcting(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        columns_to_update = [
            self.columns_main.updated_at,
            self.columns_main.status,
            self.columns_main.status_product
        ]
        for column in columns_to_update:
            df[column] = df[column + '_new'].combine_first(df[column])
            df.drop(column + '_new', axis=1, inplace=True)
        return df


class CorrNomenclatureTableStrategy(CorrectorStrategy):
    def correcting(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        df = df[asdict(self.columns_nomenclature).values()].copy()
        df[self.columns_nomenclature.created_at] = pd.to_datetime(
            df[self.columns_nomenclature.created_at],
            format='mixed',
            dayfirst=True,  # Важно! Первое число - день
            errors='coerce'
        )

        # Дата для сравнения (01.09.2024)
        cutoff_date = pd.to_datetime('01.09.2024', format='%d.%m.%Y')

        filtered_df = df[
            (df[self.columns_nomenclature.created_at] >= cutoff_date) |  # ВСЕ данные позже 01.09.2024
            (
                    (df[self.columns_nomenclature.created_at] < cutoff_date) &  # данные ДО 01.09.2024
                    (df[self.columns_nomenclature.quantity] != 0)  # но только с ненулевыми остатками
            )
            ].copy()
        return filtered_df
