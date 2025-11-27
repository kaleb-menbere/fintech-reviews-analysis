💡 Fintech Customer Experience Analysis

A comprehensive analysis of Google Play Store reviews for Ethiopian banking apps to derive customer satisfaction insights and actionable recommendations for Omega Consultancy.

🏦 Banks Under Scrutiny

Bank

App Name

Status

Commercial Bank of Ethiopia (CBE)

CBE Mobile Banking

📈 High Volume

Bank of Abyssinia (BOA)

Bank of Abyssinia Mobile

⏳ Medium Volume

Dashen Bank

Dashen Mobile Banking

📊 Lower Volume

🚀 Quick Start & Project Status

Build Status (Mockup)

To reflect the dynamic nature of a project, the build status uses badge placeholders:




Installation

# Clone the repository
git clone [YOUR_REPO_URL]
cd fintech-reviews-analysis

# Install dependencies (pandas, transformers, scikit-learn, psycopg2, etc.)
pip install -r requirements.txt


Running the Analysis Pipeline

To execute the full pipeline, run the scripts in sequence from the project root:

Step

Script Path

Output Files

Task 1: Data Collection

src/data_collection/scrape_reviews.py

data/raw/reviews_initial_clean.csv

Task 1: Preprocessing

src/data_processing/preprocess_data.py

data/processed/final_bank_reviews_constrained.csv

Task 2: NLP Analysis

src/analysis/nlp_pipeline.py

data/processed/reviews_with_sentiment_themes.csv

Task 3: DB Load

src/database/db_load_data.py

PostgreSQL (bank_reviews DB)

🎯 Business Objectives (Actionable Focus)

✅ Identify customer satisfaction drivers and pain points using data-backed evidence.

✅ Compare performance across different banking apps based on balanced sentiment scores.

✅ Provide data-driven, actionable recommendations for app improvement.

✅ Support feature development and customer retention strategies.

🔬 Analysis Methodology

Task 1: Data Collection & Preprocessing (Completed)

Successfully scraped and cleaned customer reviews for CBE, BOA, and Dashen Bank.

Key achievements:

Collected over 9,800 raw reviews using the google-play-scraper library.

Processed data to create a balanced dataset of 2,100 reviews (700 per bank) to mitigate class imbalance bias for fair comparative analysis.

Handled missing values, removed duplicates, and normalized the date format (YYYY-MM-DD).

Saved the clean, balanced dataset to data/processed/final_bank_reviews_constrained.csv.

Task 2: Sentiment and Thematic Analysis

This phase applies advanced NLP techniques to quantify feedback and group complaints into actionable themes.

Sentiment Analysis

Model: distilbert-base-uncased-finetuned-sst-2-english (Hugging Face Transformers).

Metric: Sentiment scores are aggregated by bank and rating to identify performance trends across the star spectrum (e.g., mean sentiment of 1-star reviews vs. 5-star reviews).

Thematic Analysis (Rule-Based Clustering)

Thematic analysis uses TF-IDF for keyword extraction followed by a Rule-Based Clustering approach to assign reviews to 5 core themes:

Theme 🏷️

Focus Area

Example Keywords

Scenario Alignment

Account Access Issues

Login, verification, password resets.

login, password, fingerprint, access

Feature Enhancement, Complaint Management

Transaction Performance

Speed, successful transfers, OTP delays.

slow, transfer, speed, delay, transaction

Scenario 1: Retaining Users

Reliability & Bugs

App stability, crashes, update issues.

crash, bug, error, fault, stop, problem

Complaint Management

User Interface & Experience

Navigation, design, ease of use.

ui, interface, design, easy, confusing

Feature Enhancement

Customer Support & Service

Help quality, branch interactions.

support, customer, call, help

Complaint Management

📂 Project Structure

fintech-reviews-analysis/
├── data/               # Data storage
│   ├── raw/           # Raw scraped data
│   └── processed/     # Cleaned and processed data (Input for Task 2/3)
├── src/               # Source code
│   ├── data_collection/ # Web scraping scripts
│   ├── data_processing/ # Data cleaning and preprocessing
│   ├── analysis/           # NLP and sentiment analysis (Task 2)
│   └── database/           # Database operations (Task 3)
├── notebooks/          # Jupyter notebooks
├── docs/              # Documentation and reports
├── tests/             # Unit tests
└── requirements.txt   # Project dependencies
