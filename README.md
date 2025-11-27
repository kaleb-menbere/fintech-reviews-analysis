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


# 📊 Rating Breakdown Analysis

### ⭐ **Overview**

After loading the processed dataset (`final_bank_reviews_constrained.csv`), the rating distribution across the three banking apps shows clear patterns in customer satisfaction. Each bank has exactly **700 balanced reviews**, ensuring a fair comparison.

---

## 🔢 **Raw Review Counts**

| Bank       | Review Count |
| ---------- | ------------ |
| **BOA**    | 700          |
| **CBE**    | 700          |
| **Dashen** | 700          |

---

## ⭐ **Bank-Specific Rating Distribution (1–5 Stars)**

### **Bank of Abyssinia (BOA)**

**Highly polarized review profile** — customers either love it or hate it.

| Rating    | Count   |
| --------- | ------- |
| ⭐ 1       | 282     |
| ⭐ 2       | 39      |
| ⭐ 3       | 43      |
| ⭐ 4       | 29      |
| ⭐ 5       | 307     |
| **Total** | **700** |

---

### **Commercial Bank of Ethiopia (CBE)**

**Generally positive sentiment**, with a strong cluster of 5-star reviews.

| Rating    | Count   |
| --------- | ------- |
| ⭐ 1       | 120     |
| ⭐ 2       | 24      |
| ⭐ 3       | 35      |
| ⭐ 4       | 70      |
| ⭐ 5       | 451     |
| **Total** | **700** |

---

### **Dashen Bank**

**Best-performing rating distribution** — very high percentage of 5-star reviews.

| Rating    | Count   |
| --------- | ------- |
| ⭐ 1       | 94      |
| ⭐ 2       | 30      |
| ⭐ 3       | 28      |
| ⭐ 4       | 37      |
| ⭐ 5       | 511     |
| **Total** | **700** |

---

## 📁 Output File

The rating breakdown table is automatically exported as:

```
bank_rating_breakdown.csv
```

This file can be used for dashboards, reporting, and visual analytics.


