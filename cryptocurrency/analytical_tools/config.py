from dataclasses import dataclass, field
import ccxt


@dataclass(frozen=True)
class Config:
    """Deterimining key programme settings."""
    
    api_key: str
    secret_key: str
    exchange: str = field(default="binance")
    trade_interval: int = field(default=24)
    max_position: float = field(default=10)
    min_position: float = field(default=30)
    stable_coin_main: str = field(default='BUSD')
    stable_coin_second: str = field(default='USDT')
    
    def get_exchange_fee(self, market: str) -> float:
        """Defining fee structure for selected exchanges."""
        
        fees = {"binance": {"spot": 0.05, "futures": 0.01}, 
                "bybit": {"spot": 0.1, "futures": 0.01}}
        
        return fees[self.exchange][market]
            
    def connect_client_api(self):
        """Set up api conection with an exchange."""
        
        if self.exchange == "binance":
            client = ccxt.binance({
                'apiKey': self.api_key,
                'secret': self.secret_key
                })  
        return client   
    