import pandas as pd

ds2=  ["open", "high", "low", "close", "volume", "turnover"]


def required_column(df: pd.DataFrame, required: list):
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"нет данных {missing}")


def check_types(df: pd.DataFrame):
    required_column(df, ds2)
    for column in ds2:
        if not pd.api.types.is_numeric_dtype(df[column]):
            raise TypeError(f"колонка должн быть числом{column}")

def check_no_dublicate(df: pd.DataFrame):
    if df.index.duplicated().any():
        dup = df.index[df.index.duplicated()].unique()
        raise AssertionError(f"наши дубликаты {dup[:5]}")
