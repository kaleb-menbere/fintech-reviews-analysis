"""
Data Processing Script
10 Academy Week 2 Challenge - Task 1: Apply Review Count Constraints
This script loads the initially cleaned data and applies the business logic
to constrain review counts per bank between 400 and 700.
"""

import pandas as pd
import logging
import os
import sys

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
    
    print(f"Total Final Reviews: {total_reviews}")
    print(f"\n📈 Reviews per Bank (Target: {MIN_REVIEWS}-{MAX_REVIEWS}):")
    
    all_banks_constrained = True
    for bank, count in bank_counts.items():
        status = "✅"
        if count > MAX_REVIEWS:
            status = "❌"
            all_banks_constrained = False
        elif count < MIN_REVIEWS:
            status = "⚠️ "
            
        print(f"  {status} {bank}: {count} reviews")

    print(f"\n🎯 Processing Status:")
    print(f"  All banks are sampled to Max ({MAX_REVIEWS}): {'✅' if all_banks_constrained else '⚠️ '}")
    print(f"  Final Dataset Location: {final_filepath}")
    print("=" * 60)


def main():
    """Main function to run the data processing pipeline."""
    input_filepath = os.path.join(DATA_RAW_PATH, INPUT_FILENAME)
    output_filepath = os.path.join(DATA_PROCESSED_PATH, OUTPUT_FILENAME)
    
    # 1. Load the initial clean data
    df = load_data(input_filepath)
    
    if df.empty:
        return 
        
    # 2. Apply the review count constraints
    df_constrained = apply_review_constraints(df)
    
    # 3. Save the final processed data
    save_data(df_constrained, output_filepath)
    
    # 4. Generate report
    generate_report(df_constrained, output_filepath)

if __name__ == "__main__":
    main()