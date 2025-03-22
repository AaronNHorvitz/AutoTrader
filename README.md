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
|    |
|    └──  test_notebook/        # ~Play space for experiments
|    
├── Notebooks/
|    |
|    ├── 001_Connecting_to_Alpaca_Tutorial.ipynb   # ~Demos (~e.g., Alpaca API setup)
|    ├── 002_Create_and_Update_Database.ipynb      
|    └── 003_Query_and_Visualize_Data.ipynb              
|
├── databases/
|    |
|    ├── assets.db             # ~Asset metadata, prices, dividends, actions 
|    ├── portfolio_management.db  # ~Holdings, transactions, KPIs 
|    ├── accounting.db         # ~Accounts, balances, cash flows, taxes 
|    ├── modeling.db           # ~Model & actual forecasts 
|    ├── exogenous.db          # ~Exogenous metadata & values
|    └── db_change_log.db      # ~Audit trail 
|    |
├── logs/                      # ~Log files
|    ├── setup.log             # ~Setup run logs
|    └── fetch.log             # ~New 
| 
├── credentials/
|    └── .secrets              # ~API keys 
|    
├── src/
|    |
|    ├── models/
|    |   |
|    |   ├── forecasting/      # ~Prediction logic 
|    |   └── trading/          # ~Trading logic 
|    |
|    ├── etl/
|    |   |
|    |   ├── db_setup/         # ~DB creation scripts (~e.g., setup.sql or .py)
|    |   ├── db_updates/       # ~DB update scripts (~e.g., insert prices, exogenous)
|    |   └── data_fetch/       # ~New (~fetch scripts ~Alpaca/YFinance/FRED)
|    |
|    ├── execution/            # ~Trade execution (~Alpaca API calls)
|    ├── dashboard/            # ~Dashboard logic (~e.g., Flask/Dash)
|    |   ├── templates/        # ~HTML 
|    |   └── static/           # ~CSS, JS 
|    | 
|    ├── tests/                # ~Unit tests 
|    |   ├── test_models.py    # ~Test forecasting/trading
|    |   └── test_etl.py       # ~Test DB setup/updates
|    |
|    ├── utils/                # ~Helper functions (~e.g., logging, date utils)
|    ├── config.py             # ~Settings (~BASE_URL, DB paths, API endpoints)
|    ├── get_tickers.py        # ~Fetch asset metadata (~Alpaca ~updated with logging)
|    └── main.py               # ~Entry point (~runs pipeline)
|    
├── setup.py                   # ~Creates DBs, populates initial metadata
├── .gitignore                 # ~Protects secrets, logs, DBs (~e.g., *.db, .secrets)
├── environment.yaml           # ~Anaconda env (~dependencies ~e.g., pandas, yfinance)
└── README.md                  # ~Project overview (~this file)
```
