# src/etl/populate_tickers.py

# TODO: Update database incrementally ()
# - Fetch existing tickers ( compare with new fetch )
# - Add new tickers ( date_added )
# - Flag delisted ( is_active=0, date_removed )
# - Log changes ( db_change_log.db )

import sqlite3
from pathlib import Path
from datetime import datetime
from src.etl.utils import connect_to_alpaca, fetch_alpaca_stock_tickers
from credentials import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPAKA_ENDPOINT_URL

# Database path
DB_DIR = Path('databases')
DB_PATH = DB_DIR / 'assets.db'

def recreate_database():
    """Recreate assets.db with a fresh asset_metadata table."""
    DB_DIR.mkdir(exist_ok=True)
    # Delete existing database if it exists
    if DB_PATH.exists():
        DB_PATH.unlink()  # Nuke the database ()
    
    # Create new database and table00
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asset_metadata (
            asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE,
            name TEXT,
            exchange TEXT,
            asset_type TEXT,
            sector TEXT,
            industry TEXT,
            currency TEXT,
            has_dividend INTEGER,
            is_active INTEGER,
            date_added TEXT,
            date_removed TEXT,
            fetched_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    print(f"Recreated {DB_PATH} with fresh asset_metadata table.")

def populate_tickers(alpaca_client):
    """Populate asset_metadata with all NYSE, NASDAQ, AMEX tickers."""
    # Fetch all tickers ( no limit )
    tickers = fetch_alpaca_stock_tickers(alpaca_client, exchanges=['NYSE', 'NASDAQ', 'AMEX'])
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Insert all tickers
    date_added = datetime.now().strftime("%Y-%m-%d")
    fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_count = 0
    
    for ticker in tickers:
        try:
            cursor.execute("""
                INSERT INTO asset_metadata (symbol, exchange, asset_type, is_active, date_added, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ticker, 'UNKNOWN', 'Stock', 1, date_added, fetched_at))
            new_count += 1
        except sqlite3.Error as e:
            pass  # Silently skip errors ( e.g., duplicates )
    
    conn.commit()
    conn.close()
    print(f"Populated {new_count} tickers into asset_metadata.")



if __name__ == "__main__":
    alpaca = connect_to_alpaca(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPAKA_ENDPOINT_URL)
    if alpaca:
        recreate_database()
        populate_tickers(alpaca)