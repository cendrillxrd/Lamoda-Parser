from dataclasses import asdict, dataclass

import pandas as pd


@dataclass
class InfoDTO:
    orders: pd.DataFrame
    stock: pd.DataFrame
    nomenclature: pd.DataFrame
