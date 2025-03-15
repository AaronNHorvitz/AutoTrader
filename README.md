# Alpaca Ticker Downloader

Welcome to the STAT 656 Autotrader. This project helps you fetch a list of all stock and ETF tickers (~11,000+) currently tracked by Alpaca and store them in a SQLite database and then execute the autotrader. 

## Prerequisites

- **Python 3.8+**: Installed on your system (~laptop-friendly!).
- **Libraries**: `pandas`, `requests`, `sqlite3` (standard), and `alpaca-trade-api` (~`pip install alpaca-trade-api`).
- **Storage**: ~1–2 MB free (~22 TB? You’re golden!).
- **Time**: ~5–10 minutes to set up (~fun and fast!).

## Step 1: Get an Alpaca Account

Before you can download tickers, you need an Alpaca account and API keys. Alpaca offers free paper trading (~$0)—no real money, just data and trades to play with. Here’s how to set it up:

### 1. Sign Up
- **Visit**: [Alpaca Markets](https://alpaca.markets/)
- **Action**: Click “Get Started” (~top right) or “Sign Up” (~center).
- **Details**: Enter your email and create a password (~5 minutes, ~3:50 PM PDT).
- **Result**: You’re in! (~welcome email lands quick).

### 2. Switch to Paper Trading
- **Log In**: Head to [app.alpaca.markets](https://app.alpaca.markets/).
- **Toggle**: Top left corner—switch from “Live” to “Paper” (~default for newbies, ~$0 trades).
- **Why**: Paper trading gives you API access without funding (~perfect for testing!).

### 3. Generate API Keys
- **Dashboard**: Scroll to “Your API Keys” (~right side).
- **Click**: “Generate New Keys” (~or “View” if already there).
- **Copy**: Grab your **API Key ID** (e.g., `PK123...`) and **Secret Key** (e.g., `abc...xyz`).
  - **Tip**: Save these somewhere safe (~Secret Key shows once unless regenerated!).
- **Time**: ~5 minutes (~3:55 PM PDT)—you’re API-ready!

### 4. Verify Setup
- **Check**: Log out, log back in (~Paper mode), see keys (~all set!).
- **Next**: You’ve got the keys to unlock ~11,000+ tickers—let’s code!

For more details, see Alpaca’s guide: [Connect to Alpaca API](https://alpaca.markets/learn/connect-to-alpaca-api).

## Step 2: Install Dependencies
Fire up your terminal (~or IDE) and install the Alpaca Python SDK:

```bash
pip install alpaca-trade-api