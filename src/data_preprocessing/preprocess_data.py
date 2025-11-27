"""
Data Processing Script
10 Academy Week 2 Challenge - Task 1: Apply Review Count Constraints
This script loads the initial raw data, performs cleaning (duplicates, missing values, date normalization),
filters for English language, and applies the business logic to constrain review counts 
per bank between 400 and 700.

NOTE: This script requires the 'langdetect' library. Please ensure all dependencies 
listed in requirements.txt are installed via 'pip install -r requirements.txt'.
"""

import pandas as pd
import logging
import os
import sys
# Import for language detection
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Set seed for reproducibility in langdetect (optional but good practice)
DetectorFactory.seed = 42

# --- Configuration for File Paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_RAW_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')
DATA_PROCESSED_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed')

INPUT_FILENAME = "reviews_initial_clean.csv"
OUTPUT_FILENAME = "final_bank_reviews_constrained.csv"

# Define constraints
MIN_REVIEWS = 400
MAX_REVIEWS = 700

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('processing.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def perform_initial_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles standard cleaning tasks: column validation, removing duplicates, 
    dropping missing values, and normalizing the 'date' column.
    """
    initial_count = len(df)
    logger.info("Starting initial cleaning: duplicates, missing values, and date normalization.")
    
    # --- NEW: Column Validation and Renaming ---
    REQUIRED_COLS = ['review', 'rating', 'date', 'bank']
    
    # Attempt to rename common alternative column names from scraper output
    COL_MAPPING = {
        'review_text': 'review', # Added: maps the user's provided column name
        'content': 'review',     # Review text often scraped as 'content'
        'appId': 'bank',         # App ID often used to identify the bank
        'score': 'rating',       # Rating score often scraped as 'score'
        'at': 'date'             # Date often scraped as 'at'
    }

    # Apply renaming only if the alternative name exists in the DataFrame
    rename_dict = {
        old_name: new_name for old_name, new_name in COL_MAPPING.items() 
        if old_name in df.columns
    }
    
    if rename_dict:
        df.rename(columns=rename_dict, inplace=True)
        logger.info(f"Renamed columns: {rename_dict}")

    # Check if all critical columns are now present
    missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing_cols:
        logger.critical(f"FATAL ERROR: The following critical columns are still missing after renaming: {missing_cols}. Please inspect {INPUT_FILENAME} column headers.")
        logger.critical(f"Available columns: {list(df.columns)}")
        return pd.DataFrame() # Return empty DataFrame to stop execution

    # ------------------------------------------

    # 1. Remove Duplicates based on review text and bank name
    # Now that renaming is done, 'review', 'bank', and 'date' columns exist.
    df.drop_duplicates(subset=['review', 'bank', 'date'], inplace=True)
    logger.info(f"Removed {initial_count - len(df)} duplicate rows.")
    current_count = len(df)

    # 2. Handle Missing Data in critical columns
    # We drop rows where the review text, rating, date, or bank is missing.
    critical_cols = ['review', 'rating', 'date', 'bank']
    df.dropna(subset=critical_cols, inplace=True)
    logger.info(f"Removed {current_count - len(df)} rows with missing critical data.")
    
    # Ensure 'review' column is explicitly string type before processing
    df['review'] = df['review'].astype(str)
    
    # 3. Normalize Dates to YYYY-MM-DD format
    try:
        # Convert to datetime objects
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        # Drop any rows where date conversion failed
        df.dropna(subset=['date'], inplace=True)
        # Format dates as YYYY-MM-DD string
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        logger.info("Date column successfully normalized to YYYY-MM-DD format.")
    except Exception as e:
        logger.error(f"Date normalization failed: {e}. Dates may be inconsistent.")

    logger.info(f"Initial cleaning complete. Total reviews remaining: {len(df)}")
    return df

def is_english(text: str) -> bool:
    """Detects if the given text is English."""
    if pd.isna(text) or not text.strip():
        return False
    try:
        # Use only a subset of the text for potentially faster detection on long strings
        return detect(text[:500]) == 'en'
    except LangDetectException:
        # Handle cases where the text is too short or ambiguous for detection
        return False
    except Exception as e:
        # Catch any other exception during detection
        logger.debug(f"Language detection failed for text: {text[:30]}... Error: {e}")
        return False

def filter_english_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """Filters the DataFrame to include only reviews detected as English."""
    initial_count = len(df)
    
    # Apply language detection
    df['is_english'] = df['review'].apply(is_english)
    
    # Filter the DataFrame
    df_english = df[df['is_english']].drop(columns=['is_english'])
    final_count = len(df_english)
    
    logger.info(f"Language Filtering: Kept {final_count} English reviews (Dropped {initial_count - final_count} non-English/undetectable reviews).")
    
    return df_english


def apply_review_constraints(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies the 400 minimum and 700 maximum review constraint per bank.
    
    - If a bank has > 700 reviews, it randomly samples 700.
    - If a bank has < 400 reviews, it keeps all of them.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
        
    Returns:
        pd.DataFrame: The DataFrame with constrained review counts.
    """
    logger.info("Applying review count constraints (Min: 400, Max: 700) per bank...")
    
    # Group by bank and apply the sampling/filtering logic
    df_constrained = (
        df.groupby('bank', group_keys=False)
        .apply(constrain_group)
    )
    
    # Reset index to clean up the DataFrame after grouping and applying
    df_constrained = df_constrained.reset_index(drop=True)
    
    return df_constrained

def constrain_group(group: pd.DataFrame) -> pd.DataFrame:
    """
    Helper function to apply the constraint logic to each bank group.
    """
    bank_name = group['bank'].iloc[0]
    current_count = len(group)
    
    if current_count > MAX_REVIEWS:
        # Sample down to the maximum limit (700)
        logger.info(f"Bank {bank_name}: {current_count} reviews found. Sampling down to {MAX_REVIEWS} reviews.")
        # Use .sample() to randomly select 700 rows
        return group.sample(n=MAX_REVIEWS, random_state=42) # Using a fixed seed for reproducibility
    
    elif current_count < MIN_REVIEWS:
        # Keep all reviews, but log a warning that the minimum was not met
        logger.warning(f"Bank {bank_name}: Only {current_count} reviews found. Minimum target ({MIN_REVIEWS}) not met. Keeping all.")
        return group
        
    else:
        # The review count is already within the target range (400 <= N <= 700)
        logger.info(f"Bank {bank_name}: {current_count} reviews found. Constraint met. Keeping all.")
        return group

def load_data(filepath: str) -> pd.DataFrame:
    """Loads the CSV file from the raw data directory."""
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
        logger.info(f"Successfully loaded {len(df)} reviews from {filepath}")
        return df
    except FileNotFoundError:
        logger.error(f"Input file not found: {filepath}. Please ensure the scraping script has been run.")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return pd.DataFrame()

def save_data(df: pd.DataFrame, filepath: str):
    """Saves the final processed DataFrame to CSV."""
    # Create data/processed directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    df.to_csv(filepath, index=False, encoding='utf-8')
    logger.info(f"💾 Saved {len(df)} final constrained reviews to {filepath}")

def generate_report(df: pd.DataFrame, final_filepath: str):
    """Generates a final report on the constrained dataset."""
    print("\n" + "=" * 60)
    print("📊 FINAL DATA PROCESSING REPORT")
    print("=" * 60)
    
    bank_counts = df['bank'].value_counts()
    total_reviews = len(df)
    
    print(f"Total Final Reviews (English & Constrained): {total_reviews}")
    print(f"\n📈 Reviews per Bank (Target: {MIN_REVIEWS}-{MAX_REVIEWS}):")
    
    all_banks_constrained = True
    for bank, count in bank_counts.items():
        status = "✅"
        if count > MAX_REVIEWS:
            status = "❌"
            all_banks_constrained = False
        elif count < MIN_REVIEWS:
            status = "⚠️ "
            
        print(f"   {status} {bank}: {count} reviews")

    print(f"\n🎯 Processing Status:")
    print(f"   Review constraint applied to all banks: {'✅' if all_banks_constrained else '⚠️ '}")
    print(f"   Final Dataset Location: {final_filepath}")
    print("=" * 60)


def main():
    """Main function to run the data processing pipeline."""
    input_filepath = os.path.join(DATA_RAW_PATH, INPUT_FILENAME)
    output_filepath = os.path.join(DATA_PROCESSED_PATH, OUTPUT_FILENAME)
    
    # 1. Load the initial clean data
    df = load_data(input_filepath)
    
    if df.empty:
        return 
        
    # 2. Perform initial cleaning (duplicates, missing, date normalization, and column validation)
    df_cleaned = perform_initial_cleaning(df)
    
    if df_cleaned.empty:
        # Stop if column validation failed
        return
        
    # 3. Filter data to include only English language reviews
    df_english = filter_english_reviews(df_cleaned)

    # 4. Apply the review count constraints
    df_constrained = apply_review_constraints(df_english)
    
    # 5. Save the final processed data
    save_data(df_constrained, output_filepath)
    
    # 6. Generate report
    generate_report(df_constrained, output_filepath)

if __name__ == "__main__":
    main()