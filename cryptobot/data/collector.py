import asyncio
from typing import Dict, Any, List, Optional
import ccxt
import pandas as pd

class DataCollector:
    def __init__(self, exchange_id: str = 'binance', symbol: str = 'BTC/USDT'):
        self.exchange = getattr(ccxt, exchange_id)()
        self.symbol = symbol
        self.websocket = None

    async def fetch_historical_data(self, timeframe: str = '1h', limit: int = 1000) -> pd.DataFrame:
        """Fetch historical OHLCV data"""
        ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df.set_index('timestamp')

    async def start_realtime_feed(self, callback):
        """Start websocket connection for real-time data"""
        while True:
            try:
                ticker = self.exchange.fetch_ticker(self.symbol)
                await callback({
                    'timestamp': pd.Timestamp.now(),
                    'price': ticker['last'],
                    'volume': ticker['baseVolume']
                })
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Error in realtime feed: {e}")
                await asyncio.sleep(5)