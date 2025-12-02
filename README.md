# 🚀 **Fintech Customer Experience Analysis**

### *A Data-Driven Review of Ethiopian Mobile Banking Apps*

**Prepared for Omega Consultancy**

This project provides an end-to-end analytical pipeline for evaluating customer sentiment, themes, and pain points from Google Play Store reviews of major Ethiopian banking applications. Using NLP, PostgreSQL, and automated reporting, it produces insights that support digital banking strategy, product improvement, and user experience optimization.

---

# 🏦 **Banks Included**

| Bank                                  | Mobile App            | Review Volume |
| ------------------------------------- | --------------------- | ------------- |
| **Commercial Bank of Ethiopia (CBE)** | CBE Mobile Banking    | 📈 High       |
| **Bank of Abyssinia (BOA)**           | BOA Mobile Banking    | ⏳ Medium      |
| **Dashen Bank**                       | Dashen Mobile Banking | 📉 Lower      |

---

# ⚡ **Quick Start**

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/kaleb-menbere/fintech-reviews-analysis.git
cd fintech-reviews-analysis

# Install dependencies
pip install -r requirements.txt
```

---

# ▶️ **How to Run the Full Pipeline**

All steps are detailed in **How-to-Run.md**, but here is the quick execution order:

| Step                          | Script                                      | Output                                              |
| ----------------------------- | ------------------------------------------- | --------------------------------------------------- |
| **Task 1 — Data Collection**  | `src/data_collection/scrape_reviews.py`     | `data/raw/reviews_initial_clean.csv`                |
| **Task 1 — Preprocessing**    | `src/data_preprocessing/preprocess_data.py` | `data/processed/final_bank_reviews_constrained.csv` |
| **Task 2 — NLP Analysis**     | `src/analysis/...` *(depending on version)* | `data/processed/reviews_with_sentiment_themes.csv`  |
| **Task 3 — Database Storage** | `src/database/task_3_database_storage.py`   | PostgreSQL: *bank_reviews* DB                       |
| **Task 4 — Final Reporting**  | `src/analysis/task_4_analysis.py`           | Visuals + insights → `reports/task_4_output/`       |

---

# 🎯 **Business Goals — Achieved**

This pipeline helps Omega Consultancy and partner banks to:

✔ Identify top customer frustrations and positive drivers
✔ Compare app performance through structured sentiment metrics
✔ Discover patterns across reliability, UX, and transaction flow
✔ Support data-driven feature development
✔ Improve digital banking retention and app satisfaction

---

# 🔬 **Methodology Overview**

## **Task 1 — Data Collection & Preprocessing**

* Scraped **9,800+ reviews** using *google-play-scraper*
* Cleaned and normalized text
* Balanced dataset: **700 reviews per bank**
* Output:
  `data/processed/final_bank_reviews_constrained.csv`

---

## **Task 2 — NLP: Sentiment & Thematic Analysis**

### 🔥 Sentiment Analysis

Model used:
`distilbert-base-uncased-finetuned-sst-2-english`

Produces:

* Sentiment Label → Positive / Neutral / Negative
* Sentiment Score → -1.0 to +1.0
* Emoji Reaction → 😡 😐 😃 (included in dataset)

### 🏷️ Thematic Classification

5 major customer themes:

1. Account Access Issues
2. Transaction Performance
3. Reliability & Bug Reports
4. UI & User Experience
5. Customer Support

Output:
`data/processed/reviews_with_sentiment_themes.csv`

---

## **Task 3 — PostgreSQL Database Storage**

Database Name: **bank_reviews**
Tables:

* `banks` — list of banks
* `reviews` — all enriched review records (FK → bank_id)

All cleaned review data is persisted for scalable reporting and analytics.

---

## **Task 4 — Reporting & Visualization**

Running Task 4 generates 4 key deliverables stored in:

📁 `reports/task_4_output/`

| File                            | Description                                 |
| ------------------------------- | ------------------------------------------- |
| `rating_distribution.png`       | Comparison of 1–5 star ratings across banks |
| `sentiment_trend.png`           | Monthly sentiment trend                     |
| `keyword_cloud_pain_points.png` | Negative feedback keyword cloud             |
| `raw_insights.txt`              | Summary of insights + metrics               |

---

# ⭐ **Initial Rating Summary**

| Bank       | 1-Star (Negative) | 5-Star (Positive) |
| ---------- | ----------------- | ----------------- |
| **BOA**    | 282               | 307               |
| **CBE**    | 120               | 451               |
| **Dashen** | 94                | 511               |

---

# 📂 **Project Structure**

```
fintech-reviews-analysis/
├─ How-to-Run.md
├─ README.md
├─ requirements.txt
├─ scraping.log
├─ config/
│  └─ db_config.py
├─ data/
│  ├─ raw/
│  │  └─ reviews_initial_clean.csv
│  └─ processed/
│     ├─ aggregated_bank_insights.csv
│     ├─ final_bank_reviews_constrained.csv
│     └─ reviews_with_sentiment_themes.csv
├─ notebooks/
│  ├─ README.md
│  ├─ processing.log
│  ├─ scraping.log
│  ├─ task-1.ipynb
│  ├─ task-2.ipynb
│  ├─ task-3.ipynb
│  └─ task-4.ipynb
├─ reports/
│  └─ task_4_output/
│     ├─ keyword_cloud_pain_points.png
│     ├─ rating_distribution.png
│     ├─ raw_insights.txt
│     └─ sentiment_trend.png
├─ scripts/
├─ src/
│  ├─ analysis/
│  │  └─ task_4_analysis.py
│  ├─ data_collection/
│  │  └─ scrape_reviews.py
│  ├─ data_preprocessing/
│  │  └─ preprocess_data.py
│  └─ database/
│     ├─ README.md
│     ├─ image-1.png
│     ├─ image-2.png
│     ├─ image.png
│     └─ task_3_database_storage.py
└─ tests/
```

