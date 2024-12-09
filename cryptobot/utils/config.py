import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import yaml

class Config:
    def __init__(self, config_path: Optional[str] = None):
        # Load environment variables
        load_dotenv()
        
        # Load config file if provided
        self.config: Dict[str, Any] = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)

    @property
    def exchange_api_key(self) -> str:
        return os.getenv('EXCHANGE_API_KEY', '')

    @property
    def exchange_api_secret(self) -> str:
        return os.getenv('EXCHANGE_API_SECRET', '')

    @property
    def risk_per_trade(self) -> float:
        return float(os.getenv('RISK_PER_TRADE', '0.02'))

    @property
    def max_position_size(self) -> float:
        return float(os.getenv('MAX_POSITION_SIZE', '0.1'))

    @property
    def trading_pairs(self) -> list:
        pairs = self.config.get('trading_pairs', ['BTC/USDT'])
        return pairs if isinstance(pairs, list) else [pairs]

    @property
    def strategy_params(self) -> Dict[str, Any]:
        return self.config.get('strategy', {})

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by key"""
        return self.config.get(key, default)