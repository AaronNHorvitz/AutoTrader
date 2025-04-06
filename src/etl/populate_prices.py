# src/etl/populate_prices.py
import sqlite3
from datetime import datetime, timedelta
from tqdm import tqdm  
from src.utils.db_utils import fetch_active_tickers
from src.utils.alpaca_utils import get_alpaca_client, fetch_alpaca_historical_data
from src.config import DB_DIR

DB_PATH = DB_DIR / 'assets.db'

def ensure_prices_table():
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
            FOREIGN KEY(asset_id) REFERENCES asset_metadata(asset_id)
        )
    """)
    conn.commit()
    conn.close()

def populate_prices():
    alpaca_client = get_alpaca_client()
    tickers_dict = fetch_active_tickers()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = "2002-01-01"
    tickers = list(tickers_dict.keys())

    # Fetch historical data once for all tickers
    historical_df = fetch_alpaca_historical_data(alpaca_client, tickers, start_date, end_date)

    # Insert data into DB
    for _, row in tqdm(historical_df.iterrows(), total=len(historical_df), desc="Inserting Prices into DB"):
        asset_id = tickers_dict.get(row['ticker'])
        cursor.execute("""
            INSERT OR IGNORE INTO asset_prices (asset_id, date, open, high, low, close, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            asset_id,
            row['date'],
            row['open'],
            row['high'],
            row['low'],
            row['close'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    ensure_prices_table()
    populate_prices()