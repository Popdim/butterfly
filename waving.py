from pybit.unified_trading import HTTP
from cfg import BASE_URL, KLINE_ENDPOINT
import requests
import time
import pandas as pd
import numpy as np


def interval_to_ms(interval):
    if interval.isdigit():
        minutes = int(interval)
        return minutes * 60000
    if interval == "D":
        return 24 * 60 * 60000
    if interval == "W":
        return 7 * 24 * 60 * 60000
    if interval == "M":
        return 30 * 24 * 60 * 60000
    raise ValueError("Неизвестный формат интервала")


def fetch_klines(symbol="BTCUSDT", interval="1", category="spot", limit=1, end=None):
    base_url = BASE_URL + KLINE_ENDPOINT
    params = {
        "category": category,
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    if end is not None:
        params["end"] = int(end)

    response = requests.get(url=base_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("result").get("list")


def fetch_and_bars(symbol="BTCUSDT", interval="1", category="spot", n=1):
    bars = []
    needed=int(n)
    h2o = 1000 if needed>1000 else needed
    end_time=int(time.time()*1000)
    while needed>0:
        take = min(h2o, needed)
        chunk = fetch_klines(symbol=symbol, interval=interval, category=category,limit=take, end=end_time)
        if not chunk:
            break
        bars.extend(chunk)
        oldest_start = int(chunk[-1][0])
        end_time = oldest_start-interval_to_ms(interval)

def sma(series, period):
    return series.rolling(window=period, min_periods=period).mean()


def ema(series, period):
    return series.ewm(span=period, min_periods=period, adjust=False).mean()


if __name__ == '__main__':
    res = fetch_klines(limit=10)
    print(res)
