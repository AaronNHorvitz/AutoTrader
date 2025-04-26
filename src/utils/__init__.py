#src/utils/__init__.py
"""
Utilities module initialization for stat_656_autotrader.
"""

from .alpaca_utils import (
    get_alpaca_client,
    connect_to_alpaca,
    fetch_alpaca_stock_tickers,
    fetch_alpaca_historical_data,
    fetch_alpaca_yesterday_ohlc,
    fetch_alpaca_open_prices,
    fetch_alpaca_latest_bars,
    update_stock_prices,
    populate_alpaca_full_history
)

from .db_utils import (
    get_db_connection,
    fetch_active_tickers,
    get_latest_price_date,
    fetch_all_asset_metadata,  
    fetch_all_asset_prices, 
    last_data_date, 
    last_fetch_date,
    fetch_database_stock_tickers,
    fetch_price_range
)

__all__ = [
    'get_alpaca_client',
    'connect_to_alpaca',
    'fetch_alpaca_stock_tickers',
    'update_stock_prices',
    'fetch_alpaca_historical_data',
    'fetch_alpaca_yesterday_ohlc',
    'fetch_alpaca_open_prices',
    'fetch_alpaca_latest_bars',
    'get_db_connection',
    'fetch_active_tickers',
    'get_latest_price_date',
    'fetch_all_asset_metadata',  
    'fetch_all_asset_prices', 
    'last_data_date', 
    'last_fetch_date',
    'fetch_database_stock_tickers',
    'populate_alpaca_full_history',
    'fetch_price_range'
]