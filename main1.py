from pybit.unified_trading import HTTP
from cfg import BASE_URL, KLINE_ENDPOINT
# import requests
# import time
import pandas as pd
# import numpy as np
from utils import utc_ms, get_today_utc_close



def fetch_klines_pybit(start_ms, end_ms, symbol="ETHUSDT", interval="1", category="spot", limit=1):
    """получаем свечи через pybit"""
    sessions=HTTP(testnet=True) #для реальной работы должно быть равно False, для тестового True

    response =sessions.get_kline(
        category=category,
        symbol=symbol,
        interval=interval,
        start=start_ms,
        end=end_ms,
        limit=limit
    )
    print(response)

if __name__ == '__main__':
    start_ms, end_ms=get_today_utc_close()
    fetch_klines_pybit(start_ms=start_ms, end_ms=end_ms)

