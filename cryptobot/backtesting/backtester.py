from typing import Dict, Any, List
import pandas as pd
import numpy as np
from ..strategies.base import BaseStrategy
from ..core.risk_manager import RiskManager

class Backtester:
    def __init__(self, 
                 strategy: BaseStrategy,
                 risk_manager: RiskManager,
                 initial_balance: float = 10000.0):
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position = None
        self.trades: List[Dict[str, Any]] = []

    def run(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Run backtest on historical data"""
        results = {
            'trades': [],
            'balance': [],
            'equity': []
        }

        for timestamp, row in data.iterrows():
            market_data = {
                'timestamp': timestamp,
                'open': row['open'],
                'high': row['high'],
                'low': row['low'],
                'close': row['close'],
                'volume': row['volume']
            }

            # Update strategy with new data
            self.strategy.update(market_data)

            # Generate trading signal
            signal = self.strategy.generate_signal(market_data)

            # Process signal
            if signal.action != 'HOLD':
                if self.position is None and signal.action in ['BUY', 'SELL']:
                    # Open new position
                    position = self.risk_manager.calculate_position_size(
                        self.balance,
                        signal.entry_price,
                        signal.stop_loss
                    )
                    self.position = {
                        'type': signal.action,
                        'entry_price': signal.entry_price,
                        'size': position.size,
                        'stop_loss': signal.stop_loss,
                        'take_profit': signal.take_profit
                    }
                    self.trades.append({
                        'timestamp': timestamp,
                        'type': signal.action,
                        'price': signal.entry_price,
                        'size': position.size
                    })

            # Update position if exists
            if self.position is not None:
                price = row['close']
                pnl = self._calculate_pnl(price)
                results['equity'].append(self.balance + pnl)

                # Check stop loss and take profit
                if self._should_close_position(row):
                    self._close_position(price, timestamp)

            results['balance'].append(self.balance)

        return self._generate_backtest_results(results)

    def _calculate_pnl(self, current_price: float) -> float:
        """Calculate current position PnL"""
        if self.position is None:
            return 0.0

        price_diff = current_price - self.position['entry_price']
        if self.position['type'] == 'SELL':
            price_diff = -price_diff

        return price_diff * self.position['size']

    def _should_close_position(self, row: pd.Series) -> bool:
        """Check if position should be closed based on SL/TP"""
        if self.position is None:
            return False

        if self.position['type'] == 'BUY':
            return (row['low'] <= self.position['stop_loss'] or 
                    (self.position['take_profit'] is not None and 
                     row['high'] >= self.position['take_profit']))
        else:  # SELL position
            return (row['high'] >= self.position['stop_loss'] or 
                    (self.position['take_profit'] is not None and 
                     row['low'] <= self.position['take_profit']))

    def _close_position(self, price: float, timestamp: pd.Timestamp) -> None:
        """Close current position and update balance"""
        pnl = self._calculate_pnl(price)
        self.balance += pnl
        self.trades.append({
            'timestamp': timestamp,
            'type': 'CLOSE',
            'price': price,
            'pnl': pnl
        })
        self.position = None

    def _generate_backtest_results(self, results: Dict[str, List]) -> Dict[str, Any]:
        """Generate final backtest results and statistics"""
        equity_curve = pd.Series(results['equity'])
        returns = equity_curve.pct_change().dropna()

        return {
            'trades': self.trades,
            'equity_curve': equity_curve.tolist(),
            'total_return': (self.balance - self.initial_balance) / self.initial_balance,
            'sharpe_ratio': self._calculate_sharpe_ratio(returns),
            'max_drawdown': self._calculate_max_drawdown(equity_curve),
            'total_trades': len(self.trades),
            'final_balance': self.balance
        }

    @staticmethod
    def _calculate_sharpe_ratio(returns: pd.Series) -> float:
        """Calculate Sharpe ratio"""
        if len(returns) < 2:
            return 0.0
        return np.sqrt(252) * returns.mean() / returns.std()

    @staticmethod
    def _calculate_max_drawdown(equity_curve: pd.Series) -> float:
        """Calculate maximum drawdown"""
        rolling_max = equity_curve.expanding(min_periods=1).max()
        drawdowns = equity_curve / rolling_max - 1.0
        return float(drawdowns.min())