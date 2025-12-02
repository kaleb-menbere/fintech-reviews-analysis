🚀 Fintech Customer Experience Analysis

A Data-Driven Review of Ethiopian Banking Apps for Omega Consultancy

This project delivers a comprehensive analysis of Google Play Store reviews for major Ethiopian banking applications. Using NLP, sentiment scoring, and thematic clustering, it provides actionable insights to improve customer experience and inform digital banking strategy.

🏦 Banks Analyzed

Bank

App Name

Review Volume

Commercial Bank of Ethiopia (CBE)

CBE Mobile Banking

📈 High Volume

Bank of Abyssinia (BOA)

Bank of Abyssinia Mobile

⏳ Medium Volume

Dashen Bank

Dashen Mobile Banking

📊 Lower Volume

⚡ Quick Start

🔧 Installation

# Clone the repository
git clone [https://github.com/kaleb-menbere/fintech-reviews-analysis.git](https://github.com/kaleb-menbere/fintech-reviews-analysis.git)
cd fintech-reviews-analysis

# Install dependencies
pip install -r requirements.txt


▶️ Running the Full Analysis Pipeline (4/4 Tasks)

Execute scripts in order from the project root. This sequence completes all four core tasks and generates the final report assets.

Step

Script Path

Output

Status

Task 1: Data Collection

src/data_collection/scrape_reviews.py

data/raw/reviews_initial_clean.csv

Complete

Task 1: Preprocessing

src/data_processing/preprocess_data.py

data/processed/final_bank_reviews_constrained.csv

Complete

Task 2: NLP Analysis

src/analysis/nlp_pipeline.py

data/processed/reviews_with_sentiment_themes.csv

Complete

Task 3: Database Load

src/database/db_load_data.py

PostgreSQL (bank_reviews DB)

Complete

Task 4: Analysis & Reporting

src/analysis_and_reporting.py

3 Visualizations + Raw Insights

Final Step

🎯 Business Objectives (Complete)

This project successfully enables Omega Consultancy and banking partners to:

✅ Identify key satisfaction drivers and major pain points
✅ Compare banking app performance using balanced sentiment scores
✅ Generate actionable product improvement recommendations
✅ Support feature development and user retention strategies

🔬 Analysis Methodology

Task 1 — Data Collection & Preprocessing

Collected 9,800+ raw reviews using google-play-scraper.

Built a balanced dataset (2,100 reviews): 700 reviews per bank.

Output saved to: data/processed/final_bank_reviews_constrained.csv.

Task 2 — Sentiment & Thematic Analysis

📘 Sentiment Analysis

Model: distilbert-base-uncased-finetuned-sst-2-english

Process: Sentiment score per review is calculated and stored alongside the review text.

🏷️ Thematic Clustering

Reviews are mapped to 5 key customer experience themes: Account Access Issues, Transaction Performance, Reliability & Bugs, User Interface & UX, and Customer Support.

Output: data/processed/reviews_with_sentiment_themes.csv

Task 3 — PostgreSQL Database Load

Database: bank_reviews

Tables: banks and reviews (with PK/FK constraints).

All processed review data, including sentiment scores and themes, is persisted in the PostgreSQL database for reliable, scalable querying.

📊 Task 4 — Final Analysis and Reporting

This final stage connects to the PostgreSQL database, runs aggregation queries, and generates the necessary visual assets for the final consultation report.

Key Outputs

Executing src/analysis_and_reporting.py produces the following files in the reports/ directory:

Artifact

Purpose

File Path

Rating Distribution

Comparative view of 1-5 star distribution across banks.

reports/rating_distribution.png

Sentiment Trend

Time series analysis of average monthly sentiment scores.

reports/sentiment_trend.png

Pain Point Cloud

Visualization of the most frequent negative keywords/themes.

reports/keyword_cloud_pain_points.png

Raw Insights

Text file containing core quantitative findings and placeholders for recommendations.

reports/raw_insights.txt

Initial Rating Breakdown Summary

The analysis confirms a strong polarity profile for BOA, while CBE and Dashen exhibit a more heavily skewed positive distribution.

Bank

Highly Negative (1 Star)

Highly Positive (5 Stars)

BOA

282

307

CBE

120

451

Dashen

94

511

📂 Project Structure

fintech-reviews-analysis/
├── data/
│   ├── raw/                    # Initial scraped data
│   └── processed/              # Cleaned data (post-NLP)
├── db_schema/
│   ├── bank_reviews_schema.sql # Database creation script (Task 3 documentation)
│   └── verification_queries.sql                # Queries to check data integrity
├── src/
│   ├── data_collection/
│   ├── data_processing/
│   ├── analysis/
│   ├── database/
│   └── analysis_and_reporting.py # Final script for Task 4
├── reports/                  # **Final output visualizations and reports**
├── tests/
└── requirements.txt
