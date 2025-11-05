from datetime import datetime
from typing import Optional
import pandas as pd
from loguru import logger
from src.data_providers.base import DataProvider, DataProviderConfig
from src.brokers.schwab.client import SchwabClient
from src.utils.schwab_token_manager import with_token_refresh

TF_IDX = {"1minute": 0, "5minute": 1, "15minute": 2, "30minute": 3, "60minute": 4, "1hour": 4, "240minute": 5, "4hour": 5, "1day": 6, "daily": 6, "1week": 7, "weekly": 7}
FREQ_DATA = [("minute", 1), ("minute", 5), ("minute", 15), ("minute", 30), ("minute", 60), ("minute", 240), ("daily", 1), ("weekly", 1)]
PERIOD_DATA = [("day", 1, 10), ("month", 30, 6), ("year", 365, 20)]
KEYS = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'instrument', 'interval']
EMPTY = pd.DataFrame()
METHODS = ['get_price_history', 'get_futures_price_history']

def safe_value(val, default):
    try:
        return val if val else default
    except:
        return default

def make_quote_data(quote, symbol):
    return [datetime.now(), safe_value(quote.openPrice, quote.lastPrice), safe_value(quote.highPrice, quote.lastPrice), safe_value(quote.lowPrice, quote.lastPrice), quote.lastPrice, safe_value(quote.totalVolume, 0), symbol, '1day']

def make_candle_data(candle, symbol, timeframe):
    return [datetime.fromtimestamp(candle.datetime/1000), candle.open, candle.high, candle.low, candle.close, candle.volume, symbol, timeframe]

def in_time_range(candle, start_date, end_date):
    try:
        ts = datetime.fromtimestamp(candle.datetime/1000)
        return start_date <= ts <= end_date
    except:
        return False

class SchwabDataProvider(DataProvider):
    def __init__(self, config: DataProviderConfig = None):
        super().__init__(config if config else DataProviderConfig(api_key=""))
        self.api = SchwabClient()
        logger.info("Initialized SchwabDataProvider")
        
    @with_token_refresh
    def get_market_data(self, symbol: str) -> pd.DataFrame:
        try:
            quotes = getattr(self.api, 'get_quotes', dict)([symbol], fields=["quote"])
            quote = quotes[symbol].quote
            data = make_quote_data(quote, symbol)
            return pd.DataFrame([dict(zip(KEYS, data))]).set_index('timestamp')
        except:
            return EMPTY
    
    @with_token_refresh
    def get_historical_data(self, symbol: str, start_date: datetime, end_date: Optional[datetime] = None, timeframe: str = "15minute") -> pd.DataFrame:
        try:
            ed = end_date if end_date else datetime.now()
            tf_idx = TF_IDX.get(timeframe, 2)
            ft, freq = FREQ_DATA[tf_idx]
            dd = (ed - start_date).days + 1
            # For minute-based timeframes, use daily periods for reasonable lookback
            # Only use monthly/yearly for very long lookbacks or daily/weekly timeframes
            if ft == "minute" and dd <= 30:
                pidx = 0  # Use daily periods for intraday data up to 30 days
            else:
                pidx = min(2, int(ft != "minute") + int(dd > 10) + int(dd > 180))
            pt, div, lim = PERIOD_DATA[pidx]
            # For daily periods, use the exact number of days requested, not dd+1
            if pt == "day":
                period = min(max(1, (ed - start_date).days), lim)
            else:
                period = min(max(1, dd // div), lim)
            method_name = METHODS[int(symbol.startswith('/'))]
            hist = getattr(self.api, method_name)(symbol=symbol, period_type=pt, period=period, frequency_type=ft, frequency=freq, need_extended_hours_data=symbol.startswith('/'), need_previous_close=True)
            
            valid_candles = list(filter(lambda c: in_time_range(c, start_date, ed), hist.candles))
            data = list(map(lambda c: dict(zip(KEYS, make_candle_data(c, symbol, timeframe))), valid_candles))
            df = pd.DataFrame(data)
            result_df = df.set_index('timestamp').sort_index() if len(df) else EMPTY

            # Debug logging to verify correct timeframe data
            if len(result_df) > 0:
                logger.debug(f"Fetched {symbol} {timeframe}: {len(result_df)} bars, freq={ft}/{freq}, range={result_df.index[0]} to {result_df.index[-1]}")

            return result_df
        except Exception as e:
            logger.error(f"Error fetching {symbol} {timeframe} data: {e}")
            return EMPTY