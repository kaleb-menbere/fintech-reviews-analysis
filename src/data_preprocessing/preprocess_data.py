import pandas as pd
from datetime import datetime

def preprocess_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """Performs required preprocessing on the raw review data."""
    
    # 1. Select and rename required columns
    df = df.rename(columns={
        'content': 'review_text',
        'score': 'rating',
        'at': 'date' 
    })
    
    # Add 'source' column
    df['source'] = 'Google Play'
    
    # Select final columns and ensure proper order
    df = df[['review_text', 'rating', 'date', 'bank_name', 'source', 'app_id']]

    # 2. Normalize Dates
    df['date'] = pd.to_datetime(df['date'], utc=True).dt.strftime('%Y-%m-%d')
    
    # 3. Handle Missing Data
    df.dropna(subset=['review_text', 'rating'], inplace=True)
    
    # 4. Remove Duplicates
    # Check for duplicates based on content and user/date
    df.drop_duplicates(subset=['review_text', 'date', 'bank_name'], inplace=True)
    
    # Rename 'bank_name' to 'bank' for final output consistency
    df.rename(columns={'bank_name': 'bank'}, inplace=True)
    
    print(f"Cleaned reviews: {len(df)}. Duplicates/NaNs removed.")
    return df