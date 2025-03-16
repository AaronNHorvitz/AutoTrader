# STAT 656 Autotrader

Welcome to the STAT 656 Autotrader by the Data Science Daytraders. This project helps you fetch a list of all stock and ETF tickers (~11,000+) currently tracked by Alpaca, store them in a SQLite database, and then execute an autotrader. 

## Prerequisites

- **Python 3.11+**: Installed on your system.
- **Libraries**: `pandas`, `requests`, `sqlite3` (standard), and `alpaca-trade-api` (~`pip install alpaca-trade-api`).

## Step 1: Set Up Your Environment

### 1. Install Git
- **Windows**: [git-scm.com](https://git-scm.com/download/win).
- **Mac**: `brew install git` (~`brew.sh`) or [git-scm.com](https://git-scm.com/download/mac).
- **Check**: `git --version`.

### 2. Clone the Repo
- **Terminal**: 
  ```bash
  git clone https://github.com/YOUR_USERNAME/stat_656_autotrader.git
  cd stat_656_autotrader


## Step 3: Get an Alpaca Account

Before you can download tickers, you need an Alpaca account and API keys. Alpaca offers free paper trading (~$0)—no real money, just data and trades to play with. Here’s how to set it up:

### 1. Sign Up
- **Visit**: [Alpaca Markets](https://alpaca.markets/)
- **Action**: Click “Get Started” (~top right) or “Sign Up” (~center).
- **Details**: Enter your email and create a password.
- **Result**: You’re in! (~welcome email lands quick).

### 2. Switch to Paper Trading
- **Log In**: Head to [app.alpaca.markets](https://app.alpaca.markets/).
- **Toggle**: Top left corner—switch from “Live” to “Paper”.
- **Why**: Paper trading gives you API access without funding (~perfect for testing!).

### 3. Generate API Keys
- **Dashboard**: Scroll to “Your API Keys” (~right side).
- **Click**: “Generate New Keys” (~or “View” if already there).
- **Copy**: Grab your **API Key ID** (e.g., `PK123...`) and **Secret Key** (e.g., `abc...xyz`).
- **Time**: ~5 minutes (~3:55 PM PDT)—you’re API-ready!

### 4. Type the Key and Secret into the .secrets file and save. 
```
Key="put_key_here"
Secret="put_secret_here"
```

For more details, see Alpaca’s guide: [Connect to Alpaca API](https://alpaca.markets/learn/connect-to-alpaca-api).

## Step 5: Install Dependencies
-- Instructions to run the 'environment.yaml' file--


# File Structure
```
stat_656_autotrader/
├── Sandbox/            
|    ├── experiment1/        # ~Play space (~optional)
├── Notebooks/    
|    ├── get_tickers.ipynb   # ~Demos
├── databases/    
|    ├── stock_prices.db     # ~Tickers, OHLC (~3.75 GB)
|    ├── exogenous.db        # ~Exogenous (~TBD)
|    ├── transactions.db     # ~Trades (~TBD)
|    └── prior_forecasts.db  # ~Forecast checks (~TBD)
├── logs/                    # ~Log files (~e.g., setup.log)
|    └── setup.log           # ~Setup run logs
├── src/         
|    ├── models/             
|    |   ├── forecasting/    # ~Prediction logic
|    |   └── stock_trading/  # ~Trading logic
|    ├── etl/             
|    |   ├── db_setup/       # ~DB creation (~setup.sql moved here)
|    |   └── db_updates/     # ~DB updates
|    ├── execution/          # ~Trade execution
|    ├── dashboard/          # ~Dashboard logic
|    |   ├── templates/      # ~HTML (~e.g., dashboard.html)
|    |   └── static/         # ~CSS, JS
|    ├── test/               # ~Unit tests
|    ├── utils/              # ~Helpers 
|    ├── config.py           # ~BASE_URL, settings
|    ├── .secrets            # ~Keys (~Key='...')
|    ├── get_tickers.py      # ~Ticker fetch (~updated with logging)
|    └── main.py             # ~Entry (~optional)
├── setup.py                 # ~Creates DBs, populates tickers
├── .gitignore               # ~Protect files
├── environment.yaml         # ~Anacond
```

