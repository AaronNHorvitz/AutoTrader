# src/utils/alpaca_utils.py

import time
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
from alpaca_trade_api.rest import REST
from credentials import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPAKA_ENDPOINT_URL
from src.utils.db_utils import get_db_connection, fetch_active_tickers

def get_alpaca_client():
    return REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPAKA_ENDPOINT_URL)

def connect_to_alpaca(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPAKA_ENDPOINT_URL):
    try:
        return REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPAKA_ENDPOINT_URL)
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


import pandas as pd
import time
from tqdm import tqdm
from datetime import datetime

def populate_alpaca_full_price_history(alpaca_client, tickers, end_date=None):
    """
    Populate full historical OHLC data from Alpaca for a list of tickers,
    fetching data as far back as possible until the specified end date.

    Args:
        alpaca_client (REST): Initialized Alpaca REST client.
        tickers (list): List of stock tickers to fetch.
        end_date (str, optional): End date in 'YYYY-MM-DD' format. Defaults to today's date.

    Returns:
        pd.DataFrame: Combined OHLC data for all tickers.
    """
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    alpaca_df = pd.DataFrame()
    start_time = time.time()
    missing_data_count = 0
    processed_ticker_count = 0

    for ticker in tqdm(tickers, desc="Alpaca Download Progress"):
        try:
            processed_ticker_count += 1
            bars = alpaca_client.get_bars(ticker, "1Day", "1900-01-01", end_date).df

            if not bars.empty:
                df = bars[['open', 'high', 'low', 'close']].reset_index()
                df['ticker'] = ticker
                df['date'] = df['timestamp'].dt.strftime("%Y-%m-%d")
                df = df[['ticker', 'date', 'open', 'high', 'low', 'close']]
                alpaca_df = pd.concat([alpaca_df, df], ignore_index=True)
            else:
                missing_data_count += 1

            time.sleep(1)  # Avoid rate limiting
            
        except Exception as e:
            print(f"Error for {ticker}: {e}")
            missing_data_count += 1
            time.sleep(1)

    total_seconds = time.time() - start_time
    seconds_per_ticker = round(total_seconds / len(tickers), 2)
    print(f"\nFetched {len(alpaca_df)} rows of stock data in {total_seconds:.2f} seconds.")
    print(f"Processed {processed_ticker_count} tickers, missing data for {missing_data_count} tickers.")
    print(f"Processing time per ticker: {seconds_per_ticker:.2f} seconds.")
    return alpaca_df



def update_stock_prices(db_path="assets.db"):
    """
    Queries the database for the last stock fetch and update times, then updates with latest prices.
    
    Args:
        db_path (str): Path to assets.db. Defaults to "assets.db".
    
    Returns:
        dict: Last fetch/update times and status of the update process.
    """
    result = {
        "last_fetch_time": None,
        "last_update_date": None,
        "new_records_added": 0,
        "status": "No updates performed"
    }
    
    try:
        # Connect to database and get active stock tickers
        conn = get_db_connection(db_name=db_path)
        cursor = conn.cursor()
        ticker_to_asset_id = fetch_active_tickers()  # {symbol: asset_id}
        tickers = list(ticker_to_asset_id.keys())
        if not tickers:
            result["status"] = "No active stock tickers found"
            conn.close()
            return result
        
        # Query last fetch time from asset_prices
        cursor.execute("""
            SELECT MAX(fetched_at)
            FROM asset_prices
            WHERE asset_id IN (
                SELECT asset_id FROM asset_metadata WHERE asset_type = 'Stock' AND is_active = 1
            ) AND fetched_at IS NOT NULL
        """)
        last_fetch = cursor.fetchone()[0]
        result["last_fetch_time"] = last_fetch if last_fetch else "Never fetched"
        
        # Query last update date (latest trading date in asset_prices)
        cursor.execute("""
            SELECT MAX(date)
            FROM asset_prices
            WHERE asset_id IN (
                SELECT asset_id FROM asset_metadata WHERE asset_type = 'Stock' AND is_active = 1
            ) AND date IS NOT NULL
        """)
        last_date = cursor.fetchone()[0]
        result["last_update_date"] = last_date if last_date else "No price data"
        
        # Fetch latest bars from Alpaca if we have a baseline
        if last_date or last_fetch:
            alpaca_client = get_alpaca_client()
            latest_bars_df = fetch_alpaca_latest_bars(alpaca_client, tickers)
            
            if not latest_bars_df.empty:
                # Add asset_id and fetched_at
                latest_bars_df['asset_id'] = latest_bars_df['ticker'].map(ticker_to_asset_id)
                latest_bars_df['fetched_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                latest_bars_df['adjusted_close'] = latest_bars_df['close']  # No adjustment for latest
                
                # Filter for new data
                if last_date:
                    latest_bars_df = latest_bars_df[latest_bars_df['date'] > last_date]
                
                if not latest_bars_df.empty:
                    # Insert new records
                    for _, row in latest_bars_df.iterrows():
                        cursor.execute("""
                            INSERT INTO asset_prices (
                                asset_id, date, open, high, low, close, adjusted_close, volume, fetched_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            row['asset_id'], row['date'], row['open'], row['high'], row['low'],
                            row['close'], row['adjusted_close'], row['volume'], row['fetched_at']
                        ))
                    result["new_records_added"] = len(latest_bars_df)
                    result["status"] = f"Added {result['new_records_added']} new price records"
                    conn.commit()
                else:
                    result["status"] = "No new data to add (all data up to date)"
            else:
                result["status"] = "Failed to fetch latest bars from Alpaca"
        
        conn.close()
        
    except Exception as e:
        result["status"] = f"Error: {e}"
        print(result["status"])
    
    return result

# Example usage
if __name__ == "__main__":
    update_result = update_stock_prices()
    print("Stock Price Update Report:")
    print(f"Last Fetch Time: {update_result['last_fetch_time']}")
    print(f"Last Update Date: {update_result['last_update_date']}")
    print(f"New Records Added: {update_result['new_records_added']}")
    print(f"Status: {update_result['status']}")
    