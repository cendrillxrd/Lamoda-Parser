from abc import ABC, abstractmethod
from io import BytesIO
from typing import Union

import pandas as pd
from dto.columns_main_dto import ColumnsMainDTO
from config import BASE_COLUMNS_NAME
from dto.columns_nomenclature_dto import ColumnsNomenclatureDTO
from utils.date_helper import get_today_date
from utils.save_helper import correct_columns_name


class ConverterStrategy(ABC):
    def __init__(self):
        self.columns_main = ColumnsMainDTO()
        self.columns_nomenclature = ColumnsNomenclatureDTO()

    @abstractmethod
    def converting(self, data) -> Union[pd.DataFrame, list]:
        pass


class ConvNomenclaturesStrategy(ConverterStrategy):
    def converting(self, data: dict) -> pd.DataFrame:
        df = pd.DataFrame(data)
        df.drop('sku', axis=1, inplace=True)
        columns_name = [column for column in df.columns if column in BASE_COLUMNS_NAME]
        columns_rename = {k: BASE_COLUMNS_NAME.get(k) for k in columns_name}
        df.rename(columns_rename,
                  inplace=True,
                  axis=1)
        df[self.columns_nomenclature.date] = get_today_date()

        return df


class ConvNomenclaturesPricesStrategy(ConverterStrategy):
    def converting(self, data: dict) -> pd.DataFrame:
        df = pd.DataFrame(data)
        assigned_df = df.assign(price=df['_embedded'].apply(lambda x: x['sellValues'][0]['price']))
        columns_name = [column for column in assigned_df.columns if column in BASE_COLUMNS_NAME]
        columns_rename = {k: BASE_COLUMNS_NAME.get(k) for k in columns_name}
        assigned_df.rename(columns_rename,
                           inplace=True,
                           axis=1)
        df_prices = assigned_df[[self.columns_nomenclature.supplier_sku, self.columns_nomenclature.price]].copy()

        return df_prices


class ConvStockStrategy(ConverterStrategy):
    def converting(self, data: dict) -> pd.DataFrame:
        df = pd.DataFrame(data)
        columns_name = [column for column in df.columns if column in BASE_COLUMNS_NAME]
        columns_rename = {k: BASE_COLUMNS_NAME.get(k) for k in columns_name}
        df.rename(columns_rename,
                  inplace=True,
                  axis=1)
        return df


class ConvOrderStrategy(ConverterStrategy):
    def converting(self, data: dict) -> list:
        df = pd.DataFrame(data)
        order_ids = df['id'].tolist()
        return order_ids


class ConvOrderInfoStrategy(ConverterStrategy):
    def converting(self, data: list[dict]) -> pd.DataFrame:
        list_for_df = []

        for order in data:
            items = order['_embedded']['items']
            city = order['_embedded']['shippingAddress']['city']
            shipping_method_code = order['_embedded']['deliveryMethod']['shippingMethodCode']
            partner = order['_embedded']['partner']['shopName']

            for item in items:
                order_info = {
                    self.columns_main.shop_name: partner,
                    self.columns_main.id: order['id'],
                    self.columns_main.payment_method: order['paymentMethod'],
                    self.columns_main.status: order['status'],
                    self.columns_main.created_at: order['createdAt'],
                    self.columns_main.updated_at: order['updatedAt'],
                    self.columns_main.comment: order['comment'],
                    self.columns_main.shipping_method_code: shipping_method_code,
                    self.columns_main.city: city,
                    self.columns_main.currency: order['currency'],
                }
                item['status_product'] = item.pop('status')
                item['id_item_order'] = item.pop('id')
                order_info.update(item)

                list_for_df.append(order_info)

        df = pd.DataFrame(list_for_df)
        df.to_csv('new_orders.csv', index=False, encoding='cp1251')
        columns_name = [column for column in df.columns if column in BASE_COLUMNS_NAME]
        columns_rename = {k: BASE_COLUMNS_NAME.get(k) for k in columns_name}
        df.rename(columns_rename,
                  inplace=True,
                  axis=1)

        return df


class ConvMEDCollections(ConverterStrategy):
    def converting(self, data, **kwargs) -> pd.DataFrame:
        """Преобразует данные о коллекциях на меде в DataFrame"""
        med_collections_df = pd.read_excel(BytesIO(data.content))

        med_collections_df = correct_columns_name(med_collections_df)

        med_collections_df_without_unnecessary_columns = med_collections_df[
            [self.columns_nomenclature.supplier_parent_sku, self.columns_nomenclature.collection]]
        med_collections_df_without_unnecessary_columns.drop_duplicates(
            subset=self.columns_nomenclature.supplier_parent_sku, inplace=True)
        med_collections_df_without_unnecessary_columns.reset_index(inplace=True, drop=True)
        return med_collections_df_without_unnecessary_columns
