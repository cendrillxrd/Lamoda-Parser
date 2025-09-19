from dataclasses import asdict, dataclass

import pandas as pd


@dataclass
class InfoDTO:
    orders_day: pd.DataFrame
    orders_month: pd.DataFrame
    stock: pd.DataFrame
    nomenclature: pd.DataFrame
