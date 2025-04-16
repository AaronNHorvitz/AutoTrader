# src/__init__.py

from .etl import (
    populate_prices, 
    populate_tickers,
    recreate_database,
    update_daily_prices,
)

from .utils import (
    get_alpaca_client,
    fetch_alpaca_stock_tickers,
    fetch_alpaca_historical_data,
    fetch_alpaca_latest_bars,
    get_db_connection,
    fetch_active_tickers,
    get_latest_price_date,
    last_data_date, 
    last_fetch_date,
    fetch_database_stock_tickers,
    populate_alpaca_full_history,
    )

from .statistics import (
    smooth_lowess,
)

from .visualizations import (
    plot_stock_trends,
)

from src.config import (
    DB_DIR,
    BASE_DIR, 
    LOG_DIR, 
    CREDENTIALS_DIR
)

__all__ = [
    'get_alpaca_client',
    'fetch_alpaca_stock_tickers',
    'fetch_alpaca_historical_data',
    'fetch_alpaca_latest_bars',
    'get_db_connection',
    'fetch_active_tickers',
    'get_latest_price_date',
    'populate_prices',
    'populate_tickers',
    'recreate_database',
    'update_daily_prices',
    'smooth_lowess',
    'plot_stock_trends',
    'last_data_date',
    'last_fetch_date',
    'fetch_database_stock_tickers',
    'fetch_alpaca_full_price_history',
    'populate_alpaca_full_history',
]