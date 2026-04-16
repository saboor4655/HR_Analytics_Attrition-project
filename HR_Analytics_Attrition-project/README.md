# 👥 HR Analytics — Employee Attrition & Workforce Health Audit

> **End-to-end data analytics project** | Python · SQL · Excel · Power BI

---

## 📌 Project Summary

This project analyses employee attrition at a fictional IBM company using the publicly available IBM HR Analytics dataset. It follows a complete data analyst workflow from raw data cleaning through to an executive-level Power BI dashboard, answering three core business questions:

| Layer | Question | Answer |
|---|---|---|
| **WHAT** | Who is leaving and how many? | 16.1% attrition — 237 of 1,470 employees left |
| **WHY** | Why are they leaving? | Low income, overtime, low satisfaction, short tenure |
| **HOW** | How do we fix it? | $8.7M annual cost — actionable retention ROI model |

---

## 📊 Key Findings

- **Overall attrition rate: 16.1%** — 237 employees left out of 1,470
- **Sales department** has the highest attrition at **20.6%**
- **Sales Representatives** are the highest-risk role at **39.8% attrition**
- Employees who left earned **$2,046/month less** ($4,787 vs $6,833)
- Overtime workers leave at **3× the rate** of non-overtime workers (30.5% vs 10.4%)
- **First-year employees** show 34.9% attrition — the most critical retention window
- **Total annual cost of attrition: $8,724,444** ($36,812 per leaver)

---

## 🛠️ Tools & Skills Used

| Tool | Phase | What Was Done |
|---|---|---|
| **Python** | Phase 1 | Data loading, cleaning, EDA, feature engineering, CSV export |
| **SQL (SQLite)** | Phase 2 | 10 business queries, GROUP BY, CASE WHEN, aggregations |
| **Excel** | Phase 3 | 4-sheet cost model, ROI scenarios, sensitivity analysis |
| **Power BI** | Phase 4 | 3-page interactive dashboard, DAX measures, cross-filtering |

---

## 📁 Project Structure

```
HR_Analytics_Attrition-project/
│
├── README.md
│
├── data/
│   ├── raw/               ← Download dataset from Kaggle (link below)
│   └── clean/
│       └── hr_powerbi.csv ← Cleaned 33-column Power BI dataset
│
├── python/
│   └── 01_hr_cleaning_eda.py     ← Data cleaning + EDA script
│
├── sql/
│   └── 02_hr_sql_analysis.py     ← 10 SQL business queries via SQLite
│
├── excel/
│   └── 03_hr_attrition_cost_model.xlsx  ← Cost model + ROI workbook
│
├── powerbi/
│   └── 04_hr_powerbi_dashboard.pbix     ← 3-page interactive dashboard
│
├── presentation/
│   └── HR_Analytics_Portfolio_Presentation.pptx
│
└── outputs/
    └── 02_hr_sql_results.xlsx    ← All 10 SQL results (9 sheets)
```

---

## 📥 Dataset

- **Source:** [IBM HR Analytics Employee Attrition & Performance — Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
- **Original size:** 1,470 rows × 35 columns
- **After cleaning:** 1,470 rows × 33 columns
- **Missing values:** None
- **Duplicates:** None

**Columns removed (no analytical value):**
`EmployeeCount` `EmployeeNumber` `Over18` `StandardHours` `DailyRate` `HourlyRate` `MonthlyRate`

**Columns added:**
`Attrition_Flag` `Age_Group` `Tenure_Group` `Income_Band` `JobSatisfaction_Label`

---

## 🚀 How to Run This Project

### Phase 1 — Python Cleaning

```bash
# Install dependencies
pip install pandas

# Run cleaning script
python python/01_hr_cleaning_eda.py
```

### Phase 2 — SQL Analysis

```bash
# No additional install needed (sqlite3 is built into Python)
python sql/02_hr_sql_analysis.py
```

### Phase 3 — Excel

Open `excel/03_hr_attrition_cost_model.xlsx` in Microsoft Excel.
All formulas are live — change the yellow input cells to run scenarios.

### Phase 4 — Power BI

1. Download and install [Power BI Desktop (free)](https://powerbi.microsoft.com/desktop)
2. Open `powerbi/04_hr_powerbi_dashboard.pbix`
3. If prompted, reconnect to `data/clean/hr_powerbi.csv`

---

## 📈 Dashboard Pages

| Page | Title | Content |
|---|---|---|
| Page 1 | Executive Summary | 4 KPI cards, attrition by dept/role, age group, overtime charts |
| Page 2 | Root Cause Analysis | Income gap, job satisfaction, tenure, commute distance |
| Page 3 | Cost & Recommendations | Cost KPIs, dept table, retention ROI, salary band analysis |

All pages support **cross-filtering** — click any bar to filter every visual simultaneously.

---

## 💡 Business Recommendations

| Priority | Action | Potential Annual Saving |
|---|---|---|
| 🔴 Immediate | Audit mandatory overtime in Sales | $697,960 |
| 🟡 Short-term | Salary review for Sales Reps under $3K/month | $436,225 |
| 🔵 Medium-term | Manager quality & satisfaction programme | $268,980 |
| 🟢 Long-term | Career path framework for under-25 employees | $403,470 |
| ⚫ Combined | All initiatives together (20% attrition reduction) | $944,901 net ROI |

---

## 📂 Excel Cost Model Structure

| Sheet | Purpose |
|---|---|
| 1_Cost Calculator | Assumptions + cost per leaver + company-wide impact |
| 2_Dept Risk Scorecard | Per-department attrition cost with risk ratings |
| 3_Retention ROI Model | 5 retention scenarios with net ROI + sensitivity table |
| 4_Source Data | SQL results reference table |

---

---

## 👤 Author

**Abdul Saboor**
Data Analyst | Excel · Power BI · SQL · Python

---

*Dataset credit: IBM data scientists via Kaggle. This is a fictional dataset used for analytical practice.*
