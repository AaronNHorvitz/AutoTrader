# src/etl/update_prices.py
from datetime import datetime, timedelta
from src.utils.db_utils import fetch_active_tickers, get_latest_price_date, get_db_connection
from src.utils.alpaca_utils import get_alpaca_client, fetch_alpaca_historical_data
from src.config import DB_DIR

DB_PATH = DB_DIR / 'assets.db'

def update_daily_prices():
    alpaca = get_alpaca_client()
    tickers_dict = fetch_active_tickers()
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    conn = get_db_connection()
    cursor = conn.cursor()

    for symbol, asset_id in tickers_dict.items():
        latest_date = get_latest_price_date(symbol)
        start_date = (datetime.strptime(latest_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') if latest_date else '2002-01-01'
        if start_date >= end_date:
            continue
        df = fetch_alpaca_historical_data(alpaca, [symbol], start_date, end_date)
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT OR IGNORE INTO asset_prices (asset_id, date, open, high, low, close, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (asset_id, row['date'], row['open'], row['high'], row['low'], row['close'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
    conn.close()

if __name__ == "__main__":
    update_daily_prices()
