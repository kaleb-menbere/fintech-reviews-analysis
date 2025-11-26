"""
Google Play Store Review Scraper for Ethiopian Banking Apps
10 Academy Week 2 Challenge - Task 1: Data Collection & Preprocessing
"""

import pandas as pd
import time
import logging
from google_play_scraper import reviews_all, Sort
from datetime import datetime
import sys
import os

# --- Configuration for File Paths ---
# Calculates the path to the 'data/raw' folder, assuming the script is run from 
# within the project structure (e.g., from the root or inside 'src/data_collection').
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_RAW_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')

# 🟢 FIX: Ensure output console encoding is UTF-8 for emojis (Fixes UnicodeEncodeError)
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback for systems that might not support reconfigure
        pass 

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # Ensure file logging also uses UTF-8
        logging.FileHandler('scraping.log', encoding='utf-8'), 
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def preprocess_reviews(reviews: list) -> pd.DataFrame:
    """
    Performs required preprocessing on the raw review data: 
    renaming, date normalization, handling missing data, and removing duplicates.
    
    Args:
        reviews (list): List of raw review dictionaries.
        
    Returns:
        pd.DataFrame: Cleaned and structured DataFrame ready for analysis.
    """
    if not reviews:
        return pd.DataFrame()
        
    df = pd.DataFrame(reviews)
    logger.info(f"Initial raw reviews count: {len(df)}")
    
    # 1. Select and rename required columns for the challenge
    df = df.rename(columns={
        'content': 'review_text',
        'score': 'rating',
        'at': 'date', 
        'bank_name': 'bank' # Renamed from short_name added during scraping
    })
    
    # 2. Add 'source' column and select final columns
    df['source'] = 'Google Play'
    # Specify the required columns for the final CSV deliverable
    required_cols = ['review_text', 'rating', 'date', 'bank', 'source', 'app_name', 'app_id']
    df = df.reindex(columns=required_cols, fill_value=None)

    # 3. Normalize Dates to YYYY-MM-DD format
    # Use errors='coerce' to turn invalid dates into NaT
    df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce').dt.strftime('%Y-%m-%d')
    
    # 4. Handle Missing Data and Remove Duplicates
    initial_count = len(df)
    
    # Drop rows missing essential data (text or rating)
    df.dropna(subset=['review_text', 'rating', 'date'], inplace=True)
    
    # Drop duplicates based on content, bank, and date (highly unique combination)
    df.drop_duplicates(subset=['review_text', 'date', 'bank'], inplace=True)
    
    final_count = len(df)
    logger.info(f"Cleaned reviews count: {final_count} (Dropped {initial_count - final_count} rows).")
    
    return df

class BankReviewScraper:
    """Scrapes reviews from Google Play Store for banking apps"""
    
    # 🟢 FIX: Ensure all methods are correctly indented within the class (Fixes AttributeError)
    def __init__(self):
        # 🟢 FIX: Corrected App IDs to ensure reviews are collected
        self.bank_apps = {
            'CBE': {
                'id': 'com.combanketh.mobilebanking', 
                'name': 'Commercial Bank of Ethiopia',
                'short_name': 'CBE'
            },
            'BOA': {
                'id': 'com.boa.boaMobileBanking', 
                'name': 'Bank of Abyssinia',
                'short_name': 'BOA'
            },
            'DASHEN': {
                # Targeting the Super App ID for max reviews
                'id': 'com.dashen.dashensuperapp', 
                'name': 'Dashen Bank (Super App)', 
                'short_name': 'Dashen'
            }
        }
        self.scraping_config = {
            # 🟢 FIX: Set lang=None and country='et' to maximize Ethiopian review collection
            'lang': None, 
            'country': 'et', 
            'sleep_milliseconds': 1000,
            'max_reviews_per_app': 1000 
        }
        self.all_reviews = []
        
    def scrape_single_app(self, app_id, app_name, short_name):
        """Scrape reviews for a single banking app"""
        try:
            logger.info(f"📱 Starting to scrape reviews for {app_name} ({short_name})...")
            
            # Scrape reviews with configured settings
            reviews = reviews_all(
                app_id=app_id,
                lang=self.scraping_config['lang'],
                country=self.scraping_config['country'],
                sort=Sort.MOST_RELEVANT,
                sleep_milliseconds=self.scraping_config['sleep_milliseconds']
            )
            
            # Add bank metadata to each review dictionary
            for review in reviews:
                review['bank_name'] = short_name
                review['app_name'] = app_name
                review['app_id'] = app_id
                review['scraped_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            logger.info(f"✅ Successfully scraped {len(reviews)} reviews for {short_name}")
            return reviews
            
        except Exception as e:
            logger.error(f"❌ Failed to scrape {app_name}: {str(e)}")
            return []
    
    def scrape_all_banks(self):
        """Scrape reviews for all banking apps"""
        logger.info("🚀 Starting review scraping for all banks...")
        logger.info("=" * 60)
        
        total_reviews = 0
        
        for bank_key, app_info in self.bank_apps.items():
            reviews = self.scrape_single_app(
                app_info['id'],
                app_info['name'],
                app_info['short_name']
            )
            
            self.all_reviews.extend(reviews)
            total_reviews += len(reviews)
            
            # Pause between apps to avoid rate limiting
            time.sleep(2)
        
        logger.info(f"🎯 Total raw reviews collected: {total_reviews}")
        return self.all_reviews
    
    def save_to_csv(self, df: pd.DataFrame, filename=None):
        """Save scraped reviews DataFrame to CSV file."""
        if df.empty:
            logger.error("❌ No reviews to save!")
            return None
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Use 'clean' in the filename to indicate it's the post-preprocessing output
            filename = os.path.join(DATA_RAW_PATH, f"bank_reviews_clean_{timestamp}.csv")
        
        # Create data/raw directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save to CSV using UTF-8 encoding
        df.to_csv(filename, index=False, encoding='utf-8')
        
        logger.info(f"💾 Saved {len(df)} cleaned reviews to {filename}")
        return filename
    
    def generate_report(self, df: pd.DataFrame):
        """Generate a summary report of the scraping and preprocessing results"""
        if df.empty:
            logger.error("❌ No data available for report")
            return False
        
        total_reviews = len(df)
        
        print("\n" + "=" * 60)
        print("📊 SCRAPING REPORT")
        print("=" * 60)
        
        print(f"Total Cleaned Reviews Collected: {total_reviews}")
        
        # Reviews per bank
        print("\n📈 Reviews per Bank:")
        bank_counts = df['bank'].value_counts()
        
        for expected_bank in self.bank_apps.values():
            short_name = expected_bank['short_name']
            count = bank_counts.get(short_name, 0)
            status = "✅" if count >= 400 else "⚠️ "
            print(f"  {status} {short_name}: {count} reviews")
        
        # Date range
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df.dropna(subset=['date'], inplace=True)
            if not df.empty:
                print(f"\n📅 Date Range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}")
        
        # Rating distribution
        if 'rating' in df.columns:
            print(f"\n⭐ Rating Distribution:")
            rating_counts = df['rating'].value_counts().sort_index()
            for rating, count in rating_counts.items():
                print(f"  {rating} stars: {count} reviews")
        
        # Requirements check
        banks_with_400 = sum(count >= 400 for count in bank_counts.values)
        requirement_met = total_reviews >= 1200 and banks_with_400 == 3
        
        print(f"\n🎯 TASK 1 REQUIREMENTS:")
        print(f"  Minimum 1200 total reviews: {total_reviews}/1200 {'✅' if total_reviews >= 1200 else '❌'}")
        print(f"  Minimum 400 reviews per bank: {banks_with_400}/3 {'✅' if banks_with_400 == 3 else '❌'}")
        print(f"  Overall Status: {'✅ COMPLETED' if requirement_met else '❌ INCOMPLETE'}")
        
        return requirement_met

def main():
    """Main function to run the scraping and preprocessing process"""
    print("🎯 10 Academy Week 2 Challenge - Task 1: Data Collection")
    print("Google Play Store Review Scraper")
    print("=" * 60)
    
    # Initialize scraper
    scraper = BankReviewScraper()
    
    try:
        # 1. Scrape all banks
        raw_reviews = scraper.scrape_all_banks()
        
        if not raw_reviews:
            logger.error("💥 No reviews were collected. Exiting.")
            return False
        
        # 2. Preprocess the collected data
        df_cleaned = preprocess_reviews(raw_reviews)
        
        if df_cleaned.empty:
            logger.error("💥 All collected reviews were dropped during preprocessing. Exiting.")
            return False

        # 3. Save to CSV
        csv_file = scraper.save_to_csv(df_cleaned)
        
        # 4. Generate report
        requirement_met = scraper.generate_report(df_cleaned)
        
        if requirement_met:
            print(f"\n✨ Task 1 Data Collection COMPLETED SUCCESSFULLY! 🎉")
            print(f"📁 Data saved to: {csv_file}")
            print("➡️  Next: Start Task 2 - Sentiment and Thematic Analysis")
        else:
            print(f"\n⚠️  Task 1 Data Collection INCOMPLETE")
            print("  Some requirements were not met. Check the log above.")
        
        return requirement_met
        
    except Exception as e:
        logger.error(f"💥 Critical error during scraping: {str(e)}")
        return False

if __name__ == "__main__":
    # Ensure the data/raw directory exists before running
    os.makedirs(DATA_RAW_PATH, exist_ok=True)
    
    # Run the scraper
    success = main()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)