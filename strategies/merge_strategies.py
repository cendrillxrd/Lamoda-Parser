from abc import ABC, abstractmethod

import pandas as pd

from config import ON_THE_WAY_GOODS_SHIPS_STATUS, ON_THE_WAY_SHIP_STATUS
from dto.columns_main_dto import ColumnsMainDTO
from dto.columns_nomenclature_dto import ColumnsNomenclatureDTO

columns_main = ColumnsMainDTO()
columns_nomenclature = ColumnsNomenclatureDTO()


class MergeStrategies(ABC):
    @abstractmethod
    def merge(self, *args) -> pd.DataFrame:
        pass


class MergeByShipStrategy(MergeStrategies):
    def __init__(self, merge_on: str = columns_main.sku):
        self.merge_on = merge_on

    def merge(self, nomenclature: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
        filtered_df = orders[(orders[columns_main.status].isin(ON_THE_WAY_SHIP_STATUS))
                             & (orders[columns_main.status_product].isin(ON_THE_WAY_GOODS_SHIPS_STATUS))].copy()
        article_counts = filtered_df[columns_main.sku].value_counts().reset_index().copy()
        merged_df = pd.merge(nomenclature, article_counts, on=self.merge_on, how='left')
        merged_df.rename({'count': columns_nomenclature.on_the_way}, inplace=True, axis=1)

        return merged_df


class MergeCollections(MergeStrategies):
    def __init__(self, merge_on: str = columns_nomenclature.supplier_parent_sku):
        self.merge_on = merge_on

    def merge(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        merged_df = pd.concat([df1, df2], ignore_index=True)
        return merged_df


class MergeLamodaCollections(MergeStrategies):
    def __init__(self, merge_on: str = columns_nomenclature.supplier_parent_sku):
        self.merge_on = merge_on

    def merge(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        # Паттерн для всех указанных вариантов
        pattern = r'_(\d{2}|S|L|M|M-L|3XL|XS|XXL|XS-S)$'
        df1[columns_nomenclature.supplier_parent_sku] = df1[
            columns_nomenclature.supplier_parent_sku].str.replace(
            pattern, '', regex=True)
        df1[self.merge_on] = df1[self.merge_on].astype(str)
        df2[self.merge_on] = df2[self.merge_on].astype(str)
        merged_df = pd.merge(df1, df2, on=self.merge_on, how='left')
        return merged_df


class MergeOrders(MergeStrategies):
    def __init__(self, merge_on: tuple = (columns_main.id, columns_main.sku)):
        self.merge_on = merge_on

    def _add_position_counter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Добавляет временный счетчик позиций"""
        df = df.copy()
        df['_temp_position'] = df.groupby(list(self.merge_on)).cumcount()
        return df

    def merge(self, orders_main: pd.DataFrame, orders_new: pd.DataFrame) -> pd.DataFrame:
        # Добавляем временный счетчик
        orders_main_with_pos = self._add_position_counter(orders_main)
        orders_new_with_pos = self._add_position_counter(orders_new)

        # Полный список для индекса
        full_merge_on = list(self.merge_on) + ['_temp_position']

        # Устанавливаем индекс
        df_main_indexed = orders_main_with_pos.set_index(full_merge_on)
        df_additional_indexed = orders_new_with_pos.set_index(full_merge_on)

        # Обновляем данные
        result = df_additional_indexed.combine_first(df_main_indexed)

        # Сбрасываем индекс
        result = result.reset_index()

        # Удаляем временную колонку
        result = result.drop('_temp_position', axis=1)

        # Сортируем
        result.sort_values(columns_main.created_at, inplace=True, ascending=True)

        return result


class MergeOrdersCollections(MergeStrategies):
    def __init__(self, merge_on: str = columns_nomenclature.supplier_parent_sku):
        self.merge_on = merge_on

    def merge(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        result = self.fuzzy_merge(df1, df2, columns_main.sku, self.merge_on)
        return result

    @staticmethod
    def fuzzy_merge(df1, df2, left_on, right_on):
        # Преобразуем артикулы к строке и нормализуем
        df1_arts = df1[left_on].astype(str).str.strip().str.lower().fillna("").tolist()
        df2_arts = df2[right_on].astype(str).str.strip().str.lower().fillna("").tolist()
        df2_data = df2.to_dict('records')

        results = []

        for i, art1 in enumerate(df1_arts):
            matched_idx = -1

            # Поиск совпадения
            for j, art2 in enumerate(df2_arts):
                if art2 and art1 and art2 in art1:
                    matched_idx = j
                    break

            # Создание результирующей строки
            if matched_idx >= 0:
                # Объединяем с данными из df2
                result_row = {**df1.iloc[i].to_dict(), **df2_data[matched_idx]}
            else:
                # Только данные из df1
                result_row = df1.iloc[i].to_dict()
                # Добавляем None для колонок из df2
                for col in df2.columns:
                    if col != right_on:
                        result_row[col] = None

            results.append(result_row)

        return pd.DataFrame(results)
