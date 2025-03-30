# setup.py
import sqlite3
import logging
from pathlib import Path
from src.db_schema import DATABASES  # Database schemas

# Setup directories
DB_DIR = Path('databases')
DB_DIR.mkdir(exist_ok=True)

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    filename=LOG_DIR / 'setup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_databases():
    """Check databases and create missing databases and tables."""
    for db_name, schemas in DATABASES.items():
        db_path = DB_DIR / db_name

        if not db_path.exists():
            logging.info(f"Database {db_name} not found. Creating...")
            print(f"Creating {db_name}...")
        else:
            logging.info(f"Database {db_name} exists. Checking tables...")
            print(f"Database {db_name} exists. Checking tables...")

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")  # Enable FK constraints
            
            # Execute schema creations
            for schema in schemas:
                cursor.execute(schema)
                
            conn.commit()
            logging.info(f"Tables in {db_name} created/verified successfully.")
            print(f"Tables in {db_name} created/verified.")

        except sqlite3.Error as e:
            logging.error(f"Error setting up {db_name}: {e}")
            print(f"Error setting up {db_name}: {e}")

        finally:
            conn.close()

    logging.info("All databases initialized successfully!")
    print("All databases initialized successfully!")

if __name__ == "__main__":
    setup_databases()