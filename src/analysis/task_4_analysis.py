"""
Task 4: Comprehensive Analysis, Visualization, and Reporting

This script connects to the PostgreSQL database, retrieves the necessary data, 
performs bank comparisons, generates key visualizations (KPIs), and structures 
the raw analysis needed for the final report.
"""

import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import logging
from datetime import datetime
from wordcloud import WordCloud # Added for the Word Cloud visualization requirement

# --- Setup and Configuration Loading (Identical to Task 3) ---

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Safely determine the project root
try:
    SCRIPT_PATH = os.path.abspath(__file__)
    # Adjusted to assume standard project structure for a more robust path
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_PATH))) 
except NameError:
    PROJECT_ROOT = os.path.dirname(os.getcwd()) 

# Assuming 'config' is a directory one level up from the task directory
CONFIG_FILEPATH = os.path.join(PROJECT_ROOT, 'config', 'db_config.py')
REPORTING_OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'reports', 'task_4_output')

# Ensure output directory exists
os.makedirs(REPORTING_OUTPUT_DIR, exist_ok=True)

DB_CONFIG = {} 
try:
    # Attempt to load configuration (assuming config/db_config.py structure)
    # Note: In a real environment, this might be better done by importing or reading a JSON/YAML.
    # We maintain the original method for code continuity.
    config_path_attempt = os.path.join(os.path.dirname(os.getcwd()), 'config', 'db_config.py')
    if not os.path.exists(config_path_attempt):
        logger.warning(f"DB config file not found at {config_path_attempt}. Attempting alternative path.")
        
    config_content = ""
    # Simplified logic assuming a predictable config location relative to task folder
    if os.path.exists(config_path_attempt):
        with open(config_path_attempt, 'r') as f:
            config_content = f.read()
    else:
         # Fallback to current directory for testing if path fails
        current_dir_config = os.path.join(os.getcwd(), 'db_config.py')
        if os.path.exists(current_dir_config):
             with open(current_dir_config, 'r') as f:
                config_content = f.read()
        else:
             raise FileNotFoundError(f"db_config.py not found at expected paths.")
        
    exec(config_content, globals()) 
    if 'DB_CONFIG' not in globals() or not isinstance(DB_CONFIG, dict):
        raise ValueError("db_config.py did not define a valid DB_CONFIG dictionary.")
except Exception as e:
    logger.error(f"Error loading or parsing db_config.py: {e}")
    # In a runnable environment, we would exit here, but for generation, we continue.
    # sys.exit(1)


# --- SQL Queries for Data Extraction ---

# 1. Monthly Sentiment Trend (for Line Plot)
SQL_MONTHLY_TREND = """
SELECT
    EXTRACT(YEAR FROM T1.review_date) AS review_year,
    EXTRACT(MONTH FROM T1.review_date) AS review_month,
    T2.bank_name,
    COUNT(T1.review_pk) AS total_reviews,
    ROUND(AVG(T1.sentiment_score)::numeric, 4) AS average_sentiment
FROM
    reviews T1
JOIN
    banks T2 ON T1.bank_id = T2.bank_id
WHERE
    T1.review_date IS NOT NULL
GROUP BY
    review_year,
    review_month,
    T2.bank_name
ORDER BY
    review_year,
    review_month,
    T2.bank_name;
"""

# 2. Rating Distribution (for Histogram)
SQL_RATING_DISTRIBUTION = """
SELECT
    T2.bank_name,
    T1.rating,
    COUNT(T1.review_pk) AS rating_count
FROM
    reviews T1
JOIN
    banks T2 ON T1.bank_id = T2.bank_id
GROUP BY
    T2.bank_name,
    T1.rating
ORDER BY
    T2.bank_name,
    T1.rating;
"""

# 3. Theme Performance and Sample Reviews (for Analysis and Word Cloud)
SQL_THEME_ANALYSIS = """
SELECT
    T2.bank_name,
    T1.review_text,
    T1.sentiment_score,
    T1.identified_theme
FROM
    reviews T1
JOIN
    banks T2 ON T1.bank_id = T2.bank_id
WHERE
    T1.identified_theme IS NOT NULL;
"""

# --- Visualization Functions ---

def generate_monthly_trend_plot(df_trend, output_dir):
    """Generates and saves the Monthly Sentiment Trend Line Plot."""
    logger.info("Generating Monthly Sentiment Trend Plot...")
    
    # --- Date Conversion Logic ---
    try:
        # Convert year/month components to a datetime object
        year_str = df_trend['review_year'].astype(int).astype(str)
        month_str = df_trend['review_month'].astype(int).astype(str)
        dates_str = year_str + '-' + month_str + '-01'
        df_trend['date'] = pd.to_datetime(dates_str, format='%Y-%m-%d')
    except ValueError as e:
        logger.error(f"Date conversion error: {e}")
        raise
        
    
    plt.figure(figsize=(14, 7))
    sns.lineplot(
        data=df_trend, 
        x='date', 
        y='average_sentiment', 
        hue='bank_name', 
        marker='o'
    )
    plt.title('Monthly Average Sentiment Trend by Bank (Time Series)')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment Score (Higher is Better)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the file
    filepath = os.path.join(output_dir, 'sentiment_trend.png')
    plt.savefig(filepath)
    
    # --- ADDED: Display the plot interactively ---
    plt.show() 
    
    plt.close()
    logger.info(f"Saved: {filepath}")

def generate_rating_distribution_plot(df_rating, output_dir):
    """Generates and saves the Rating Distribution Plot (Bar/Histogram)."""
    logger.info("Generating Rating Distribution Plot...")
    
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=df_rating,
        x='rating',
        y='rating_count',
        hue='bank_name',
        palette='viridis'
    )
    plt.title('Rating Distribution (1-5 Stars) by Bank')
    plt.xlabel('Rating')
    plt.ylabel('Number of Reviews')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    # Save the file
    filepath = os.path.join(output_dir, 'rating_distribution.png')
    plt.savefig(filepath)
    
    # --- ADDED: Display the plot interactively ---
    plt.show() 
    
    plt.close()
    logger.info(f"Saved: {filepath}")

def generate_word_cloud(df_themes, output_dir):
    """Generates and saves a Word Cloud based on pain points (low sentiment reviews)."""
    logger.info("Generating Word Cloud for Pain Points...")
    
    # 1. Filter for low sentiment reviews (Pain Points)
    pain_point_reviews = df_themes[df_themes['sentiment_score'] < 0.4]
    
    # 2. Combine all review text into a single string
    text = " ".join(review for review in pain_point_reviews.review_text.astype(str))
    
    # 3. Generate the word cloud
    wordcloud = WordCloud(
        width=1600, 
        height=800, 
        background_color='white', 
        min_font_size=10, 
        colormap='magma'
    ).generate(text)
    
    plt.figure(figsize=(16, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.title('Common Keywords in Low Sentiment (Pain Point) Reviews', fontsize=20)
    
    # Save the file
    filepath = os.path.join(output_dir, 'keyword_cloud_pain_points.png')
    plt.savefig(filepath)
    
    # --- ADDED: Display the plot interactively ---
    plt.show()
    
    plt.close()
    logger.info(f"Saved: {filepath}")

# --- Core Analysis and Reporting Function ---

def run_task_4_analysis():
    """Connects to DB, runs queries, generates visualizations, and performs analysis."""
    conn = None
    try:
        # 1. Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("Successfully connected to PostgreSQL for Task 4 analysis.")

        # 2. Extract Data using SQL
        df_trend = pd.read_sql(SQL_MONTHLY_TREND, conn)
        df_rating = pd.read_sql(SQL_RATING_DISTRIBUTION, conn)
        df_themes = pd.read_sql(SQL_THEME_ANALYSIS, conn)
        logger.info(f"Extracted {len(df_themes)} themed records for analysis.")

        # 3. Generate Visualizations (3 Plots: Trend, Distribution, Word Cloud)
        generate_monthly_trend_plot(df_trend, REPORTING_OUTPUT_DIR)
        generate_rating_distribution_plot(df_rating, REPORTING_OUTPUT_DIR)
        generate_word_cloud(df_themes, REPORTING_OUTPUT_DIR) # Fulfills the 'keyword cloud' requirement
        
        # 4. Perform Insights Generation (This will feed the final report)
        insights = generate_insights(df_themes)
        
        # 5. Output Raw Analysis Data for Report
        insights_filepath = os.path.join(REPORTING_OUTPUT_DIR, 'raw_insights.txt')
        with open(insights_filepath, 'w', encoding='utf-8') as f:
            f.write("--- BANK PERFORMANCE INSIGHTS ---\n\n")
            for bank, data in insights.items():
                f.write(f"BANK: {bank}\n")
                f.write("----------------------------\n")
                f.write(f"TOP DRIVERS:\n{data['drivers']}\n\n")
                f.write(f"TOP PAIN POINTS:\n{data['pain_points']}\n\n")
                f.write("-" * 30 + "\n\n")
        logger.info(f"Saved raw insights to {insights_filepath}")

        logger.info(f"\n✨ Task 4: Analysis and Visualizations saved to '{REPORTING_OUTPUT_DIR}'")


    except psycopg2.OperationalError as e:
        logger.error(f"PostgreSQL Connection Error: {e}")
        logger.error("Ensure server is running and config/db_config.py is correct.")
    except Exception as e:
        # Log a more detailed error if possible
        logger.error(f"An unexpected error occurred during Task 4: {e}")
        # Log the traceback for debugging
        import traceback
        logger.error(traceback.format_exc())
    finally:
        if conn:
            conn.close()
            logger.info("PostgreSQL connection closed.")

# --- Helper function for identifying Drivers/Pain Points ---

def generate_insights(df_themes):
    """
    Identifies 2+ drivers (positive sentiment) and pain points (negative sentiment) 
    per bank based on thematic clustering.
    """
    insights = {}
    banks = df_themes['bank_name'].unique()

    for bank in banks:
        bank_df = df_themes[df_themes['bank_name'] == bank]
        
        # Calculate Average Sentiment per Theme
        theme_summary = bank_df.groupby('identified_theme').agg(
            avg_sentiment=('sentiment_score', 'mean'),
            count=('sentiment_score', 'count')
        ).reset_index()
        
        # Filter for sufficient data points (e.g., at least 10 reviews per theme)
        theme_summary = theme_summary[theme_summary['count'] > 10]

        # Drivers (High positive sentiment themes)
        drivers = theme_summary.sort_values(by='avg_sentiment', ascending=False).head(3)
        
        # Pain Points (Low/Negative sentiment themes)
        pain_points = theme_summary.sort_values(by='avg_sentiment', ascending=True).head(3)

        insights[bank] = {
            'drivers': drivers.to_string(index=False),
            'pain_points': pain_points.to_string(index=False),
        }
        
    return insights

if __name__ == "__main__":
    run_task_4_analysis()