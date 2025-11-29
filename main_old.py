from pybit.unified_trading import HTTP
from cfg import BASE_URL_TEST

base_url = BASE_URL_TEST
sessions = HTTP(testnet=True)

response = sessions.get_kline(
    category="spot",
    symbol="BTCUSDT",
    interval="1",
    limit=1
)
print(response)
if response.get('retCode') != 0:
    print("so cunt")
else:
    candel = response.get("result").get("list")
    print(f'{candel[0][4]}usdt')


