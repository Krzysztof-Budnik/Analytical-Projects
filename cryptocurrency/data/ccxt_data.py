import ccxt
import csv


def main(symbol: str, timeframe: str, since: str, limit: int, file_name: str) -> None:
    """Downloads data from binance to csv file with ccxt.
    Best for most recent candels."""
    
    exchange = ccxt.binance()

    ohlc = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=since, limit=limit)
    
    with open(f"{file_name}.csv", 'w', encoding='utf8', newline='') as f:
            thewriter = csv.writer(f)

            header = ["Open time", "Open", "High", "Low", "Close", "Volume"]
            thewriter.writerow(header)

            for candle in ohlc:
                thewriter.writerow(candle)
        
            
if __name__ == "__main__":
    main(symbol = 'BTCUSDT', 
         timeframe = "1h",
         since = None,  
         limit=500,
         file_name = "TEST-ccxt-btcc")