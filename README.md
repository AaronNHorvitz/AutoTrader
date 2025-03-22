# STAT 656 Autotrader

Welcome to the STAT 656 Autotrader by the Data Science Daytraders. This project helps you fetch a list of all stock and ETF tickers currently tracked by Alpaca, store them in a SQLite database, and then execute an autotrader.

## Prerequisites

- **Python 3.11+**: Installed on your system.
- **Libraries**: `pandas`, `requests`, `sqlite3` (standard), and `alpaca-trade-api` (~`pip install alpaca-trade-api`).

## Step 1: Set Up Your Environment

### 1. Install Git
- **Windows**: [git-scm.com](https://git-scm.com/download/win).
- **Mac**: `brew install git` (~`brew.sh`) or [git-scm.com](https://git-scm.com/download/mac).
- **Check**: `git --version`.

### 2. Install Anaconda
- **Download Anaconda**: [Anaconda.com](https://www.anaconda.com/products/distribution)
- **Install**: Run the downloaded installer and follow the installation instructions.
- **Verify**: Open your terminal and type `conda --version` to ensure Anaconda is installed correctly.

### 3. Check SQLite Installation
- **Windows/Mac**: SQLite comes pre-installed with Anaconda. To verify, open a terminal and run:
  ```bash
  sqlite3 --version
  ```
- If not available, install it using:
  ```bash
  conda install -c conda-forge sqlite
  ```

### 4. Clone the Repo
- **Terminal**: 
  ```bash
  git clone https://github.com/YOUR_USERNAME/stat_656_autotrader.git
  cd stat_656_autotrader
  ```

## Step 2: Get an Alpaca Account

Before you can download tickers, you need an Alpaca account and API keys. Alpaca offers free paper trading (~$0)—no real money, just data and trades to play with. Here’s how to set it up:

### 1. Sign Up
- **Visit**: [Alpaca Markets](https://alpaca.markets/)
- **Action**: Click “Get Started” (~top right) or “Sign Up” (~center).
- **Details**: Enter your email and create a password.

### 2. Switch to Paper Trading
- **Log In**: Head to [app.alpaca.markets](https://app.alpaca.markets/).
- **Toggle**: Top left corner—switch from “Live” to “Paper”.
- Paper trading gives you API access without funding.

### 3. Generate API Keys
- **Dashboard**: Scroll to “Your API Keys” (~right side).
- **Click**: “Generate New Keys” (~or “View” if already there).

### 4. Type the Key and Secret into the .secrets file and save.
- **Create**: Create an empty text file.
- **Copy**: Grab your **API Key ID** (e.g., `PK123...`) and **Secret Key** (e.g., `abc...xyz`).
- **Paste**: Paste your credentials in the text file so it looks like this:
  ```
  Key="put_key_here"
  Secret="put_secret_here"
  ```
- **Save**: Save your credentials as '.secrets' in the 'credentials' directory.


## File Structure/ Project Architecture

```
stat_656_autotrader/
├── Sandbox/            
|    ├── experiment1/        # ~Play space (~optional)
├── Notebooks/    
|    ├── 001 Connecting to Alpaca Tutorial.ipynb.ipynb   # ~Demos
├── databases/    
|    ├── stock_prices.db     # ~Tickers, OHLC (~3.75 GB)
|    ├── exogenous.db        # ~Exogenous (~TBD)
|    ├── transactions.db     # ~Trades (~TBD)
|    └── prior_forecasts.db  # ~Forecast checks (~TBD)
├── logs/                    # ~Log files (~e.g., setup.log)
|    └── setup.log           # ~Setup run logs
├── credentials/
|    └── .secrets            # ~Keys (~Key='...')
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
|    ├── get_tickers.py      # ~Ticker fetch (~updated with logging)
|    └── main.py             # ~Entry (~optional)
├── setup.py                 # ~Creates DBs, populates tickers
├── .gitignore               # ~Protect files
├── environment.yaml         # ~Anaconda
└── README.md                # ~Readme.md file 
```

For more details, see Alpaca’s guide: [Connect to Alpaca API](https://alpaca.markets/learn/connect-to-alpaca-api).
