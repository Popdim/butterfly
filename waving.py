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


def fetch_klines(symbol="ETHUSDT", interval="1", category="spot", limit=1, end=None):
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


def fetch_and_bars(symbol="ETHUSDT", interval="1", category="spot", n=1):
    bars = []
    needed = int(n)
    h2o = 1000 if needed > 1000 else needed
    end_time = int(time.time() * 1000)
    while needed > 0:
        take = min(h2o, needed)
        chunk = fetch_klines(symbol=symbol, interval=interval, category=category, limit=take, end=end_time)
        if not chunk:
            break
        bars.extend(chunk)
        oldest_start = int(chunk[-1][0])
        end_time = oldest_start - interval_to_ms(interval)
        needed = n - len(bars)
        time.sleep(1)
    if not bars:
        raise RuntimeError("RuntimeError")
    df = pd.DataFrame(bars, columns=['startTime', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
    df['startTime'] = pd.to_datetime(df['startTime'].astype(int), unit='ms', utc=True)
    for col in ['open', 'high', 'low', 'close', 'volume', 'turnover']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.sort_values('startTime').reset_index(drop=True)
    df = df.set_index('startTime')
    return df


def rsi(series: pd.Series, period):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = delta.where(delta < 0, 0.0)
    avg_gained = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gained / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def sma(series, period):
    return series.rolling(window=period, min_periods=period).mean()


def ema(series, period):
    return series.ewm(span=period, min_periods=period, adjust=False).mean()


if __name__ == '__main__':
    res = fetch_klines(limit=10)
    print(res)
    df = fetch_and_bars(symbol='BTCUSDT', interval="1", n=500)
    # print(df)
    df['sma20'] = sma(df['close'], period=20)
    df['ema20'] = ema(df['close'], period=20)
    df['rsi20'] = rsi(df['close'], period=20)
    print(df['rsi20'])
    print(df['ema20'])
    print(df['sma20'])
    df.to_csv('ethereal.csv')