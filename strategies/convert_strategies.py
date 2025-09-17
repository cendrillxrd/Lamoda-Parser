from abc import ABC, abstractmethod
from typing import Union

import pandas as pd
from dto.columns_main_dto import ColumnsMainDTO
from config import BASE_COLUMNS_NAME


class ConverterStrategy(ABC):
    def __init__(self):
        self.columns = ColumnsMainDTO()
        pass

    @abstractmethod
    def converting(self, data) -> Union[pd.DataFrame, list]:
        pass


class ConvNomenclaturesStrategy(ConverterStrategy):
    def converting(self, data: dict) -> pd.DataFrame:
        df = pd.DataFrame(data)
        columns_name = [column for column in df.columns if column in BASE_COLUMNS_NAME]
        columns_rename = {k: BASE_COLUMNS_NAME.get(k) for k in columns_name}
        df.rename(columns_rename,
                  inplace=True,
                  axis=1)

        return df


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
                    self.columns.shop_name: partner,
                    self.columns.id: order['id'],
                    self.columns.payment_method: order['paymentMethod'],
                    self.columns.status: order['status'],
                    self.columns.created_at: order['createdAt'],
                    self.columns.updated_at: order['updatedAt'],
                    self.columns.comment: order['comment'],
                    self.columns.shipping_method_code: shipping_method_code,
                    self.columns.city: city,
                    self.columns.currency: order['currency'],
                }
                item['status_product'] = item.pop('status')
                item['id_item_order'] = item.pop('id')
                order_info.update(item)

                list_for_df.append(order_info)

        df = pd.DataFrame(list_for_df)

        columns_name = [column for column in df.columns if column in BASE_COLUMNS_NAME]
        columns_rename = {k: BASE_COLUMNS_NAME.get(k) for k in columns_name}
        df.rename(columns_rename,
                  inplace=True,
                  axis=1)
        return df
