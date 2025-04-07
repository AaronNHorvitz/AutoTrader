# src/utils/db_utils.py
import sqlite3
import pandas as pd
from pathlib import Path
from src.config import DB_DIR

def get_db_connection(db_name='assets.db', print_statements=True):
    db_path = Path(DB_DIR) / db_name
    if print_statements:
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

def last_data_date(print_statements=False):
    """Retrieve the most recent date from the 'date' column in the asset_prices table.

    This function queries the SQLite database 'assets.db' to find the maximum value
    in the 'date' column of the 'asset_prices' table and returns it as a Python
    datetime.date object.

    Parameters
    ----------
    print_statements : bool, optional
        If True, print SQL connection and query statements for debugging purposes.
        Default is False.

    Returns
    -------
    datetime.date
        The most recent date from the 'date' column, as a datetime.date object
        (e.g., datetime.date(2025, 3, 28)).

    Raises
    ------
    ValueError
        If the date string retrieved from the database cannot be parsed into a valid date.
    sqlite3.Error
        If there is an issue with the database connection or query execution.

    Examples
    --------
    >>> from db_utils import last_data_date
    >>> date = last_data_date(print_statements=True)
    >>> print(date)
    2025-03-28
    """
    # Database Connection
    conn = get_db_connection('assets.db', print_statements=print_statements)
    cursor = conn.cursor()
    
    # Find most recent date
    cursor.execute("""
        SELECT MAX(date)
        FROM asset_prices
        """)
    most_recent_date = cursor.fetchone()[0]
    conn.close()
    
    # Convert string to datetime using date-only format
    dt = datetime.strptime(most_recent_date, '%Y-%m-%d')
    date_only = dt.date()
    
    return date_only

def last_fetch_date(print_statements=False):
    """Retrieve the most recent fetch date from the 'fetched_at' column in the asset_prices table.

    This function queries the SQLite database 'assets.db' to find the maximum value
    in the 'fetched_at' column of the 'asset_prices' table, which represents the
    timestamp when data was last fetched, and returns the date portion as a Python
    datetime.date object.

    Parameters
    ----------
    print_statements : bool, optional
        If True, print SQL connection and query statements for debugging purposes.
        Default is False.

    Returns
    -------
    datetime.date
        The date portion of the most recent 'fetched_at' timestamp, as a datetime.date
        object (e.g., datetime.date(2025, 3, 28)).

    Raises
    ------
    ValueError
        If the datetime string retrieved from the database cannot be parsed into a valid datetime.
    sqlite3.Error
        If there is an issue with the database connection or query execution.

    Examples
    --------
    >>> from db_utils import last_fetch_date
    >>> fetch_date = last_fetch_date(print_statements=True)
    >>> print(fetch_date)
    2025-03-28
    """
    # Database Connection
    conn = get_db_connection('assets.db', print_statements=print_statements)
    cursor = conn.cursor()

    # Find most recent fetched_at datetime
    cursor.execute("""
        SELECT MAX(fetched_at)
        FROM asset_prices
        """)
    most_recent_fetch_date = cursor.fetchone()[0]
    conn.close()

    # Convert string to datetime and extract date
    dt = datetime.strptime(most_recent_fetch_date, '%Y-%m-%d %H:%M:%S')
    date_only = dt.date()
    
    return date_only

