#src/etl/utils.py

import sys
import time
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
from alpaca_trade_api.rest import REST
import logging

# Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

def connect_to_alpaca(api_key, secret_key, base_url):
    """
    Initialize and test connection to Alpaca API.
    
    Args:
        api_key (str): Alpaca API key.
        secret_key (str): Alpaca secret key.
        base_url (str): Alpaca API endpoint URL.
    
    Returns:
        REST: Alpaca REST client instance if successful, None if failed.
    """
    try:
        alpaca = REST(api_key, secret_key, base_url=base_url)
        #logging.info("Connected to Alpaca successfully!")
        #print("Connected to Alpaca successfully!")
        return alpaca
    except Exception as e:
        #logging.error(f"Connection failed: {e}")
        #print(f"Connection failed: {e}")
        return None

def fetch_alpaca_stock_tickers(alpaca_client, exchanges=['NASDAQ', 'NYSE', 'AMEX']):
    """
    Fetch list of active, tradable stock tickers from Alpaca for specified U.S. exchanges.
    
    Args:
        alpaca_client (REST): Initialized Alpaca REST client.
        exchanges (list): List of U.S. exchanges to filter (default: ['NASDAQ', 'NYSE', 'AMEX']).
    
    Returns:
        list: Filtered list of stock tickers (uppercase, alpha-only).
    """
    try:
        assets = alpaca_client.list_assets(status='active')
        stock_assets = [
            asset for asset in assets
            if asset.exchange in exchanges
            and asset.tradable
            and asset.status == 'active'
            and asset.symbol.isalpha()
            and asset.symbol.isupper()
        ]
        stock_tickers = [asset.symbol for asset in stock_assets]
        #logging.info(f"Fetched {len(stock_tickers)} company stock tickers from Alpaca.")
        #print(f"Fetched {len(stock_tickers)} company stock tickers from Alpaca (U.S. exchanges, no CUSIPs/ETFs/SPACs)!")
        #print("First 20 company stock tickers:", stock_tickers[:20])
        return stock_tickers
    except Exception as e:
        #logging.error(f"Error fetching tickers: {e}")
        #print(f"Error fetching tickers: {e}")
        return []

def fetch_alpaca_historical_data(alpaca_client, tickers, start_date, end_date, years_back=5):
    """
    Fetch historical OHLC data from Alpaca for a list of tickers.
    
    Args:
        alpaca_client (REST): Initialized Alpaca REST client.
        tickers (list): List of stock tickers to fetch.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        years_back (int): Number of years for threshold (default: 5).
    
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
                #logging.warning(f"No data for {ticker}")
                #print(f"No data for {ticker}")
            
            time.sleep(1)  # Avoid rate limiting
        except Exception as e:
            #logging.error(f"Error for {ticker}: {e}")
            #print(f"Error for {ticker}: {e}")
            time.sleep(1)

    total_seconds = time.time() - start_time
    seconds_per_ticker = round(total_seconds / len(tickers), 2)
    #logging.info(f"Fetched {len(alpaca_df)} rows in {total_seconds:.2f} seconds.")
    ##print(f"\nFetched {len(alpaca_df)} rows of stock data in {total_seconds:.2f} seconds.")
    ##print(f"Processed {processed_ticker_count} tickers, missing {missing_data_count} tickers, "
    #      f"{not_enough_time_count} tickers did not have enough time.")
    ##print(f"Processing time per ticker: {seconds_per_ticker:.2f} seconds.")
    return alpaca_df

def fetch_alpaca_yesterday_ohlc(alpaca_client, tickers):
    """
    Fetch yesterday's OHLC data for a list of tickers from Alpaca.
    
    Args:
        alpaca_client (REST): Initialized Alpaca REST client.
        tickers (list): List of stock tickers to fetch.
    
    Returns:
        pd.DataFrame: OHLC data for yesterday.
    """
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    start_time = time.time()
    daily_df = pd.DataFrame()

    for ticker in tqdm(tickers, desc="Fetching Yesterday's OHLC"):
        try:
            bars = alpaca_client.get_bars(ticker, "1Day", yesterday, yesterday).df
            if not bars.empty:
                bars.reset_index(inplace=True)
                ohlc = bars[['timestamp', 'open', 'high', 'low', 'close']]
                ohlc['ticker'] = ticker
                ohlc['date'] = ohlc['timestamp'].dt.strftime("%Y-%m-%d")
                daily_df = pd.concat([daily_df, ohlc[['ticker', 'date', 'open', 'high', 'low', 'close']]])
            time.sleep(1)
        except Exception as e:
            #logging.error(f"Error fetching {ticker}: {e}")
            ##print(f"Error fetching {ticker}: {e}")
            time.sleep(1)

    fetch_time = time.time() - start_time
    seconds_per_ticker = round(fetch_time / len(tickers), 2)
    #logging.info(f"Fetched OHLC for {yesterday} in {fetch_time:.2f} seconds.")
    ##print(f"\nFetched OHLC data for yesterday ({yesterday}) in {fetch_time:.2f} seconds.")
    ##print(f"Average processing time per ticker: {seconds_per_ticker:.2f} seconds.")
    return daily_df

def fetch_alpaca_open_prices(alpaca_client, tickers):
    """
    Fetch today's opening prices at market open (9:30 AM EST/EDT) for a list of tickers.
    
    Args:
        alpaca_client (REST): Initialized Alpaca REST client.
        tickers (list): List of stock tickers to fetch.
    
    Returns:
        pd.DataFrame: Opening prices at market open.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    market_open = f"{today}T09:30:00-05:00"
    market_open_dt = pd.Timestamp(market_open)
    start_time = time.time()
    open_prices_df = pd.DataFrame()

    for ticker in tqdm(tickers, desc="Fetching Today's Open Prices"):
        try:
            bars = alpaca_client.get_bars(
                ticker, "1Min", market_open_dt.isoformat(), 
                (market_open_dt + timedelta(minutes=1)).isoformat()
            ).df
            if not bars.empty:
                bars.reset_index(inplace=True)
                open_price = bars.iloc[0]['open']
                open_prices_df = pd.concat([
                    open_prices_df,
                    pd.DataFrame({'ticker': [ticker], 'date': [today], 'open': [open_price]})
                ])
            time.sleep(1)
        except Exception as e:
            #logging.error(f"Error fetching {ticker}: {e}")
            ##print(f"Error fetching {ticker}: {e}")
            time.sleep(1)

    fetch_time = time.time() - start_time
    seconds_per_ticker = round(fetch_time / len(tickers), 2)
    #logging.info(f"Fetched open prices for {today} in {fetch_time:.2f} seconds.")
    ##print(f"\nFetched today's open prices ({today}) in {fetch_time:.2f} seconds.")
    ##print(f"Average processing time per ticker: {seconds_per_ticker:.2f} seconds.")
    return open_prices_df

def fetch_alpaca_latest_bars(alpaca_client, tickers):
    """
    Fetch latest bars (real-time OHLC) for a list of tickers in batch from Alpaca.
    
    Args:
        alpaca_client (REST): Initialized Alpaca REST client.
        tickers (list): List of stock tickers to fetch.
    
    Returns:
        pd.DataFrame: Latest OHLC data for all tickers.
    """
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
            }
            for ticker, bar in bars.items()
        ]
        real_time_df = pd.DataFrame(data)
        #logging.info("Fetched latest bars successfully.")
        ##print("Real-Time Opening Prices (Market Open):")
        return real_time_df
    except Exception as e:
        #logging.error(f"Error fetching real-time data: {e}")
        ##print(f"Error fetching real-time data: {e}")
        return pd.DataFrame()