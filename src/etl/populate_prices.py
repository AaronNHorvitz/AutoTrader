# src/etl/populate_prices.py
import sqlite3
import logging
from pathlib import Path
from datetime import datetime, timedelta
from src.etl.utils import (
    connect_to_alpaca, fetch_alpaca_historical_data, 
    fetch_alpaca_yesterday_ohlc, fetch_alpaca_latest_bars
)
from credentials import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPAKA_ENDPOINT_URL

# Configure logging
# logging.basicConfig(
#     filename='logs/fetch.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# Database path
DB_DIR = Path('databases')
DB_PATH = DB_DIR / 'assets.db'

def ensure_prices_table_exists():
    """Check if asset_prices table exists and create it if missing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asset_prices (
            price_id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            adjusted_close REAL,
            volume INTEGER,
            fetched_at TEXT,
            FOREIGN KEY (asset_id) REFERENCES asset_metadata(asset_id)
        )
    """)
    conn.commit()
    conn.close()
    #logging.info("Ensured asset_prices table exists.")

def get_tickers_from_db():
    """Fetch tickers and asset_ids from asset_metadata."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT asset_id, symbol FROM asset_metadata WHERE is_active = 1")
    ticker_data = cursor.fetchall()
    conn.close()
    return {symbol: asset_id for asset_id, symbol in ticker_data}

def get_latest_date(ticker):
    """Get the most recent date for a ticker in asset_prices."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(date) 
        FROM asset_prices 
        WHERE asset_id = (SELECT asset_id FROM asset_metadata WHERE symbol = ?)
    """, (ticker,))
    latest_date = cursor.fetchone()[0]
    conn.close()
    return latest_date

def populate_historical_prices(alpaca_client, tickers_dict, start_date="2002-01-01"):
    """Populate historical OHLC data from 2002 to yesterday."""
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for ticker, asset_id in tickers_dict.items():
        latest_date = get_latest_date(ticker)
        fetch_start = start_date if not latest_date else latest_date
        
        if fetch_start >= end_date:
            #logging.info(f"Skipping {ticker}: already up to date.")
            continue
        
        #logging.info(f"Fetching historical data for {ticker} from {fetch_start} to {end_date}.")
        df = fetch_alpaca_historical_data(alpaca_client, [ticker], fetch_start, end_date)
        
        if not df.empty:
            fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT OR IGNORE INTO asset_prices (asset_id, date, open, high, low, close, fetched_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (asset_id, row['date'], row['open'], row['high'], row['low'], row['close'], fetched_at))
        
        conn.commit()
        #logging.info(f"Populated historical prices for {ticker}.")
    
    conn.close()

def update_latest_prices(alpaca_client, tickers_dict):
    """Update asset_prices with the latest bars from the most recent run."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    df = fetch_alpaca_latest_bars(alpaca_client, list(tickers_dict.keys()))
    if not df.empty:
        fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for _, row in df.iterrows():
            asset_id = tickers_dict.get(row['ticker'])
            cursor.execute("""
                INSERT OR REPLACE INTO asset_prices (asset_id, date, open, high, low, close, volume, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (asset_id, row['date'], row['open'], row['high'], row['low'], row['close'], row['volume'], fetched_at))
        
        conn.commit()
        #logging.info("Updated latest prices with fetch_alpaca_latest_bars.")
        print(f"Updated latest prices for {len(df)} tickers.")
    
    conn.close()

if __name__ == "__main__":
    alpaca = connect_to_alpaca(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPAKA_ENDPOINT_URL)
    if alpaca:
        ensure_prices_table_exists()
        tickers_dict = get_tickers_from_db()
        if not tickers_dict:
            #logging.warning("No tickers in asset_metadata. Run populate_tickers.py first.")
            print("No tickers found. Run populate_tickers.py first.")
        else:
            populate_historical_prices(alpaca, tickers_dict)
            update_latest_prices(alpaca, tickers_dict)

