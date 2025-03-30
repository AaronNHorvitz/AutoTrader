# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / 'databases'
LOG_DIR = BASE_DIR / 'logs'
CREDENTIALS_DIR = BASE_DIR / 'credentials'