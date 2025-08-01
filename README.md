# Autotrader - In Development

Welcome to the AutoTrader. This project fetches stock tickers and historical data from Alpaca, storing them in a structured SQLite database. It leverages **ARIMAX forecasting**, and **Bayesian (MCMC) methods** for systematic stock selection, portfolio optimization, and automated daily trading.

---

## Trading Strategy Overview

The Autotrader implements a systematic trading approach combining:

- **ARIMAX (ARIMA with Exogenous Inputs)** models for robust price forecasting.
- **Bayesian Portfolio Optimization (MCMC)** for intelligent stock selection based on forecasted returns and volatility.

---
## Workflow 

## ARIMAX Forecasting Workflow Summary

```
Fetch Historical HLOC Data
           │
Check for Randomness & Randomness with Drift
           │
Smooth Data (LOWESS)
           │
Detect Level Shifts (Change points)
           │
Test Stationarity (ADF & KPSS)
           │
Check Predictive Power (Open prices around shifts)
           │
Conduct Final Randomness Tests (Runs, Ljung-Box, etc.)
           │
Confirm Data Suitable for ARIMAX
           │
Integrate Opening Prices (Transfer Function)
           │
Fit & Forecast ARIMAX Model


```
## MCMC Retraining Periods
 - MCMC Retrains every weekend
 - MCMC Retrains every Market Holiday (Except when it's integrated into a 3 day weekend)

## Integrated Trading Workflow (Including MCMC Selection and Unsuitable Stocks)

```
Fetch Daily Historical Data (HLOC) for All Candidate Stocks
                       │
         Fetch the Morning's Open Price Data
                       │
       Perform Level Shift and Stationarity Tests
                       │
      Data Suitable for Forecasting (ARIMAX Forecasting)?
            ┌───────────┴───────────┐
            │                       │
           Yes                      No
            │                       │               
Flag as Trustworthy           Flag as Untrustworthy
Forecast                      Forecast (Consider Selling)
            └─────────────┬─────────┘
                          │
               Forecast Prices (H, L, C)  
                          │
            Perform MCMC Portfolio Optimization
     (Identifies Optimal Stocks to Buy or Sell Based on Criteria)
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
 MCMC Identified as                   MCMC Identified as 
 BUY candidate                        SELL candidate
        │                                   │
 Suitable?                           Suitable?
 │                                   │
 ├─Yes: Forecast-based─┐             ├─Yes: Forecast-based─┐
 │ BUY LIMIT           │             │ SELL LIMIT           │
 │ (Forecast Low-Close)│             │ (Forecast High-Close)│
 │                     │             │                      │
 │ Immediately set     │             │ Immediately set      │
 │ Stop-loss Sell Limit│             │ Buyback Limit        │
 │ (below Low)         │             │ (above High)         │
 │                     │             │                      │
 ├─No: Conservative────┤             ├─No: Conservative─────┤
 │ Set conservative    │             │ Set conservative      │
 │ BUY LIMIT at recent │             │ SELL LIMIT at recent  │
 │ stable low          │             │ stable high           │
 │                     │             │                       │
 │ Immediately set     │             │ Immediately set       │
 │ strict Stop-loss    │             │ strict Buyback Limit  │
 │ (tight range)       │             │ (tight range)         │
 └─────────────────────┘             └───────────────────────┘
              │                               │
     Execute Trades via Alpaca API (buy or sell as directed)
              │                               │
              │                               │
   Daily ARIMAX Forecast Update     Daily ARIMAX Forecast Update
Adjust stop-loss ↑ only, Adjust buyback limit ↓ only (adaptive strategy)
              │                               │
              │                               │
Market Surge Detection & Protection (Catch unexpected spikes)
   - Monitor forecasted vs. actual High/Low deviations
   - Flag large surge in prices (beyond forecast intervals)
   - Trigger immediate review or special actions
```

## Price Setting Formulas 
### Buy Limit
$Buy Limit = \frac{Forecasted Low + Forecasted Close }{2}$

### Initial Defensive Sell Limit After Purchase (Stop-loss): (to guard against immediate stock price plunges)

$Stop Loss = Forecasted Low - (Forecasted Close - Forecasted Low) x 0.5$

### Sell Limit
$Sell Limit = \frac{Forecasted High + Forecasted Close }{2}$

### Stock Purchase Example:
The MCMC model identifies a stock for purchase. The forecasted low is $150, and the forecasted close is $155. 
- The Auto-Trader will execute a **Buy-Limit Order** at ($150 + $155)/2 = **$152.50**
- After the purchase is executed, the Auto-Trader will immeidately set a **Stop-Loss Order** at  $150 - ($155 - $150) × 0.5 = **$147.50**
- The Auto-Trader will record the transaction and update the financials. 

### Stock Sale Example:
The MCMC model identifies a stock to sell. The forecasted high is $160, and the forecasted close is $155.
 - The Auto-Trader will execute a **Sell-Limit Order** at ($160 + $155)/2 = **$157.50**
 - If the trade fails to execute, and the previous **Stop-Loss Order** fails to execute the Auto-Trader will execute a *Sell-Market Order* five minutes prior to the market close.

### Daily Stop-Loss Order Updates
 - The Auto-Trader will update **Stop-Loss Orders** daily based on daily forecasts. 

## Special Circumstances
### Circumstances
- If the stock is flagged as "unsuitable," trade cautiously and defensively to minimize potential losses.
- Continuously monitor model accuracy, especially during market volatility or periods of instability.
- Leverage the flexibility of the automated system to rapidly respond to emerging market conditions.
- Monitoring: Track actual market prices vs. forecast intervals.
- Surge Detection: Flag significant deviations beyond predicted intervals.

### Immediate Response:
- Temporarily flag stock as unsuitable.
- Execute conservative orders to capitalize on unexpected surges or exit positions safely.
- Re-evaluate stability after shifts. Resume standard trading if conditions stabilize.

## Prerequisites

- **Python 3.11+**: Required for the project.
- **Git**: For cloning the repository.
- **Anaconda**: For managing the Python environment and dependencies.
- **Libraries**: Key dependencies include `pandas`, `requests`, `sqlite3` (standard library), `alpaca-trade-api`, `fredapi`, and more (see `environment.yaml`).

## Setup

Follow these steps to set up the STAT 656 Autotrader:

### Step 1: Install Prerequisites

#### - A. Install Git
- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win).
- **Mac**: Run `brew install git` ([brew.sh](https://brew.sh)) or download from [git-scm.com](https://git-scm.com/download/mac).
- **Verify**: `git --version`.

#### - B. Install Anaconda
- **Download**: [Anaconda.com](https://www.anaconda.com/products/distribution).
- **Install**: Follow the installer instructions.
- **Verify**: `conda --version`.

#### - C. Open the Anaconda PowerShell Prompt (Windows Users)
After installing Anaconda on Windows, use the **Anaconda PowerShell Prompt** to run commands. This ensures Conda and Python are accessible:
- **Start Menu**: Search for "Anaconda PowerShell Prompt" and open it.
- **Verify Conda**: In the prompt, run:
  ```powershell
  conda --version
  ```
  You should see something like `conda 23.7.4`. If not, ensure Anaconda was added to your PATH during installation or reinstall it.

#### - D. Clone the Repository
This makes a copy of all the code you will use during this project. While in the Anaconda Powershell, navigate to the directory where you want to store the project's code. This is often a `dev` folder. Type the following into the directory you want to save the code. 

```
git clone https://github.com/AaronNHorvitz/stat_656_autotrader.git
```

***NOTE*** If you’ve already cloned the repository and are setting up your environment again, run one of these commands to update your local copy. Do this every time you start working on your code to stay in sync:
```
git pull origin main
```
or
```
git pull https://github.com/AaronNHorvitz/stat_656_autotrader.git
```

#### - E. Set Up the Environment
Next you will need a copy of all the open source software in an environment that we will all use to code in. This ensures that the versions of the software we are using are the same.  
There is a PowerShell script named `setup_env.ps1` that simplifies setting up your coding environment. It automatically uses the `environment.yaml` file to install the required library packages and their specific versions. To speed up the setup process, it installs Mamba as a faster alternative to Conda.

##### - 1. Navigate to the Project Directory:
Type in this and hit enter:
```
cd stat_656_autotrader
```
I'm in linux and I'm trying to run a script to intsall Mamba. My instructions are: 
##### - 2. Run the Setup Script:
This script:
- Installs Mamba if not already present.
- Removes any existing autotrader environment.
- Creates a fresh autotrader environment using environment.yaml.

**Windows**
```
.\setup_env.ps1
```

**Updated Environment Setup Instructions for Mac/Linux Users**
- Step 1: Before running the setup script on Mac or Linux, you need to set execute permissions for the script. Open your terminal and run:
```
chmod +x setup_env.ps1
```

- Step 2: Run the Setup Script

Execute the script using PowerShell. On Mac and Linux systems, install PowerShell first if you don't have it already:
- *MacOS*
```
brew install powershell
```

- *Linux (Ubuntu/Debian):*
```
sudo apt-get update
sudo apt-get install -y powershell
```
- Then, run the setup script using PowerShell:

```
pwsh setup_env.ps1
```

##### - 3. Activate the Environment:

```
conda activate autotrader
```

##### - 4. Register the Kernel (For Jupyter Lab, Jupyter Notebook, VS Code):
This registers your environment as a Jupyter kernel, making it selectable in notebook interfaces and IDEs like VS Code.

```
python -m ipykernel install --user --name=autotrader --display-name "Python (autotrader)"
```

### Step 2: Get an Alpaca Account

Before you can download tickers, you need an Alpaca account and API keys. Alpaca offers free paper trading ($0)—no real money, just data and trades to play with. Here’s how to set it up:

#### - A. Sign Up
- **Visit**: [Alpaca Markets](https://alpaca.markets/)
- **Action**: Click “Get Started” (top right) or “Sign Up” (center).
- **Details**: Enter your email and create a password.

#### - B. Switch to Paper Trading 
#### (WARNING: This step may not work for you. If it doesn't you may need to use a credit/ debit card.)
- **Log In**: Head to [app.alpaca.markets](https://app.alpaca.markets/).
- **Toggle**: Top left corner—switch from “Live” to “Paper”.
- Paper trading gives you API access without funding.

#### - C. Generate API Keys
- **Dashboard**: Scroll to “Your API Keys” (right side).
- **Click**: “Generate New Keys” (or “View” if already there).

#### - D. Type the Key and Secret into the .secrets file and save.
- **Create**: Create an empty text file.
- **Copy**: Grab your **API Key ID** (e.g., `PK123...`) and **Secret Key** (e.g., `abc...xyz`).
- **Paste**: Paste your credentials in the text file so it looks like this:
- **Save**: Save your credentials as '.secrets' in the 'credentials' directory.

#### - E. This is how the text should look inside the 'credentials/.secrets' file. 
  ```
  ALPACA_API_KEY="your_alpaca_key"
  ALPACA_SECRET_KEY="your_alpaca_secret"
  ALPAKA_ENDPOINT_URL=""
  ```
### Step 3: Run 'setup.py' to Initialize and Populate the Databases

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
### Step 4: Running the Tutorials from a Jupyter Notebook

#### - 1. Launching a Jupyter Notebook
Open the Anaconda PowerShell Prompt, type the following at the prompt, and hit Enter:
```
jupyter-notebook
```
#### - 2. Navigate to the `Notebooks` directory. 
In the Jupyter interface, click through to the Notebooks folder.

#### - 3. Open the First Jupyter Notebook Tutorial Labeled `001 Tutorial - Connecting and Testing Alpaca Connections.ipynb` 
Run the Python code sequentially in each cell to ensure all connections (e.g., Alpaca API) are working.

#### - 4. Open up the second Jupyter Notebook Tutorial labeled `002 Set Up Databases and Populating Tickers and Historical Stock Data.ipynb` 
Run the Python code sequentially in each cell to populate the database with the most recent tickers and stock prices.


## File Structure/ Project Architecture

```
stat_656_autotrader/

├── Sandbox/
|    |
|    └──  test_notebook/        # Play space for experiments
|    
├── Notebooks/
|    |
|    ├── 001 Tutorial - Connecting and Testing Alpaca Connections.ipynb
|    ├── 002 Tutorial - Set Up Databases and Populating Tickers and Historical Stock Data.ipynb
|    ├── 003 Tutorial - Update Recent Stock Prices and Visualize.ipynb  
|    ├── 004 Tutorial - Visualize Stock Data.ipynb  
|    ├── 005 Tutorial - Simple Database Queries.ipynb 
|    ├── 006 Tutorial - Tests for Randomness.ipynb
|    └── <add notebooks as needed>             
|
├── databases/
|    |
|    ├── assets.db             # Asset metadata, prices, dividends, actions 
|    ├── portfolio_management.db  # Holdings, transactions, KPIs 
|    ├── accounting.db         # Accounts, balances, cash flows, taxes 
|    ├── modeling.db           # Model & actual forecasts 
|    ├── exogenous.db          # Exogenous metadata & values
|    └── db_change_log.db      # Audit trail 
|    
├── logs/                      # Log files
|    └──  setup.log             # Setup run logs
| 
├── credentials/
│    ├── __init__.py
|    └── .secrets              # API keys 
|    
├── src/
|    |
|    ├── models/
|    |   |
│    │   ├── __init__.py
|    |   |   |
|    |   ├── forecasting/      # Prediction logic 
|    |   |   |
|    |   |   ├── __init__.py   
|    |   |   ├── arimax.py     # ARIMA forecasting, SARIMAX, ARIMAX, etc.
|    |   |   └── <add files as needed>
|    |   |    
|    |   ├── trading/          # Trading logic
|    |   |   |
|    |   |   ├── __init__.py   
|    |   |   └── <add files as needed>  
|    |   |
|    |   └── <add directories as needed>    
|    |
|    ├── etl/
|    |   |
│    │   ├── __init__.py
│    │   ├── populate_prices.py
│    │   ├── populate_tickers.py
│    │   ├── update_prices.py
|    |   └── <add files as needed>      
|    |
|    ├── statistics/
|    |   |
│    │   ├── __init__.py
│    │   ├── changepoints.py       # Level shifts, variance shifts, trend changes, etc. 
|    |   ├── smoothers.py          # Smoothing utilities (Exponential, Simple Moving Average, LOWESS, etc.)
|    |   ├── stationarity.py       # Stationarity tests (ADF, KPSS, etc.)  
│    │   ├── transformations.py    # Differencing, log transforms
|    |   └── <add files as needed>  
|    |
|    ├── execution/            # Trade execution 
│    │   ├── __init__.py
|    |   └── <add files as needed> 
|    |
|    ├── visulazations/ 
|    |   |      
│    │   ├── __init__.py
|    |   ├── exploratory_plots.py 
|    |   ├── stock_price_trends.py  
|    |   └── <add files as needed>      
|    |
|    ├── dashboard/            # Dashboard logic (e.g., Flask/Dash)
|    |   |
│    │   ├── __init__.py
|    |   └── <add files as needed>  
|    | 
|    ├── tests/                # Unit tests 
|    |   |
│    │   ├── test_arimax.py
│    │   ├── test_changepoints.py
│    │   ├── test_smoothers.py 
│    │   ├── test_stationarity.py 
│    │   ├── test_transformations.py
|    |   └── <add files as needed> 
|    |
|    ├── utils/                
│    │   ├── __init__.py
│    │   ├── alpaca_utils.py
│    │   ├── db_utils.py
|    |   └── <add files as needed> 
|    |
|    ├── get_tickers.py        # Fetch asset metadata (Alpaca updated with logging)
|    |
|    ├── db_schema.py          # Database schema used during initial setup. 
|    ├── config.py                  # Settings (BASE_URL, DB paths, API endpoints)
|    └── main.py               # Entry point (runs pipeline)
|    
├── setup_env.ps1              # Sets up the `autotrader` environment. 
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
  - `exchange` (TEXT): Exchange (e.g., "NASDAQ").
  - `asset_type` (TEXT): Type (e.g., "Stock").
  - `is_active` (INTEGER): 1 (active) or 0 (inactive).
  - `date_added` (TEXT): Date added (e.g., "2025-03-22").
  - `date_removed` (TEXT): Date removed (e.g., "2025-04-01" or NULL if active).
  - `fetched_at` (TEXT): Timestamp of last fetch (e.g., "2025-03-22 13:00:00").

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