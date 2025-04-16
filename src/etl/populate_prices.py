# src/etl/populate_prices.py
import sqlite3
from datetime import datetime, timedelta
from src.utils.db_utils import fetch_active_tickers
from src.utils.alpaca_utils import get_alpaca_client, populate_alpaca_full_history
from src.config import DB_DIR

DB_PATH = DB_DIR / 'assets.db'



def populate_prices():
    # Get tickers and Alpaca client
    tickers_dict = fetch_active_tickers()
    tickers = list(tickers_dict.keys())
    alpaca_client = get_alpaca_client()

    # Set end date to yesterday
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Populate price history, inserting as fetched
    populate_alpaca_full_history(alpaca_client=alpaca_client, tickers=tickers, end_date=end_date)

if __name__ == "__main__":
    populate_prices()