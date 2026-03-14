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


class CorrCollectionsNomenclature(CorrectorStrategy):
    def correcting(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        df.fillna(0, inplace=True)  # заменяем пустоту на нули
        df_correct = df[asdict(self.columns_nomenclature).values()].copy()
        return df_correct


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

        # Удалить дубликаты после слияния
        df = df.drop_duplicates(subset=(self.columns_main.id,
                                        self.columns_main.sku,
                                        self.columns_main.created_at), keep='first')
        return df


class CorrNomenclatureTableStrategy(CorrectorStrategy):
    def correcting(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        df_numeric = df.fillna(0).copy()
        df_numeric[self.columns_nomenclature.total_quantity] = (df_numeric[self.columns_nomenclature.quantity]
                                                                + df_numeric[self.columns_nomenclature.on_the_way])
        df_numeric[self.columns_nomenclature.created_at] = pd.to_datetime(
            df_numeric[self.columns_nomenclature.created_at],
            format='mixed',
            dayfirst=True,
            errors='coerce'
        )

        # Дата для сравнения (01.09.2024)
        cutoff_date = pd.to_datetime('01.09.2024', format='%d.%m.%Y')

        filtered_df = df_numeric[
            ((df_numeric[self.columns_nomenclature.created_at] >= cutoff_date) |  # ВСЕ данные позже 01.09.2024
             (
                     (df_numeric[self.columns_nomenclature.created_at] < cutoff_date) &  # данные ДО 01.09.2024
                     (df_numeric[self.columns_nomenclature.quantity] != 0)  # но только с ненулевыми остатками
             )) &
            (~df_numeric[self.columns_nomenclature.status].isin(['photoshoot_pending', 'inactive']))
            ].copy()
        columns = [self.columns_nomenclature.on_the_way, self.columns_nomenclature.total_quantity]

        for column in columns:
            filtered_df[column] = pd.to_numeric(filtered_df[column], downcast="integer")

        return filtered_df


class CorrCollectionsOrders(CorrectorStrategy):
    def correcting(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        df.fillna(0, inplace=True)  # заменяем пустоту на нули
        df = df[asdict(self.columns_main).values()].copy()
        return df
