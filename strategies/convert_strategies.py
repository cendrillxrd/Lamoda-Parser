from abc import ABC, abstractmethod

import pandas as pd


class ConverterStrategy(ABC):
    def __init__(self):
        # self.columns = ColumnsDTO()
        pass

    @abstractmethod
    def converting(self, data) -> pd.DataFrame:
        pass


class ConvNomenclaturesStrategy(ConverterStrategy):
    def converting(self, data: dict) -> pd.DataFrame:
        return data


class ConvStockStrategy(ConverterStrategy):
    def converting(self, data: dict) -> pd.DataFrame:
        return data


class ConvOrderStrategy(ConverterStrategy):
    def converting(self, data: dict) -> pd.DataFrame:
        return data
