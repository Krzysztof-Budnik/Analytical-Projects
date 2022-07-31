# exchange conection
import ccxt

# csv handling
from csv import writer

# data handling
import pandas as pd

# technical analysis indicators
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import SMAIndicator


class TradingData():
    exchange = ccxt.binance()
    
    def __init__(self, symbols: list[str], timeframe: str, limit: str) -> None:
        """Downloading data based on three main parameters: list of symbols, 
        candlestick timeframe and limit (amount of records). self.pairs represent coins 
        saved in format coin-stablecoin so that they can be used in file names"""
        
        self.symbols = symbols
        self.timeframe = timeframe
        self.limit = limit
        self.pairs = [coin.replace("/", "-") for coin in self.symbols]
    
    def __repr__(self) -> str:
        return f'TradingData \nsymbols: {self.symbols} \ntimeframe: {self.timeframe} \
    \nlimit: {self.limit}'
      
    def download_to_csv(self, since=None) -> None:
        """Downloads data from binance to csv file. For each coin separate csv 
        file is generated."""
    
        for coin, pair in zip(self.symbols, self.pairs):
            ohlc = self.exchange.fetch_ohlcv(symbol = coin, 
                                        timeframe = self.timeframe, 
                                        since = since, 
                                        limit = self.limit)
        
            with open(f"{pair}_{self.timeframe}.csv", 'w', encoding='utf8', newline='') as f:
                    thewriter = writer(f)
                    
                    header = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
                    thewriter.writerow(header)
                    
                    for candle in ohlc[:-1]:
                        thewriter.writerow(candle)
                           
    def update_csv_data(self) -> None:
        """Updates csv files with most recent records."""

        file_to_check = f"BTC-BUSD_{self.timeframe}.csv"
        
        df = pd.read_csv(file_to_check)
        last_record = df['timestamp'].iloc[-1]

        for coin, pair in zip(self.symbols, self.pairs):
            ohlc = self.exchange.fetch_ohlcv(symbol = coin, 
                                        timeframe = self.timeframe, 
                                        since = last_record)
            
            with open(f"{pair}_{self.timeframe}.csv", 'a+', encoding='utf8', newline='') as f:
                    thewriter = writer(f)

                    for candle in ohlc[1:-1]:
                        thewriter.writerow(candle)
    
    def create_dataframes(self) -> dict[str: pd.DataFrame]:
        """For each pair specified in TradingData instance there is dataframe created and 
        saved in dictionary format"""
        
        coin_df_dictionary = {pair: pd.read_csv(f"{pair}_{self.timeframe}.csv") for pair in self.pairs}
        return coin_df_dictionary
    


class IndicatorData():
    """Applying indicators to dataframes"""
    
    def __init__(self, coin_dataframes: dict[str: pd.DataFrame]) -> None:
        """Main argument: coin_dataframes dictionary containing dataframes with 
        price data about all analysed cryptocurrencies."""
        
        self.coin_dataframes = coin_dataframes
        self.symbols = list(self.coin_dataframes.keys())
        self.dataframes = list(self.coin_dataframes.values())
              
    def __getitem__(self, key) -> pd.DataFrame:
        return self.coin_dataframes[key]
    
    def __len__(self) -> int:
        return len(self.coin_dataframes)
    
    def __repr__(self) -> str:
        symbol_lst = [i for i in self.symbols]
        return f'ExtendedData \nsymbols: {symbol_lst}'
    
    
    ### Managing dataframes ### 
    
    def drop_all_indicators(self) -> None:
        """Drop all indicator columns."""
        
        for df in self.dataframes:
            df.drop(df.iloc[:, 6:], axis = 1, inplace = True)
            
    def drop_all_main_data(self) -> None:
        """Drop all indicator columns."""
        
        for df in self.coin_dataframes.values():
            df.drop(df.iloc[:, :7], axis = 1, inplace = True)
            
    def drop_columns_by_name(self, columns: list[str]) -> None:
        """Allows dropping specific indicator columns."""
        
        for df in self.coin_dataframes.values():
            df.drop(df.columns[columns], axis = 1, inplace = True)
    
    def drop_columns_by_index(self, index_list: list[int]) -> None:
        """Allows dropping specific indicator columns."""
        
        for df in self.coin_dataframes.values():
            df.drop(df.columns[index_list], axis = 1, inplace = True)    
                  
    def format_time(self) -> None:
        """Method changes unix timestamp into datetime object."""
        
        for df in self.coin_dataframes.values():
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            
    def columns(self) -> list:
        return list(list(self.coin_dataframes.values())[0].columns)
    
    
    ### Methods for Indicator calculations ###
    
    def apply_bollinger_bands(self, window: int) -> None:
        """Adds bollinger band indicator values to all coin dataframes provided."""
        
        for df in self.coin_dataframes.values():
            bb_indicator = BollingerBands(df['close'], window=window)
            
            df['upper_band'] = bb_indicator.bollinger_hband()
            df['lower_band'] = bb_indicator.bollinger_lband()
            df['bb_moving_average'] = bb_indicator.bollinger_mavg()
    
    def apply_atr(self) -> None:
        """Apply average true range."""
        
        for df in self.coin_dataframes.values():
            atr_indicator = AverageTrueRange(df['high'], df['low'], df['close'])
            df['atr'] = atr_indicator.average_true_range()

    def apply_simple_ma(self, window_list: list[int]) -> None:
        """Apply SMA. Since interval is passed as list of integers,
        there is a possibility to create multiple sma at once."""
        
        for df in self.coin_dataframes.values():
            for i in window_list:
                atr_indicator = SMAIndicator(df['close'], window=i)
                df[f'sma_{i}d'] = atr_indicator.sma_indicator()
        
    def test_boolean(self, param_name: str):
         for df in self.coin_dataframes.values():
             df[param_name] = True
    
    
##### FUNCTIONS #####    
    
def indicator_data_info(indicator_data: IndicatorData) -> dict:
    """Returns inforamtion about IndicatorData"""
    
    result = {"pairs": len(indicator_data), 
              "records per dataframe": len(indicator_data.dataframes[0])}
    return result