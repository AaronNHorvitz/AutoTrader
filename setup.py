# setup.py
import sqlite3
import logging
from pathlib import Path
from src.db_schema import DATABASES  # Database schemas

# Define absolute path relative to setup.py's location
BASE_DIR = Path(__file__).parent
DB_DIR = BASE_DIR / 'databases'
DB_DIR.mkdir(exist_ok=True)

LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_DIR / 'setup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_databases():
    """Initialize databases and tables based on defined schemas."""
    for db_name, schemas in DATABASES.items():
        db_path = DB_DIR / db_name

        db_exists = db_path.exists()
        logging.info(f"{'Found' if db_exists else 'Creating'} database: {db_name}")
        print(f"{'Database exists:' if db_exists else 'Creating'} {db_name}...")

        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON;")  # Enable FK constraints
                cursor = conn.cursor()

                for schema in schemas:
                    cursor.execute(schema)

                conn.commit()

            logging.info(f"Database '{db_name}' tables verified successfully.")
            print(f"Tables in '{db_name}' created/verified successfully.")

        except sqlite3.Error as e:
            logging.error(f"Error setting up '{db_name}': {e}")
            print(f"Error setting up '{db_name}': {e}")

    logging.info("All databases initialized successfully.")
    print("All databases initialized successfully.")

if __name__ == "__main__":
    setup_databases()