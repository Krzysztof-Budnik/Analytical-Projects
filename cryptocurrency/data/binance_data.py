import config 
from binance.client import Client
import csv


client = Client(config.BINANCE_KEY_ID, config.BINANCE_SECRET_KEY)

def main(symbol: str, start_date: str, end_date: str, interval: Client, file_name: str) -> None:
    """Download data from binance to csv file."""
    
    candles = client.get_historical_klines(symbol=symbol, interval=interval, start_str=start_date, end_str=end_date)
    
    with open(f"{file_name}.csv", 'w', encoding='utf8', newline='') as f:
        thewriter = csv.writer(f)

        header = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", 
                  "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Can be ignored"]
        thewriter.writerow(header)
        
        for candlestick in candles:
            thewriter.writerow(candlestick)
        
            
if __name__ == "__main__":
    main(symbol = 'BTCUSDT', 
         start_date = "2020-01-01", 
         end_date = "2020-12-31", 
         interval = Client.KLINE_INTERVAL_1HOUR, 
         file_name = "BTC-data")
