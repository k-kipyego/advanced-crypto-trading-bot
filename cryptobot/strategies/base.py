from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class TradeSignal:
    action: str  # "BUY", "SELL", or "HOLD"
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signal(self, data: Dict[str, Any]) -> TradeSignal:
        """Generate trading signal based on market data"""
        pass

    @abstractmethod
    def update(self, market_data: Dict[str, Any]) -> None:
        """Update strategy state with new market data"""
        pass