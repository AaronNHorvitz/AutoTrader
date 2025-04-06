from pathlib import Path

# Base directory of the project (root: stat_656_autotrader/)
BASE_DIR = Path(__file__).resolve().parent.parent  # Two .parents to reach stat_656_autotrader/ from src/

# Directories relative to BASE_DIR
DB_DIR = BASE_DIR / 'databases'
LOG_DIR = BASE_DIR / 'logs'
CREDENTIALS_DIR = BASE_DIR / 'credentials'

