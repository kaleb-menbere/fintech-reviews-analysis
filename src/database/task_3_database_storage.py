"""
Task 3: Store Cleaned Data in PostgreSQL

This script handles the connection to a PostgreSQL database, defines the 
required schema (Banks and Reviews tables), and performs bulk insertion 
of the processed review data from Task 2.
"""

import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2 import extras
import os
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Safely determine the project root
try:
    SCRIPT_PATH = os.path.abspath(__file__)
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_PATH)))
except NameError:
    # Fallback for environments where __file__ is not defined (like notebooks).
    PROJECT_ROOT = os.path.dirname(os.getcwd()) 

# Define Paths and Imports
DATA_PROCESSED_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed')
INPUT_FILENAME = "reviews_with_sentiment_themes.csv"
CONFIG_FILEPATH = os.path.join(PROJECT_ROOT, 'config', 'db_config.py')

# Initialize DB_CONFIG globally
DB_CONFIG = {} 

try:
    # Read the content of the config file directly to avoid import path issues
    # The config file is expected to define a dictionary named DB_CONFIG
    with open(CONFIG_FILEPATH, 'r') as f:
        config_content = f.read()
    
    # Execute the content, defining DB_CONFIG in the global scope
    # This bypasses the need for dynamic sys.path manipulation
    exec(config_content, globals()) 
    
    # Check if DB_CONFIG was successfully defined and is a dictionary
    if 'DB_CONFIG' not in globals() or not isinstance(DB_CONFIG, dict):
        raise ValueError("db_config.py did not define a valid DB_CONFIG dictionary.")

except FileNotFoundError:
    logger.error(f"Failed to find config file: {CONFIG_FILEPATH}")
    logger.error("Please ensure db_config.py exists in the 'config' directory.")
    sys.exit(1)
except Exception as e:
    logger.error(f"Error loading or parsing db_config.py: {e}")
    logger.error("Please ensure the syntax in db_config.py is correct (it should only define the DB_CONFIG dictionary).")
    sys.exit(1)


# --- SQL Schema Definitions ---

# 1. Banks Table: Stores unique bank names
CREATE_BANKS_TABLE = """
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) UNIQUE NOT NULL,
    app_name VARCHAR(100)
);
"""

# 2. Reviews Table: Stores the enriched review data, linked to Banks
CREATE_REVIEWS_TABLE = """
CREATE TABLE IF NOT EXISTS reviews (
    review_pk SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id) ON DELETE CASCADE,
    review_id_generated INTEGER UNIQUE NOT NULL, -- Original index from pandas
    review_text TEXT,
    review_preprocessed TEXT,
    rating INTEGER NOT NULL,
    review_date DATE,
    sentiment_label VARCHAR(10),
    sentiment_score NUMERIC(5, 4),
    identified_theme VARCHAR(50),
    source VARCHAR(50) DEFAULT 'Google Play'
);
"""

# --- Connection and Insertion Functions ---

def create_db_tables(conn):
    """Creates the 'banks' and 'reviews' tables if they don't exist."""
    with conn.cursor() as cur:
        logger.info("Creating 'banks' table...")
        cur.execute(CREATE_BANKS_TABLE)
        logger.info("Creating 'reviews' table...")
        cur.execute(CREATE_REVIEWS_TABLE)
    conn.commit()
    logger.info("Database schema creation complete.")

def insert_banks_data(conn, df: pd.DataFrame) -> dict:
    """
    Inserts unique bank names into the 'banks' table and returns a mapping 
    of bank_name to bank_id. Handles conflicts to ensure idempotency.
    """
    bank_names = df['bank'].unique()
    
    # Assuming app_name is the same as bank_name for this task
    bank_data = [(name, name + ' Mobile App') for name in bank_names]
    
    # INSERT OR IGNORE, and return the ID if inserted/fetch existing ID
    insert_query = sql.SQL("INSERT INTO banks (bank_name, app_name) VALUES (%s, %s) ON CONFLICT (bank_name) DO NOTHING RETURNING bank_id, bank_name;")
    
    bank_id_map = {}
    with conn.cursor() as cur:
        logger.info(f"Inserting {len(bank_names)} unique bank entries...")
        for name, app_name in bank_data:
            try:
                cur.execute(insert_query, (name, app_name))
                result = cur.fetchone()
                if result:
                    # Successfully inserted (returned ID)
                    bank_id_map[result[1]] = result[0]
                else:
                    # Conflict occurred (bank already exists), fetch the existing ID
                    cur.execute(sql.SQL("SELECT bank_id FROM banks WHERE bank_name = %s"), (name,))
                    fetched_id = cur.fetchone()
                    if fetched_id:
                        bank_id_map[name] = fetched_id[0]
                    else:
                        logger.error(f"Failed to find or insert bank: {name}")

            except Exception as e:
                logger.error(f"Error inserting/fetching bank {name}: {e}")

    conn.commit()
    logger.info(f"Bank ID mapping created: {bank_id_map}")
    return bank_id_map

def insert_reviews_data(conn, df: pd.DataFrame, bank_id_map: dict):
    """Performs bulk insertion of review data into the 'reviews' table."""
    logger.info("Preparing reviews data for bulk insertion...")

    # Map bank name to its foreign key (bank_id)
    df['bank_id'] = df['bank'].map(bank_id_map)

    # Convert date string to proper SQL date format and handle NaN/None
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

    # Select the columns matching the database schema for insertion
    review_records = df[[
        'bank_id',
        'review_id_generated',
        'review',
        'review_preprocessed',
        'rating',
        'date',
        'sentiment_label',
        'sentiment_score',
        'identified_theme',
        'source'
    ]].values.tolist()

    # Replace pandas NaN/NaT with None for SQL compatibility
    review_records = [[None if pd.isna(item) or (item is pd.NaT) else item for item in row] for row in review_records]

    # Define the target table and columns
    table_name = 'reviews'
    columns = [
        'bank_id', 'review_id_generated', 'review_text', 'review_preprocessed', 
        'rating', 'review_date', 'sentiment_label', 'sentiment_score', 
        'identified_theme', 'source'
    ]
    
    # Use ON CONFLICT (review_id_generated) DO NOTHING to handle existing records
    insert_query = sql.SQL(
        "INSERT INTO {} ({}) VALUES %s ON CONFLICT (review_id_generated) DO NOTHING"
    ).format(sql.Identifier(table_name), sql.SQL(', ').join(map(sql.Identifier, columns)))
    
    # Use execute_values for efficient bulk insertion
    with conn.cursor() as cur:
        logger.info(f"Starting bulk insertion of {len(review_records)} review records...")
        try:
            extras.execute_values(cur, insert_query, review_records, template=None, page_size=1000)
            conn.commit()
            logger.info("Bulk insertion complete.")
        except Exception as e:
            logger.error(f"Error during bulk insert: {e}")
            conn.rollback()

def main():
    """Main function to run the PostgreSQL storage pipeline."""
    
    input_filepath = os.path.join(DATA_PROCESSED_PATH, INPUT_FILENAME)
    
    # 1. Load Data
    try:
        df = pd.read_csv(input_filepath, encoding='utf-8')
        logger.info(f"Loaded {len(df)} enriched reviews for database storage.")
        
        # Add a default 'source' column if it's missing (as per schema)
        if 'source' not in df.columns:
             df['source'] = 'Google Play'
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_filepath}. Run Task 2 analysis first.")
        return 

    conn = None
    try:
        # 2. Establish Connection
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("Successfully connected to PostgreSQL database.")

        # 3. Create Tables
        create_db_tables(conn)

        # 4. Insert Banks and get mapping
        bank_id_map = insert_banks_data(conn, df)
        
        # 5. Insert Reviews
        insert_reviews_data(conn, df, bank_id_map)
        
        logger.info("\n✨ Task 3: Data successfully loaded into PostgreSQL.")

    except psycopg2.OperationalError as e:
        logger.error(f"PostgreSQL Connection Error: {e}")
        logger.error("Please ensure your PostgreSQL server is running and the credentials in config/db_config.py are correct.")
        logger.error("Also, ensure the database 'bank_reviews' exists.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            logger.info("PostgreSQL connection closed.")


if __name__ == "__main__":
    main()