# Advanced Crypto Trading Bot

A professional-grade cryptocurrency trading bot with advanced technical analysis, risk management, and backtesting capabilities. Built with Python, this bot provides a robust framework for implementing and testing trading strategies.

## 🚀 Features

- **Real-time Market Data**
  - Integration with major cryptocurrency exchanges
  - WebSocket support for live price updates
  - Historical data collection and storage

- **Advanced Technical Analysis**
  - Multiple technical indicators (SMA, EMA, RSI, MACD)
  - Custom indicator development framework
  - Signal generation and filtering

- **Risk Management**
  - Position sizing based on account risk
  - Dynamic stop-loss calculation
  - Take-profit management
  - Maximum drawdown protection

- **Strategy Framework**
  - Easy-to-implement strategy interface
  - Multiple timeframe analysis
  - Strategy combination support
  - Example strategies included

- **Backtesting Engine**
  - Historical performance analysis
  - Detailed trade statistics
  - Performance metrics calculation
  - Equity curve visualization

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/k-kipyego/advanced-crypto-trading-bot.git
   cd advanced-crypto-trading-bot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .[dev]  # Install with development dependencies
   ```

4. **Configure the environment**
   ```bash
   cp .env.example .env
   cp config.yaml.example config.yaml
   ```

## ⚙️ Configuration

1. **Environment Variables (.env)**
   ```ini
   EXCHANGE_API_KEY=your_api_key
   EXCHANGE_API_SECRET=your_api_secret
   RISK_PER_TRADE=0.02
   MAX_POSITION_SIZE=0.1
   LOG_LEVEL=INFO
   ```

2. **Trading Configuration (config.yaml)**
   ```yaml
   trading_pairs:
     - BTC/USDT
     - ETH/USDT

   strategy:
     name: MovingAverageCrossover
     parameters:
       short_period: 10
       long_period: 20
   ```

## 🚦 Usage

1. **Run the bot**
   ```bash
   python -m cryptobot
   ```

2. **Run backtesting**
   ```bash
   python -m cryptobot.backtesting --strategy ma_crossover --start 2023-01-01
   ```

3. **Generate performance report**
   ```bash
   python -m cryptobot.analysis.report
   ```

## 📊 Example Strategy

```python
from cryptobot.strategies import BaseStrategy
from cryptobot.core.indicators import TechnicalIndicators

class CustomStrategy(BaseStrategy):
    def __init__(self, rsi_period: int = 14):
        self.rsi_period = rsi_period
        self.prices = []

    def generate_signal(self, data):
        self.prices.append(data['close'])
        if len(self.prices) < self.rsi_period:
            return None

        rsi = TechnicalIndicators.rsi(self.prices, self.rsi_period)
        if rsi.value < 30:
            return {
                "action": "BUY",
                "stop_loss": data['close'] * 0.95
            }
        elif rsi.value > 70:
            return {
                "action": "SELL",
                "stop_loss": data['close'] * 1.05
            }
        
        return {"action": "HOLD"}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=cryptobot tests/

# Run specific test file
pytest tests/test_indicators.py
```

## 📝 Documentation

Detailed documentation is available in the `docs/` directory. To build the documentation:

```bash
cd docs
make html
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This trading bot is for educational and research purposes only. Cryptocurrency trading involves substantial risk of loss and is not suitable for every investor. The performance of this bot is not guaranteed, and users should carefully consider their financial situation and risk tolerance before using it with real funds.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape this project
- Built with Python and love for the crypto community
