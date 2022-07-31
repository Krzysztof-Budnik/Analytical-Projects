import vectorbt as vbt
from config import ALPACA_ID, ALPACA_SECRET_KEY

vbt.settings.data['alpaca']['key_id'] = ALPACA_ID
vbt.settings.data['alpaca']['secret_key'] = ALPACA_SECRET_KEY


def main(symbol: str, start_date: str, end_date: str, candles: str, limit: int, file_name: str):
    """Downloads data with alpaca api in csv format."""
    
    data = vbt.AlpacaData.download(symbol, start=start_date, end=end_date, timeframe=candles, limit=limit)
    data.get().to_csv(f"{file_name}.csv")
    
    
if __name__ == "__main__":
    main(symbol = 'SPY',
         start_date = '2016-01-01', 
         end_date = '2021-12-16', 
         candles = '1d', 
         limit = 1000,
         file_name = "SPY-data")
    