from pybit.unified_trading import HTTP
from cfg import BASE_URL, KLINE_ENDPOINT
# import requests
# import time
import pandas as pd
# import numpy as np
from utils import utc_ms, get_today_utc_close


def fetch_klines_pybit(start_ms, end_ms, symbol="BTCUSDT", interval="1", category="spot", limit=1):
    """получаем свечи через pybit"""
    sessions = HTTP(testnet=True)  # для реальной работы должно быть равно False, для тестового True

    response = sessions.get_kline(
        category=category,
        symbol=symbol,
        interval=interval,
        start=start_ms,
        end=end_ms,
        limit=limit
    )
    # print(response)

    if response.get("retCode") != 0:
        raise RuntimeError(f"ошибка от bybit {response.get('retMsg')}")
    rows = response.get("result").get("list")
    print(rows)
    df = pd.DataFrame(rows, columns=["start", "open", "hype", "low", "close", "volume", "turnover"])
    print(df)
    df = df.astype({
        "start": "int64",
        "open": "float64",
        "hype": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "turnover": "float64"
    })
    df = df.sort_values("start").reset_index(drop=True)
    df["datetime"] = pd.to_datetime(df['start'], unit='ms', utc=True)
    df = df.set_index("datetime")
    # print(df.head())
    return df


if __name__ == '__main__':
    start_ms, end_ms = get_today_utc_close()
    result = fetch_klines_pybit(start_ms=start_ms, end_ms=end_ms, limit=10)
    print(result.tail())