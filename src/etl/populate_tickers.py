# src/etl/populate_tickers.py
import sqlite3
from datetime import datetime
from pathlib import Path

from src.utils.alpaca_utils import get_alpaca_client, fetch_alpaca_stock_tickers
from src.utils.db_utils import get_db_connection
from src.config import DB_DIR

# Explicitly define your absolute DB_DIR path
#DB_DIR = Path(r'd:\dev\stat_656_autotrader\databases')
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / 'assets.db'

def recreate_database():
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE asset_metadata (
            asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE,
            name TEXT,
            exchange TEXT,
            asset_type TEXT,
            is_active INTEGER,
            date_added TEXT,
            date_removed TEXT,
            fetched_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def populate_tickers():
    alpaca_client = get_alpaca_client()
    assets = alpaca_client.list_assets()  # Correct method for alpaca-trade-api

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for asset in assets:
        if asset.exchange in ['NASDAQ', 'NYSE', 'AMEX'] and asset.tradable and asset.symbol.isalpha():
            query_string = """
                INSERT OR IGNORE INTO asset_metadata (
                    symbol, name, exchange, asset_type, is_active, date_added, fetched_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query_string, (
                asset.symbol,
                asset.name,
                asset.exchange,
                getattr(asset, 'class'),  # Fixed: Use getattr() to access 'class' safely
                1 if asset.status == 'active' else 0,
                date_now.split()[0],
                date_now
            ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    recreate_database()
    populate_tickers()