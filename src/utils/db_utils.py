# src/utils/db_utils.py
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import os 
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

def fetch_database_stock_tickers():
    """Retrieve a list of stock ticker symbols from the asset_metadata table.

    This function queries the SQLite database 'assets.db' to extract all values
    from the 'symbol' column in the 'asset_metadata' table and returns them as
    a Python list.

    Returns
    -------
    list
        A list of strings representing stock ticker symbols (e.g., ['AAPL', 'GOOGL', 'TSLA']).

    Raises
    ------
    sqlite3.Error
        If there is an issue with the database connection or query execution.
    KeyError
        If the 'symbol' column is not present in the query result.

    Examples
    --------
    >>> from db_utils import fetch_database_stock_tickers
    >>> tickers = fetch_database_stock_tickers()
    >>> print(tickers)
    ['AAPL', 'GOOGL', 'TSLA']
    """
    conn = get_db_connection('assets.db', print_statements=False)
    query = """
    SELECT symbol FROM asset_metadata
    """
    past_ticker_list = pd.read_sql(query, conn)['symbol'].to_list()
    conn.close()
    return past_ticker_list

def fetch_price_range(ticker, days_back, conn=None, calendar_days=False):
    """
    Retrieve OHLC (Open, High, Low, Close) stock price data for a given ticker symbol over a specified number of calendar or trading days.

    This function queries the `asset_prices` table from the `assets.db` SQLite database and returns historical price data starting from the most recent available date. Users can specify whether the retrieval window should consider calendar days or strictly the last N trading days.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol (e.g., 'AAPL').
    days_back : int
        Number of days to retrieve price data for.
    conn : sqlite3.Connection, optional
        An existing SQLite database connection. If None, a new connection to 'assets.db' is established and closed automatically.
    calendar_days : bool, optional
        If True, fetch prices from the last `days_back` calendar days.
        If False (default), fetch prices from the last `days_back` trading days only.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing historical OHLC data with the following columns:
        - 'date' (datetime64): Date of the price record.
        - 'open' (float): Opening price of the stock.
        - 'high' (float): Highest price during the trading session.
        - 'low' (float): Lowest price during the trading session.
        - 'close' (float): Closing price of the stock.

        If no price data is available for the given parameters, an empty DataFrame with the above columns is returned.

    Raises
    ------
    sqlite3.Error
        If a database connection or SQL query execution fails.
    ValueError
        If input parameters are invalid or result in no data retrieval.

    Examples
    --------
    Retrieve Apple's closing prices for the past 60 calendar days:

    >>> df_calendar = fetch_price_range('AAPL', 60, calendar_days=True)
    >>> print(df_calendar.head())

    Retrieve Microsoft's price data for the last 30 trading days:

    >>> df_trading = fetch_price_range('MSFT', 30, calendar_days=False)
    >>> print(df_trading.tail())
    """
    close_conn = False
    if conn is None:
        conn = get_db_connection('assets.db')
        close_conn = True

    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(date)
        FROM asset_prices
        WHERE asset_id = (SELECT asset_id FROM asset_metadata WHERE symbol = ?)
    """, (ticker,))
    most_recent_date = cursor.fetchone()[0]

    if most_recent_date:
        most_recent_date = datetime.strptime(most_recent_date, '%Y-%m-%d')

        if calendar_days:
            start_date = most_recent_date - timedelta(days=days_back)
            start_date_str = start_date.strftime('%Y-%m-%d')
            print(f"Querying {ticker} prices from {start_date_str} to {most_recent_date.strftime('%Y-%m-%d')}")
            
            query = """
                SELECT date, open, high, low, close
                FROM asset_prices
                WHERE asset_id = (SELECT asset_id FROM asset_metadata WHERE symbol = ?)
                AND date >= ?
                ORDER BY date ASC
            """
            params = (ticker, start_date_str)

        else:
            # Fetch trading days (recent N entries ordered descending)
            cursor.execute("""
                SELECT date
                FROM asset_prices
                WHERE asset_id = (SELECT asset_id FROM asset_metadata WHERE symbol = ?)
                ORDER BY date DESC
                LIMIT ?
            """, (ticker, days_back))
            dates = cursor.fetchall()

            if not dates:
                print(f"No price data found for {ticker} in assets.db")
                return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close'])

            earliest_date = dates[-1][0]  # last row fetched is earliest date
            print(f"Querying {ticker} prices for last {days_back} trading days from {earliest_date} to {most_recent_date.strftime('%Y-%m-%d')}")

            query = """
                SELECT date, open, high, low, close
                FROM asset_prices
                WHERE asset_id = (SELECT asset_id FROM asset_metadata WHERE symbol = ?)
                AND date >= ?
                ORDER BY date ASC
            """
            params = (ticker, earliest_date)

        price_data = pd.read_sql_query(query, conn, params=params)
        price_data['date'] = pd.to_datetime(price_data['date'])
        print(f"Fetched {len(price_data)} price records for {ticker}")
    else:
        print(f"No price data found for {ticker} in assets.db")
        price_data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close'])

    if close_conn:
        conn.close()
    
    return price_data

