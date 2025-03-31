# src/utils/db_utils.py
import sqlite3
import pandas as pd
from pathlib import Path
from config import DB_DIR

def get_db_connection(db_name='assets.db'):
    db_path = Path(DB_DIR) / db_name
    print(f"Connecting to database: {db_path}")  # Debug: Show the path
    return sqlite3.connect(db_path)

def fetch_active_tickers():
    conn = get_db_connection()
    df = pd.read_sql("SELECT asset_id, symbol FROM asset_metadata WHERE is_active = 1", conn)
    conn.close()
    return df.set_index('symbol')['asset_id'].to_dict()

def get_latest_price_date(symbol):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(date) FROM asset_prices
        WHERE asset_id = (SELECT asset_id FROM asset_metadata WHERE symbol = ?)
    """, (symbol,))
    date = cur.fetchone()[0]
    conn.close()
    return date

def fetch_all_asset_metadata():
    """
    Fetch all asset metadata from the asset_metadata table.
    Returns:
        pd.DataFrame: DataFrame containing all asset metadata.
    """
    conn = get_db_connection()
    # Debug: Check raw data
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM asset_metadata")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    print("Raw rows fetched:", rows[:5])  # Show first 5 rows
    print("Column names from DB:", columns)  # Show actual columns
    df = pd.read_sql("SELECT * FROM asset_metadata", conn)
    conn.close()
    return df

def fetch_all_asset_prices():
    """
    Fetch all historical prices from the asset_prices table.
    Returns:
        pd.DataFrame: DataFrame containing all price data with joined symbol info.
    """
    conn = get_db_connection()
    query = """
        SELECT ap.price_id, ap.asset_id, am.symbol, ap.date, ap.open, ap.high, 
               ap.low, ap.close, ap.adjusted_close, ap.volume, ap.fetched_at
        FROM asset_prices ap
        LEFT JOIN asset_metadata am ON ap.asset_id = am.asset_id
        ORDER BY ap.date ASC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df