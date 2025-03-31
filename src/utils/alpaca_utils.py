# src/utils/alpaca_utils.py

import time
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
from alpaca_trade_api.rest import REST
from credentials import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPAKA_ENDPOINT_URL

def get_alpaca_client():
    return REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPAKA_ENDPOINT_URL)

def connect_to_alpaca(api_key, secret_key, base_url):
    try:
        return REST(api_key, secret_key, base_url=base_url)
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def fetch_alpaca_stock_tickers(alpaca_client, exchanges=['NASDAQ', 'NYSE', 'AMEX']):
    try:
        assets = alpaca_client.list_assets(status='active')
        stock_assets = [
            asset.symbol for asset in assets
            if asset.exchange in exchanges and asset.tradable
            and asset.symbol.isalpha() and asset.symbol.isupper()
        ]
        return stock_assets
    except Exception as e:
        print(f"Error fetching tickers: {e}")
        return []

def fetch_alpaca_historical_data(alpaca_client, tickers, start_date, end_date, years_back=5):
    """
    Fetch historical OHLC data from Alpaca for a list of tickers.
    
    Args:
        alpaca_client (REST): Initialized Alpaca REST client.
        tickers (list): List of stock tickers to fetch.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        years_back (int): Number of years of data required (default: 5).
    
    Returns:
        pd.DataFrame: Combined OHLC data for all tickers.
    """
    alpaca_df = pd.DataFrame()
    start_time = time.time()
    missing_data_count = 0
    not_enough_time_count = 0
    processed_ticker_count = 0
    trading_days_back = years_back * 252  # Approx trading days/year

    for ticker in tqdm(tickers, desc="Alpaca Download Progress"):
        try:
            processed_ticker_count += 1
            bars = alpaca_client.get_bars(ticker, "1Day", start_date, end_date).df
            
            if not bars.empty:
                df = bars[['open', 'high', 'low', 'close']].reset_index()
                if len(df) < trading_days_back:
                    missing_data_count += 1
                    not_enough_time_count += 1
                    continue
                
                df['ticker'] = ticker
                df['date'] = df['timestamp'].dt.strftime("%Y-%m-%d")
                df = df[['ticker', 'date', 'open', 'high', 'low', 'close']]
                alpaca_df = pd.concat([alpaca_df, df])
            else:
                missing_data_count += 1
            
            time.sleep(1)  # Avoid rate limiting
        except Exception as e:
            print(f"Error for {ticker}: {e}")
            time.sleep(1)

    total_seconds = time.time() - start_time
    seconds_per_ticker = round(total_seconds / len(tickers), 2)
    print(f"\nFetched {len(alpaca_df)} rows of stock data in {total_seconds:.2f} seconds.")
    print(f"Processed {processed_ticker_count} tickers, missing {missing_data_count} tickers, "
          f"{not_enough_time_count} tickers did not have enough time.")
    print(f"Processing time per ticker: {seconds_per_ticker:.2f} seconds.")
    return alpaca_df


def fetch_alpaca_yesterday_ohlc(alpaca_client, tickers):
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    daily_df = pd.DataFrame()

    for ticker in tqdm(tickers, desc="Yesterday OHLC"):
        try:
            bars = alpaca_client.get_bars(ticker, "1Day", yesterday, yesterday).df
            if not bars.empty:
                bars.reset_index(inplace=True)
                ohlc = bars[['timestamp', 'open', 'high', 'low', 'close']]
                ohlc['ticker'] = ticker
                ohlc['date'] = yesterday
                daily_df = pd.concat([daily_df, ohlc[['ticker', 'date', 'open', 'high', 'low', 'close']]])
            time.sleep(0.5)
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            time.sleep(1)

    return daily_df

def fetch_alpaca_open_prices(alpaca_client, tickers):
    today = datetime.now().strftime("%Y-%m-%d")
    market_open_dt = pd.Timestamp(f"{today}T09:30:00-05:00")
    open_prices_df = pd.DataFrame()

    for ticker in tqdm(tickers, desc="Open Prices"):
        try:
            bars = alpaca_client.get_bars(ticker, "1Min", market_open_dt.isoformat(), (market_open_dt + timedelta(minutes=1)).isoformat()).df
            if not bars.empty:
                open_price = bars.iloc[0]['open']
                open_prices_df = pd.concat([
                    open_prices_df,
                    pd.DataFrame({'ticker': [ticker], 'date': [today], 'open': [open_price]})
                ])
            time.sleep(0.5)
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            time.sleep(1)

    return open_prices_df

def fetch_alpaca_latest_bars(alpaca_client, tickers):
    try:
        bars = alpaca_client.get_latest_bars(tickers)
        data = [
            {
                'ticker': ticker,
                'date': bar.t.strftime("%Y-%m-%d"),
                'open': bar.o,
                'high': bar.h,
                'low': bar.l,
                'close': bar.c,
                'volume': bar.v
            } for ticker, bar in bars.items()
        ]
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error fetching latest bars: {e}")
        return pd.DataFrame()
