from typing import List, Dict, Any
import numpy as np
from .base import BaseStrategy, TradeSignal

class MovingAverageCrossover(BaseStrategy):
    def __init__(self, short_period: int = 10, long_period: int = 20):
        self.short_period = short_period
        self.long_period = long_period
        self.prices: List[float] = []

    def update(self, market_data: Dict[str, Any]) -> None:
        self.prices.append(market_data['close'])
        if len(self.prices) > self.long_period * 2:
            self.prices.pop(0)

    def generate_signal(self, data: Dict[str, Any]) -> TradeSignal:
        if len(self.prices) < self.long_period:
            return TradeSignal(action="HOLD")

        short_ma = np.mean(self.prices[-self.short_period:])
        long_ma = np.mean(self.prices[-self.long_period:])
        current_price = self.prices[-1]

        if short_ma > long_ma:
            stop_loss = min(self.prices[-self.short_period:]) * 0.95
            take_profit = current_price + (current_price - stop_loss) * 2
            return TradeSignal(
                action="BUY",
                entry_price=current_price,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
        elif short_ma < long_ma:
            stop_loss = max(self.prices[-self.short_period:]) * 1.05
            take_profit = current_price - (stop_loss - current_price) * 2
            return TradeSignal(
                action="SELL",
                entry_price=current_price,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
        return TradeSignal(action="HOLD")