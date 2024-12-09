import pandas as pd
from typing import Dict, Any
import json
import os

class DataStorage:
    def __init__(self, base_path: str = 'data'):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def save_historical_data(self, data: pd.DataFrame, symbol: str, timeframe: str):
        """Save historical data to CSV"""
        filename = f"{symbol.replace('/', '_')}_{timeframe}.csv"
        filepath = os.path.join(self.base_path, filename)
        data.to_csv(filepath)

    def load_historical_data(self, symbol: str, timeframe: str) -> pd.DataFrame:
        """Load historical data from CSV"""
        filename = f"{symbol.replace('/', '_')}_{timeframe}.csv"
        filepath = os.path.join(self.base_path, filename)
        return pd.read_csv(filepath, index_col=0, parse_dates=True)

    def save_trade_history(self, trade_data: Dict[str, Any]):
        """Save trade history to JSON"""
        filepath = os.path.join(self.base_path, 'trade_history.json')
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                history = json.load(f)
        else:
            history = []
        history.append(trade_data)
        with open(filepath, 'w') as f:
            json.dump(history, f, indent=2)