# 🚀 Fintech Customer Experience Analysis

### *A Data-Driven Review of Ethiopian Banking Apps for Omega Consultancy*

This project delivers a comprehensive analysis of **Google Play Store reviews** for major Ethiopian banking applications. Using NLP, sentiment scoring, and thematic clustering, it provides actionable insights to improve customer experience and inform digital banking strategy.

---

## 🏦 **Banks Analyzed**

| Bank                                  | App Name                 | Review Volume   |
| ------------------------------------- | ------------------------ | --------------- |
| **Commercial Bank of Ethiopia (CBE)** | CBE Mobile Banking       | 📈 High Volume  |
| **Bank of Abyssinia (BOA)**           | Bank of Abyssinia Mobile | ⏳ Medium Volume |
| **Dashen Bank**                       | Dashen Mobile Banking    | 📊 Lower Volume |

---

## 📌 **Project Status (Mockup Build Badges)**

> *(Badges shown as placeholders — to be updated once CI/CD is integrated.)*
> **Build Status:** ![Build Badge](#)
> **Data Pipeline:** ![Pipeline Badge](#)

---

## ⚡ Quick Start

### 🔧 **Installation**

```bash
# Clone the repository
git clone [YOUR_REPO_URL]
cd fintech-reviews-analysis

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ **Running the Full Analysis Pipeline**

Execute scripts **in order** from the project root:

| Step                        | Script Path                              | Output                                              |
| --------------------------- | ---------------------------------------- | --------------------------------------------------- |
| **Task 1: Data Collection** | `src/data_collection/scrape_reviews.py`  | `data/raw/reviews_initial_clean.csv`                |
| **Task 1: Preprocessing**   | `src/data_processing/preprocess_data.py` | `data/processed/final_bank_reviews_constrained.csv` |
| **Task 2: NLP Analysis**    | `src/analysis/nlp_pipeline.py`           | `data/processed/reviews_with_sentiment_themes.csv`  |
| **Task 3: Database Load**   | `src/database/db_load_data.py`           | PostgreSQL (`bank_reviews` DB)                      |

---

## 🎯 **Business Objectives**

This project enables Omega Consultancy and banking partners to:

✔ Identify **key satisfaction drivers** and **major pain points**
✔ Compare banking app performance using **balanced sentiment scores**
✔ Generate **actionable product improvement recommendations**
✔ Support **feature development** and **user retention strategies**

---

## 🔬 **Analysis Methodology**

### **Task 1 — Data Collection & Preprocessing (Complete)**

**Achievements:**

* Collected **9,800+ raw reviews** using `google-play-scraper`
* Built a **balanced dataset (2,100 reviews)** → *700 reviews per bank*
* Removed duplicates, normalized dates, handled missing values
* Output saved to: `data/processed/final_bank_reviews_constrained.csv`

---

### **Task 2 — Sentiment & Thematic Analysis**

#### 📘 **Sentiment Analysis**

* **Model:** `distilbert-base-uncased-finetuned-sst-2-english`
* **Output:**

  * Sentiment score per review
  * Aggregated sentiment trends per bank
  * Comparison of **1★ vs 5★** review tone across banks

---

#### 🏷️ **Thematic Clustering (Rule-Based + TF-IDF)**

Reviews are mapped to **5 key customer experience themes**:

| Theme                       | Focus Area                     | Example Keywords        | Scenario Alignment          |
| --------------------------- | ------------------------------ | ----------------------- | --------------------------- |
| **Account Access Issues**   | Login, verification, passwords | login, password, access | Feature Enhancement         |
| **Transaction Performance** | Transfer speed, OTP, failures  | slow, transfer, delay   | Scenario 1: Retaining Users |
| **Reliability & Bugs**      | Crashes, errors, updates       | crash, bug, error       | Complaint Management        |
| **User Interface & UX**     | Navigation, design             | ui, design, confusing   | Feature Enhancement         |
| **Customer Support**        | Service quality, help          | support, help, call     | Complaint Management        |

Output: `data/processed/reviews_with_sentiment_themes.csv`

---

## 📂 **Project Structure**

```
fintech-reviews-analysis/
├── data/                  # Raw and processed data
│   ├── raw/
│   └── processed/
├── src/
│   ├── data_collection/   # Scraping scripts
│   ├── data_processing/   # Preprocessing & cleaning
│   ├── analysis/          # NLP sentiment + theme analysis
│   └── database/          # PostgreSQL load operations
├── notebooks/             # Exploration & visualization
├── docs/                  # Documentation, final reports
├── tests/                 # Unit tests
└── requirements.txt       # Dependencies
```

---
