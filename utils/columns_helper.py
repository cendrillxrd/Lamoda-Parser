import pandas as pd

from config import BASE_COLUMNS_NAME


def correct_columns_name(df: pd.DataFrame) -> pd.DataFrame:
    columns_name = [column for column in df.columns if column in BASE_COLUMNS_NAME]

    columns_rename = {k: BASE_COLUMNS_NAME.get(k) for k in columns_name}
    df.rename(columns_rename,
              inplace=True,
              axis=1)
    return df
