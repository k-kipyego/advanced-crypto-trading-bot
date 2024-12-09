from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class Position:
    size: float
    entry_price: float
    stop_loss: float
    take_profit: Optional[float] = None

class RiskManager:
    def __init__(self, max_position_size: float, risk_per_trade: float):
        self.max_position_size = max_position_size
        self.risk_per_trade = risk_per_trade