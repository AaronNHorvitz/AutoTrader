# src/etl/__init__.py
"""
Initialization file for the ETL module of stat_656_autotrader.
Imports all functions from populate_prices.py, populate_tickers.py, and utils.py.
"""

from .populate_prices import (
    ensure_prices_table_exists,
    get_tickers_from_db,
    populate_historical_prices,
    update_latest_prices
)

from .populate_tickers import (
    populate_tickers
)

from .utils import (
    connect_to_alpaca,
    fetch_alpaca_stock_tickers,
    fetch_alpaca_historical_data,
    fetch_alpaca_yesterday_ohlc,
    fetch_alpaca_open_prices,
    fetch_alpaca_latest_bars
)

__all__ = [
    'ensure_prices_table_exists',
    'get_tickers_from_db',
    'populate_historical_prices',
    'update_latest_prices',
    'ensure_database_exists',
    'populate_tickers',
    'connect_to_alpaca',
    'fetch_alpaca_stock_tickers',
    'fetch_alpaca_historical_data',
    'fetch_alpaca_yesterday_ohlc',
    'fetch_alpaca_open_prices',
    'fetch_alpaca_latest_bars'
]