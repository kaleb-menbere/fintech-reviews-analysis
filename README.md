Fintech Reviews Analysis

A comprehensive analysis of Google Play Store reviews for Ethiopian banking apps to derive customer satisfaction insights and actionable recommendations.

🏦 Banks Analyzed

Commercial Bank of Ethiopia (CBE)

Bank of Abyssinia (BOA)

Dashen Bank

📁 Project Structure

fintech-reviews-analysis/
├── data/               # Data storage
│   ├── raw/           # Raw scraped data
│   └── processed/     # Cleaned and processed data
├── src/               # Source code
│   ├── data_collection/scrape_reviews.py    # Web scraping scripts
│   ├── data_processing/preprocess_data.py    # Data cleaning and preprocessing
│   ├── analysis/           # NLP and sentiment analysis
│   └── database/           # Database operations
├── notebooks/          # Jupyter notebooks
│   ├── exploration/   # Data exploration
│   └── analysis/      # Analysis notebooks
├── docs/              # Documentation and reports
│   ├── reports/       # Generated reports
│   └── assets/        # Images and assets
├── tests/             # Unit tests
├── config/            # Configuration files
└── scripts/           # Utility scripts


🚀 Quick Start

Installation

pip install -r requirements.txt


Running the Pipeline

Data Collection: python src/data_collection/scrape_reviews.py

Data Processing: python src/data_processing/clean_reviews.py

Analysis: python src/analysis/sentiment_analysis.py

📊 Methodology

Data Collection: Automated scraping of Google Play Store reviews

Data Cleaning: Handling missing values, duplicates, and normalization

Sentiment Analysis: Using transformer models for sentiment classification

Thematic Analysis: Keyword extraction and topic modeling

Database Storage: PostgreSQL for persistent data storage

Visualization: Interactive plots and dashboards

🎯 Business Objectives

Identify customer satisfaction drivers and pain points

Compare performance across different banking apps

Provide data-driven recommendations for app improvement

Support feature development and customer retention strategies

Task 2: Sentiment and Thematic Analysis Methodology

This task focused on quantifying user sentiment and grouping feedback into actionable themes using Natural Language Processing (NLP) techniques.

Sentiment Analysis

Model: distilbert-base-uncased-finetuned-sst-2-english (Hugging Face Transformers).

Process: The model was applied to the cleaned review text, outputting a sentiment_label (positive or negative) and a sentiment_score (confidence). The score was normalized such that a higher score always indicates more positive sentiment.

Aggregation: Sentiment scores were aggregated by bank and rating to identify sentiment trends across the star spectrum (e.g., mean sentiment of 1-star reviews vs. 5-star reviews).

Thematic Analysis

Method: Keyword Extraction (via TF-IDF) followed by Rule-Based Clustering.

Keyword Extraction: The TF-IDF (Term Frequency-Inverse Document Frequency) method was used to identify the most significant unigrams and bigrams (n-grams) within each bank's review set. This informed the creation of the theme rules.

Theme Rules (Rule-Based Clustering): To ensure consistency and actionability (meeting the 3-5 theme requirement), a rule-based mapping was implemented. Reviews are assigned one or more of the following themes based on the presence of specific keywords:

Account Access Issues: (e.g., login, password, fingerprint)

Transaction Performance: (e.g., slow, transfer, speed, time)

Reliability & Bugs: (e.g., crash, bug, error, fault)

User Interface & Experience: (e.g., UI, interface, design, easy)

Customer Support & Service: (e.g., support, customer, call, help)

The resulting dataset, reviews_with_sentiment_themes.csv, includes the calculated sentiment and assigned themes for use in Task 3 and Task 4.