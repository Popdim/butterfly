import pandas as pd


def to_pandas_frame(timeframe: str):
    tf = timeframe.lower()
    if tf == "1m":
        return "1T"
    if tf == "15m":
        return "15T"
    if tf == "5m":
        return "5T"
    raise ValueError(f"неизвестный формат TimeFrame")
def resample_auntie(df_1m:pd.DataFrame, tf):
    frame = to_pandas_frame(tf)
    egg ={
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
        "turnover": "sum"
    }
    df_new = df_1m.resample(rule=frame, label="right",closed="right", origin="start_day").agg(egg).dropna(how="any")
    df_new = df_new.astype({
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "turnover": "float64"
    })
    return df_new
