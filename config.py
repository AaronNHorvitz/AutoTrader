# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # One .parent to reach stat_656_autotrader
DB_DIR = BASE_DIR / 'databases'
LOG_DIR = BASE_DIR / 'logs'
CREDENTIALS_DIR = BASE_DIR / 'credentials'