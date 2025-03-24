# STAT 656 Autotrader

Welcome to the STAT 656 Autotrader by the Data Science Daytraders. This project fetches stock and ETF tickers from Alpaca, stores them in a SQLite database, integrates exogenous data (YFinance/FRED), and executes an autotrader (175 stocks OHLC 2002-2025 1-5+ days).

## Prerequisites

- **Python 3.11+**: Installed on your system.
- **Libraries**: `pandas`, `requests`, `sqlite3` (standard), `alpaca-trade-api` (`pip install alpaca-trade-api`), `yfinance`, `fredapi` (for exogenous data ).

## Setup

Follow these steps to set up the STAT 656 Autotrader ():

### Step 1: Install Prerequisites

#### 1. Install Git
- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win).
- **Mac**: Run `brew install git` ([brew.sh](https://brew.sh)) or download from [git-scm.com](https://git-scm.com/download/mac).
- **Verify**: `git --version`.

#### 2. Install Anaconda
- **Download**: [Anaconda.com](https://www.anaconda.com/products/distribution).
- **Install**: Follow the installer instructions.
- **Verify**: `conda --version`.

#### 3. Check SQLite
- **Anaconda**: SQLite is pre-installed. Verify: `sqlite3 --version`.
- **Install (if needed)**: `conda install -c conda-forge sqlite`.

#### 4. Clone the Repository
- **Terminal**: 
  ```bash
  git clone https://github.com/YOUR_USERNAME/stat_656_autotrader.git
  cd stat_656_autotrader

### Step 2: Set Up the Environment
Create Environment: Use environment.yaml to set up dependencies. NOTE: This could take more than an hour to run. 
```
conda env create -f environment.yaml
conda activate autotrader
```

After creating your environment, run the following command to ensure the autotrader environment appears in JupyterLab, Jupyter Notebook, and VS Code:

```
python -m ipykernel install --user --name=autotrader --display-name "Python (autotrader)"
```
This registers your environment as a Jupyter kernel and makes it selectable in notebook interfaces and IDEs like VS Code.

### Step 3: Get an Alpaca Account

Before you can download tickers, you need an Alpaca account and API keys. Alpaca offers free paper trading ($0)—no real money, just data and trades to play with. Here’s how to set it up:

#### - 1. Sign Up
- **Visit**: [Alpaca Markets](https://alpaca.markets/)
- **Action**: Click “Get Started” (top right) or “Sign Up” (center).
- **Details**: Enter your email and create a password.

#### - 2. Switch to Paper Trading
- **Log In**: Head to [app.alpaca.markets](https://app.alpaca.markets/).
- **Toggle**: Top left corner—switch from “Live” to “Paper”.
- Paper trading gives you API access without funding.

#### - 3. Generate API Keys
- **Dashboard**: Scroll to “Your API Keys” (right side).
- **Click**: “Generate New Keys” (or “View” if already there).

#### - 4. Type the Key and Secret into the .secrets file and save.
- **Create**: Create an empty text file.
- **Copy**: Grab your **API Key ID** (e.g., `PK123...`) and **Secret Key** (e.g., `abc...xyz`).
- **Paste**: Paste your credentials in the text file so it looks like this:
- **Save**: Save your credentials as '.secrets' in the 'credentials' directory.

#### This is how the text should look inside the 'credentials/.secrets' file. 
  ```
  ALPACA_API_KEY="your_alpaca_key"
  ALPACA_SECRET_KEY="your_alpaca_secret"
  ALPAKA_ENDPOINT_URL=""
  ```

### Step 4: Run 'setup.py' to Initialize and Populate the Databases

Run the setup.py script to check and create the SQLite databases (6 .db files: assets.db, portfolio_management.db, accounting.db, modeling.db, exogenous.db, db_change_log.db):

#### - 1. Open a terminal, navigate to `STAT_656_AUTOTRADER/src/` and run:
  ```
  python setup.py
  ```
What it does:
Checks if databases exist in databases/ (creates them if missing $0).
Sets up 13 tables (with foreign keys see $0).
Logs actions to logs/setup.log (for debugging $0).

Expected Output:
```
Creating assets.db...
Tables in assets.db created/verified.
Creating portfolio_management.db...
Tables in portfolio_management.db created/verified.
[... repeats for all 6 DBs ...]
All databases initialized successfully!
```


## File Structure/ Project Architecture

```
stat_656_autotrader/

├── Sandbox/
|    |
|    └──  test_notebook/        # Play space for experiments
|    
├── Notebooks/
|    |
|    ├── 001_Connecting_to_Alpaca_Tutorial.ipynb   # Demos (e.g., Alpaca API setup)
|    ├── 002_Create_and_Update_Database.ipynb      
|    └── 003_Query_and_Visualize_Data.ipynb              
|
├── databases/
|    |
|    ├── assets.db             # Asset metadata, prices, dividends, actions 
|    ├── portfolio_management.db  # Holdings, transactions, KPIs 
|    ├── accounting.db         # Accounts, balances, cash flows, taxes 
|    ├── modeling.db           # Model & actual forecasts 
|    ├── exogenous.db          # Exogenous metadata & values
|    └── db_change_log.db      # Audit trail 
|    |
├── logs/                      # Log files
|    ├── setup.log             # Setup run logs
|    └── fetch.log             # New 
| 
├── credentials/
|    └── .secrets              # API keys 
|    
├── src/
|    |
|    ├── models/
|    |   |
|    |   ├── forecasting/      # Prediction logic 
|    |   └── trading/          # Trading logic 
|    |
|    ├── etl/
|    |   |
|    |   ├── db_setup/         # DB creation scripts (e.g., setup.sql or .py)
|    |   ├── db_updates/       # DB update scripts (e.g., insert prices, exogenous)
|    |   └── data_fetch/       # New (fetch scripts Alpaca/YFinance/FRED)
|    |
|    ├── execution/            # Trade execution (Alpaca API calls)
|    |
|    ├── dashboard/            # Dashboard logic (e.g., Flask/Dash)
|    |   ├── templates/        # HTML 
|    |   └── static/           # CSS, JS 
|    | 
|    ├── tests/                # Unit tests 
|    |   ├── test_models.py    # Test forecasting/trading
|    |   └── test_etl.py       # Test DB setup/updates
|    |
|    ├── utils/                # Helper functions (e.g., logging, date utils)
|    ├── config.py             # Settings (BASE_URL, DB paths, API endpoints)
|    ├── db_schema.py          # Database schema used during initial setup. 
|    ├── get_tickers.py        # Fetch asset metadata (Alpaca updated with logging)
|    └── main.py               # Entry point (runs pipeline)
|    
├── setup.py                   # Creates DBs, populates initial metadata
├── .gitignore                 # Protects secrets, logs, DBs (e.g., *.db, .secrets)
├── environment.yaml           # Anaconda env (dependencies e.g., pandas, yfinance)
└── README.md                  # Project overview (this file)
```
## Data Dictionary/ Data Architecture

Below is the data dictionary for the database architecture (6 `.db` files, 13 tables ). All timestamps use ISO 8601 format (e.g., "2025-03-22 13:00:00" TEXT in SQLite sortable ).

#### 1. `assets.db` (Asset Data)
- **`asset_metadata`** (Asset details):
  - `asset_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique asset ID.
  - `symbol` (TEXT, UNIQUE): Asset ticker (e.g., "AAPL").
  - `name` (TEXT): Full name (e.g., "Apple Inc.").
  - `exchange` (TEXT): Exchange (e.g., "NASDAQ", "NYSE").
  - `asset_type` (TEXT): Type (e.g., "Stock", "ETF", "Crypto").
  - `sector` (TEXT): Sector (e.g., "Technology").
  - `industry` (TEXT): Industry (e.g., "Consumer Electronics").
  - `currency` (TEXT): Trading currency (e.g., "USD").
  - `has_dividend` (INTEGER): 1 (true) or 0 (false) if pays dividends.
  - `is_active` (INTEGER): 1 (tradable) or 0 (inactive Alpaca).
  - `date_added` (TEXT): ISO 8601 date added (e.g., "2025-03-22").
  - `date_removed` (TEXT): ISO 8601 date removed (NULL if active).
  - `fetched_at` (TEXT): ISO 8601 timestamp of last fetch (e.g., "2025-03-22 13:00:00").

- **`asset_dividends`** (Dividend history):
  - `dividend_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique dividend ID.
  - `asset_id` (INTEGER, FOREIGN KEY -> asset_metadata.asset_id): Links to asset.
  - `symbol` (TEXT): Asset ticker (redundant speed e.g., "AAPL").
  - `ex_date` (TEXT): ISO 8601 ex-dividend date (e.g., "2025-03-22").
  - `record_date` (TEXT): ISO 8601 record date (e.g., "2025-03-23").
  - `pay_date` (TEXT): ISO 8601 payment date (e.g., "2025-04-01").
  - `amount` (REAL): Dividend amount (USD e.g., 0.23).
  - `currency` (TEXT): Currency (e.g., "USD").
  - `dividend_type` (TEXT): Type (e.g., "Regular", "Special").
  - `source` (TEXT): Data source (e.g., "Alpaca", "Yahoo").
  - `fetched_at` (TEXT): ISO 8601 timestamp (e.g., "2025-03-22 13:00:00").

- **`corporate_actions`** (Splits, mergers):
  - `action_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique action ID.
  - `asset_id` (INTEGER, FOREIGN KEY -> asset_metadata.asset_id): Links to asset.
  - `symbol` (TEXT): Asset ticker (redundant speed e.g., "AAPL").
  - `action_type` (TEXT): Type (e.g., "Split", "Merger").
  - `action_description` (TEXT): Details (e.g., "2-for-1 split").
  - `action_date` (TEXT): ISO 8601 effective date (e.g., "2025-03-22").
  - `ratio` (REAL): Ratio (e.g., 2.0 NULL if N/A).
  - `cash_value` (REAL): Cash component (USD e.g., 5.00 NULL if N/A).
  - `notes` (TEXT): Additional info (NULL if empty).
  - `fetched_at` (TEXT): ISO 8601 timestamp (e.g., "2025-03-22 13:00:00").

- **`asset_prices`** (OHLC data):
  - `price_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique price ID.
  - `asset_id` (INTEGER, FOREIGN KEY -> asset_metadata.asset_id): Links to asset.
  - `date` (TEXT): ISO 8601 date (e.g., "2025-03-22").
  - `open` (REAL): Opening price (USD e.g., 150.25).
  - `high` (REAL): High price (USD).
  - `low` (REAL): Low price (USD).
  - `close` (REAL): Closing price (USD).
  - `adjusted_close` (REAL): Adjusted closing price (USD dividends/splits).
  - `volume` (INTEGER): Trading volume (shares e.g., 1000000).
  - `fetched_at` (TEXT): ISO 8601 timestamp (e.g., "2025-03-22 13:00:00").

#### 2. `portfolio_management.db` (Portfolio & Trades)
- **`asset_holdings`** (Current positions):
  - `holding_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique holding ID.
  - `account_id` (INTEGER, FOREIGN KEY -> record_of_accounts.account_id): Links to account.
  - `asset_id` (INTEGER, FOREIGN KEY -> asset_metadata.asset_id): Links to asset.
  - `date` (TEXT): ISO 8601 date (e.g., "2025-03-22" history).
  - `quantity` (REAL): Shares/contracts (e.g., 10.5 fractional).
  - `avg_cost` (REAL): Average cost basis (USD e.g., 145.50).
  - `last_updated` (TEXT): ISO 8601 timestamp (e.g., "2025-03-22 13:00:00").

- **`transactions`** (Executed trades):
  - `transaction_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique transaction ID.
  - `account_id` (INTEGER, FOREIGN KEY -> record_of_accounts.account_id): Links to account.
  - `asset_id` (INTEGER, FOREIGN KEY -> asset_metadata.asset_id): Links to asset.
  - `transaction_type` (TEXT): Type (e.g., "Buy", "Sell", "Dividend").
  - `quantity` (REAL): Shares/contracts (e.g., 10.0).
  - `price` (REAL): Price per share (USD e.g., 150.00).
  - `fees` (REAL): Fees (USD e.g., 1.50).
  - `timestamp` (TEXT): ISO 8601 timestamp (e.g., "2025-03-22 14:30:00").

- **`kpi_tracker`** (Performance metrics):
  - `kpi_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique KPI ID.
  - `account_id` (INTEGER, FOREIGN KEY -> record_of_accounts.account_id): Links to account.
  - `kpi_date` (TEXT): ISO 8601 date (e.g., "2025-03-22").
  - `total_return` (REAL): Cumulative return (% e.g., 0.05 5%).
  - `daily_return` (REAL): Daily return (% e.g., 0.01 1%).
  - `win_rate` (REAL): Win rate (0-1 e.g., 0.65 65%).
  - `profit_factor` (REAL): Profit factor (e.g., 1.8).
  - `max_drawdown` (REAL): Max drawdown (% e.g., -0.10 10%).
  - `sharpe_ratio` (REAL): Sharpe ratio (e.g., 1.5).
  - `alpha` (REAL): Alpha (e.g., 0.02).
  - `beta` (REAL): Beta (e.g., 0.95).
  - `volatility` (REAL): Volatility (% e.g., 0.15 15%).
  - `trading_days` (INTEGER): Days tracked (e.g., 252).
  - `timestamp` (TEXT): ISO 8601 timestamp (e.g., "2025-03-22 13:00:00").

#### 3. `accounting.db` (Financials)
- **`record_of_accounts`** (Account metadata):
  - `account_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique account ID.
  - `account_name` (TEXT): Name (e.g., "Main Trading Account").
  - `account_type` (TEXT): Type (e.g., "Actual", "Simulated").
  - `owner` (TEXT): Owner (e.g., "John Doe" NULL if system).
  - `status` (TEXT): Status (e.g., "Active", "Closed").
  - `date_opened` (TEXT): ISO 8601 date (e.g., "2025-01-01").
  - `date_closed` (TEXT): ISO 8601 date (NULL if active).

- **`account_balances`** (Cash & equity):
  - `balance_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique balance ID.
  - `account_id` (INTEGER, FOREIGN KEY -> record_of_accounts.account_id): Links to account.
  - `date` (TEXT): ISO 8601 date (e.g., "2025-03-22").
  - `cash_available` (REAL): Cash for trading (USD e.g., 50000.00).
  - `total_cash` (REAL): Total cash (USD e.g., 51000.00).
  - `total_assets_value` (REAL): Asset value (USD e.g., 75000.00).
  - `total_equity` (REAL): Equity (USD e.g., 125000.00).
  - `liabilities` (REAL): Liabilities (USD e.g., 0.00 margin).

- **`record_of_cash_flows`** (Cash movements):
  - `cash_flow_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique cash flow ID.
  - `account_id` (INTEGER, FOREIGN KEY -> record_of_accounts.account_id): Links to account.
  - `date` (TEXT): ISO 8601 date (e.g., "2025-03-22").
  - `cash_addition` (REAL): Deposits (USD e.g., 1000.00 NULL if N/A).
  - `cash_withdrawal` (REAL): Withdrawals (USD e.g., 500.00 NULL if N/A).
  - `fees` (REAL): Fees (USD e.g., 1.50 NULL if N/A).
  - `note` (TEXT): Description (e.g., "AAPL Buy $1500" NULL if empty).

- **`tax_transactions`** (Tax liabilities):
  - `tax_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique tax ID.
  - `account_id` (INTEGER, FOREIGN KEY -> record_of_accounts.account_id): Links to account.
  - `transaction_id` (INTEGER, FOREIGN KEY -> transactions.transaction_id): Links to trade.
  - `realized_gain` (REAL): Gain/loss (USD e.g., 100.00).
  - `tax_liability` (REAL): Tax owed (USD e.g., 20.00).
  - `tax_paid` (REAL): Tax paid (USD e.g., 0.00).
  - `tax_year` (INTEGER): Year (e.g., 2025).
  - `date_recorded` (TEXT): ISO 8601 date (e.g., "2025-03-22").

#### 4. `modeling.db` (Forecasts)
- **`model_forecasts`** (Predictions):
  - `forecast_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique forecast ID.
  - `model_name` (TEXT): Model name (e.g., "ARIMA").
  - `asset_id` (INTEGER, FOREIGN KEY -> asset_metadata.asset_id): Links to asset.
  - `forecast_date` (TEXT): ISO 8601 date (e.g., "2025-03-22").
  - `predicted_return` (REAL): Predicted return (% e.g., 0.02 2%).
  - `confidence` (REAL): Confidence (0-1 e.g., 0.95).
  - `horizon_days` (INTEGER): Forecast horizon (e.g., 5).
  - `model_version` (TEXT): Version (e.g., "v1.0").

- **`actual_forecasts`** (Realized returns):
  - `actual_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique actual ID.
  - `forecast_id` (INTEGER, FOREIGN KEY -> model_forecasts.forecast_id): Links to forecast.
  - `actual_return` (REAL): Realized return (% e.g., 0.015 1.5%).
  - `comparison_date` (TEXT): ISO 8601 date (e.g., "2025-03-27").

#### 5. `exogenous.db` (External Indicators)
- **`exogenous_metadata`** (Indicator details):
  - `exog_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique indicator ID.
  - `exog_symbol` (TEXT, UNIQUE): Indicator symbol (e.g., "CL=F").
  - `exog_title` (TEXT): Name (e.g., "WTI Crude Oil").
  - `explanation_description` (TEXT): What it is (e.g., "Futures price of WTI crude oil").
  - `explanation_importance` (TEXT): Why it matters (e.g., "Influences energy stocks").
  - `source` (TEXT): Source (e.g., "YFinance", "FRED").
  - `frequency` (TEXT): Frequency (e.g., "Daily", "Monthly").
  - `units` (TEXT): Units (e.g., "Dollars").
  - `lag` (REAL): Lag (e.g., 1.0 days).
  - `in_use` (INTEGER): 1 (true) or 0 (false).
  - `date_added` (TEXT): ISO 8601 date (e.g., "2025-03-22").
  - `last_fetch` (TEXT): ISO 8601 timestamp (e.g., "2025-03-22 13:00:00").

- **`exogenous_vals`** (Indicator values):
  - `exog_vals_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique value ID.
  - `exog_id` (INTEGER, FOREIGN KEY -> exogenous_metadata.exog_id): Links to indicator.
  - `date` (TEXT): ISO 8601 date (e.g., "2025-03-22").
  - `open` (REAL): Opening value (USD NULL if N/A).
  - `high` (REAL): High value (USD NULL if N/A).
  - `low` (REAL): Low value (USD NULL if N/A).
  - `close` (REAL): Closing value (USD NULL if N/A).
  - `adjusted_close` (REAL): Adjusted value (USD NULL if N/A).
  - `fetched_at` (TEXT): ISO 8601 timestamp (e.g., "2025-03-22 13:00:00").

#### 6. `db_change_log.db` (Audit Trail)
- **`change_log`** (DB updates):
  - `log_id` (INTEGER, PRIMARY KEY, AUTOINCREMENT): Unique log ID.
  - `table_name` (TEXT): Table affected (e.g., "asset_prices").
  - `change_type` (TEXT): Type (e.g., "INSERT", "UPDATE").
  - `change_detail` (TEXT): Details (e.g., "Added price for AAPL").
  - `changed_at` (TEXT): ISO 8601 timestamp (e.g., "2025-03-22 13:00:00").
  - `user` (TEXT): User/system (e.g., "system" NULL if unknown).
  - `db_name` (TEXT): Database (e.g., "assets.db").