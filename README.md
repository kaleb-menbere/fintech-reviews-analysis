# 🚀 Fintech Customer Experience Analysis

### *A Data-Driven Review of Ethiopian Banking Apps for Omega Consultancy*

This project delivers a full analytical pipeline for evaluating customer experiences across major Ethiopian mobile banking applications. Using NLP, sentiment analysis, thematic classification, and relational data storage, it generates actionable insights to guide digital banking strategy and feature development.

---

# 🏦 Banks Included in the Study

| Bank                                  | App Name                 | Review Volume |
| ------------------------------------- | ------------------------ | ------------- |
| Commercial Bank of Ethiopia (CBE) | CBE Mobile Banking       | 📈 High       |
| Bank of Abyssinia (BOA)           | Bank of Abyssinia Mobile | ⏳ Medium      |
| Dashen Bank                       | Dashen Mobile Banking    | 📊 Low        |

---

# ⚡ Quick Start

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/kaleb-menbere/fintech-reviews-analysis.git
cd fintech-reviews-analysis

# Install dependencies
pip install -r requirements.txt
```

---

# ▶️ Running the Full Analysis Pipeline (All 4 Tasks)

Run each script from the project root in the order below.

| Step                             | Script Path                              | Output                                                 | Status        |
| -------------------------------- | ---------------------------------------- | ------------------------------------------------------ | ------------- |
| Task 1 — Data Collection     | `src/data_collection/scrape_reviews.py`  | `data/raw/reviews_initial_clean.csv`                   | ✅ Complete    |
| Task 1 — Preprocessing       | `src/data_processing/preprocess_data.py` | `data/processed/final_bank_reviews_constrained.csv`    | ✅ Complete    |
| Task 2 — NLP Analysis        | `src/analysis/nlp_pipeline.py`           | `data/processed/reviews_with_sentiment_themes.csv`     | ✅ Complete    |
| Task 3 — Database Load       | `src/database/db_load_data.py`           | PostgreSQL: `bank_reviews`                             | ✅ Complete    |
| Task 4 — Reporting & Visuals | `src/analysis_and_reporting.py`          | Rating chart, sentiment trend, keyword cloud, insights | 🏁 Final Step |

---

# 🎯 Business Objectives — Successfully Achieved

This analysis enables Omega Consultancy and banking partners to:

✔ Identify the strongest customer satisfaction drivers
✔ Detect major pain points affecting transactions & app usage
✔ Compare banking app performance using balanced sentiment data
✔ Generate actionable product improvement recommendations
✔ Support feature roadmapping & user retention strategies

---

# 🔬 Analysis Methodology

## Task 1 — Data Collection & Preprocessing

* Scraped 9,800+ Google Play reviews using *google-play-scraper*.
* Built a balanced dataset: 700 reviews per bank (total 2,100).
* Cleaned, deduplicated, standardized, and normalized text.

📁 Output:
`data/processed/final_bank_reviews_constrained.csv`

---

## Task 2 — Sentiment & Thematic Analysis

### 📘 Sentiment Analysis

* Model used: `distilbert-base-uncased-finetuned-sst-2-english`
* Produced:

  * Sentiment label (Positive / Neutral / Negative)
  * Sentiment polarity score
  * Emoji reaction (visual sentiment indicator)

### 🏷️ Thematic Clustering

Reviews are categorized into 5 customer experience themes:

1. Account Access Issues
2. Transaction Performance
3. Reliability & Bugs
4. User Interface & UX
5. Customer Support

📁 Output:
`data/processed/reviews_with_sentiment_themes.csv`

---

## Task 3 — PostgreSQL Database Storage

* Database: bank_reviews
* Tables:

  * `banks` (parent)
  * `reviews` (child, FK to bank_id)
* All enriched reviews (sentiment + themes) stored relationally for scalable querying.

---

## Task 4 — Final Analysis & Reporting

The final script connects to the PostgreSQL database and produces visual assets + insights.

### Generated Assets

| Artifact                  | Purpose                          | File Path                               |
| ------------------------- | -------------------------------- | --------------------------------------- |
| ⭐ Rating Distribution | Compare 1–5 star ratings         | `reports/rating_distribution.png`       |
| 📉 Sentiment Trend    | Time-series of monthly sentiment | `reports/sentiment_trend.png`           |
| ☁️ Pain Point Cloud   | Most frequent negative keywords  | `reports/keyword_cloud_pain_points.png` |
| 📄 Raw Insights       | Key metrics + recommendations    | `reports/raw_insights.txt`              |

---

# ⭐ Initial Rating Breakdown Summary

| Bank       | 1-Star (Highly Negative) | 5-Star (Highly Positive) |
| ---------- | ------------------------ | ------------------------ |
| BOA    | 282                      | 307                      |
| CBE    | 120                      | 451                      |
| Dashen | 94                       | 511                      |

---

# 📂 Project Structure

```
fintech-reviews-analysis/
├── data/
│   ├── raw/                       # Initial scraped data
│   └── processed/                 # Cleaned & NLP-enriched data
├── db_schema/
│   ├── bank_reviews_schema.sql    # Database creation script
│   └── verification_queries.sql   # Integrity checks
├── src/
│   ├── data_collection/
│   ├── data_processing/
│   ├── analysis/
│   ├── database/
│   └── analysis_and_reporting.py  # Final analytics script
├── reports/                       # Final visualizations & insight files
├── tests/
└── requirements.txt
```

