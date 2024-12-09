from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import pandas as pd

@dataclass
class IndicatorResult:
    value: float
    signal: Optional[str] = None

class TechnicalIndicators:
    @staticmethod
    def sma(data: List[float], period: int) -> IndicatorResult:
        if len(data) < period:
            raise ValueError(f"Not enough data for SMA calculation. Need {period} points")
        sma_value = np.mean(data[-period:])
        current_price = data[-1]
        signal = "BUY" if current_price > sma_value else "SELL"
        return IndicatorResult(sma_value, signal)