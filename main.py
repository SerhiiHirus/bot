import asyncio
from config import api_key, api_secret
from setting import symbol, kline_time, rsi_len, rsi_low, rsi_high
from orders import market_order
from pybit.unified_trading import HTTP
import talib
import numpy as np


session = HTTP(testnet = False, demo = True, api_key=api_key, api_secret=api_secret)

async def run():
    while True:
        close_price = []

        responce = session.get_kline(
            category = "linear",
            symbol = symbol,
            interval = kline_time,
            limit = 1000
        )

        klines = responce.get('result',{}).get('list',[])
        klines = sorted(klines, key=lambda x :int(x[0]))

        for candle in klines:
            close_price_for_list = float(candle[4])
            close_price.append(close_price_for_list)

        close_price = np.array(close_price, dtype='float')

        # Условие сетапа и открытия сделки
        rsi_value = talib.RSI(close_price, timeperiod = rsi_len)[-1]
        print(f"RSI: {round(rsi_value, 2)}")

        if rsi_value < rsi_low:
            """BUY"""
            await market_order(session,symbol,"Buy",close_price)

        elif rsi_value > rsi_high:
            """SELL"""
            await market_order(session,symbol,"Sell",close_price)

        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(run())
