# setup.py
import sqlite3
import os
import logging
from pathlib import Path
from src.db_schema import DATABASES  # Import database schemas

# Setup logging
logging.basicConfig(
    filename='logs/setup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define database directory
DB_DIR = Path('databases')
DB_DIR.mkdir(exist_ok=True)  # Create directory if it doesn't exist

def setup_databases():
    """Check and create databases if they don't exist."""
    for db_name, schemas in DATABASES.items():
        db_path = DB_DIR / db_name
        # Check if database exists
        if not db_path.exists():
            logging.info(f"Database {db_name} not found. Creating...")
            print(f"Creating {db_name}...")
        else:
            logging.info(f"Database {db_name} found. Checking tables...")
            print(f"Database {db_name} exists. Checking tables...")

        # Connect and create tables
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            for schema in schemas:
                cursor.execute(schema)
            conn.commit()
            logging.info(f"Tables in {db_name} created/verified successfully.")
            print(f"Tables in {db_name} created/verified.")
        except sqlite3.Error as e:
            logging.error(f"Error with {db_name}: {e}")
            print(f"Error with {db_name}: {e}")
        finally:
            conn.close()

    logging.info("All databases initialized successfully!")
    print("All databases initialized successfully!")

if __name__ == "__main__":
    setup_databases()