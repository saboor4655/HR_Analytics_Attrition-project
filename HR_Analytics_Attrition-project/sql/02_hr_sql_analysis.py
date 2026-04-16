# =============================================================================
# PROJECT 1 — HR Analytics
# Script   : 02_hr_sql_analysis.py
# Purpose  : Load clean HR data into SQLite and answer business questions
#            using real SQL queries — just like in a corporate environment.
# =============================================================================

import pandas as pd          # to load our CSV
import sqlite3               # built into Python — no install needed!
import os

# --- FILE PATHS ---
CLEAN_PATH = r"C:\Users\dell\Downloads\HR_Analytics_Project\data\clean\hr_clean.csv"
DB_PATH    = r"C:\Users\dell\Downloads\HR_Analytics_Project\data\clean\hr_database.db"
OUTPUT_DIR = r"C:\Users\dell\Downloads\HR_Analytics_Project\outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =============================================================================
# STEP 1 — LOAD CSV INTO SQLITE DATABASE
# =============================================================================
# Think of SQLite as a mini-database that lives in a single file on your PC.
# We load our clean CSV into it as a "table" called 'employees'.
# After this, we can query it exactly like a real SQL database.

print("=" * 60)
print("STEP 1: Loading data into SQLite database...")
print("=" * 60)

df = pd.read_csv(CLEAN_PATH)

# Connect to SQLite — this creates the .db file automatically
conn = sqlite3.connect(DB_PATH)

# Write the dataframe into a table called 'employees'
# if_exists='replace' means: overwrite if the table already exists
df.to_sql("employees", conn, if_exists="replace", index=False)

print(f"\n  Table 'employees' created in database.")
print(f"  Rows loaded: {len(df):,}")
print(f"  Database saved: {DB_PATH}")


# =============================================================================
# HELPER FUNCTION
# =============================================================================
# Instead of writing conn.execute() every time, we create a small helper
# function. This is called a "reusable function" — market standard practice.

def run_query(title, sql):
    """
    Runs a SQL query and prints the result nicely.
    
    Parameters:
    - title : A label so we know what the query is about
    - sql   : The actual SQL query to run
    """
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    
    result = pd.read_sql_query(sql, conn)
    # pd.read_sql_query runs the SQL and returns a DataFrame (table)
    
    print(result.to_string(index=False))
    # to_string(index=False) prints without the row numbers
    
    return result


# =============================================================================
# QUERY 1 — OVERALL ATTRITION SUMMARY
# =============================================================================
# SQL explanation:
# COUNT(*)              → count all rows (all employees)
# SUM(attrition_flag)   → adds up all 1s = total who left
# ROUND(... * 100, 1)   → calculate % and round to 1 decimal
# AS                    → rename a column in the result

run_query(
    "Q1: Overall Attrition Summary",
    """
    SELECT
        COUNT(*)                                        AS total_employees,
        SUM(attrition_flag)                             AS employees_left,
        COUNT(*) - SUM(attrition_flag)                  AS employees_stayed,
        ROUND(SUM(attrition_flag) * 100.0 / COUNT(*), 1) AS attrition_rate_pct
    FROM employees
    """
)


# =============================================================================
# QUERY 2 — ATTRITION BY DEPARTMENT
# =============================================================================
# SQL explanation:
# GROUP BY department   → split the table into groups, one per department
# ORDER BY ... DESC     → sort from highest to lowest attrition rate

run_query(
    "Q2: Attrition Rate by Department",
    """
    SELECT
        department,
        COUNT(*)                                          AS total_employees,
        SUM(attrition_flag)                               AS left_company,
        ROUND(SUM(attrition_flag) * 100.0 / COUNT(*), 1) AS attrition_rate_pct
    FROM employees
    GROUP BY department
    ORDER BY attrition_rate_pct DESC
    """
)


# =============================================================================
# QUERY 3 — ATTRITION BY JOB ROLE
# =============================================================================
# Same logic as Q2 but grouped by job role instead of department.

run_query(
    "Q3: Attrition Rate by Job Role (Highest Risk First)",
    """
    SELECT
        jobrole,
        COUNT(*)                                          AS total_employees,
        SUM(attrition_flag)                               AS left_company,
        ROUND(SUM(attrition_flag) * 100.0 / COUNT(*), 1) AS attrition_rate_pct
    FROM employees
    GROUP BY jobrole
    ORDER BY attrition_rate_pct DESC
    """
)


# =============================================================================
# QUERY 4 — AVERAGE SALARY: LEFT vs STAYED
# =============================================================================
# SQL explanation:
# AVG(monthlyincome)   → calculate the average salary per group
# CASE WHEN ... END    → this is like IF/ELSE in SQL
#   WHEN attrition = 'Yes' THEN 'Left'   means: if they left, label as "Left"
#   ELSE 'Stayed'                         means: otherwise label as "Stayed"

run_query(
    "Q4: Average Monthly Income — Left vs Stayed",
    """
    SELECT
        CASE WHEN attrition = 'Yes' THEN 'Left' ELSE 'Stayed' END AS status,
        ROUND(AVG(monthlyincome), 0)  AS avg_monthly_income,
        ROUND(MIN(monthlyincome), 0)  AS min_income,
        ROUND(MAX(monthlyincome), 0)  AS max_income
    FROM employees
    GROUP BY attrition
    ORDER BY avg_monthly_income ASC
    """
)


# =============================================================================
# QUERY 5 — OVERTIME IMPACT ON ATTRITION
# =============================================================================
# This answers WHY — overworked employees leave at much higher rates.

run_query(
    "Q5: Overtime vs Attrition (The WHY)",
    """
    SELECT
        overtime,
        COUNT(*)                                          AS total_employees,
        SUM(attrition_flag)                               AS left_company,
        ROUND(SUM(attrition_flag) * 100.0 / COUNT(*), 1) AS attrition_rate_pct
    FROM employees
    GROUP BY overtime
    ORDER BY attrition_rate_pct DESC
    """
)


# =============================================================================
# QUERY 6 — ATTRITION BY AGE GROUP
# =============================================================================
# SQL explanation:
# CASE WHEN age < 25 THEN '< 25'   → creates age buckets (like bins in Python)
# This is called "binning" or "bucketing" in analytics.

run_query(
    "Q6: Attrition by Age Group",
    """
    SELECT
        CASE
            WHEN age < 25             THEN '1. Under 25'
            WHEN age BETWEEN 25 AND 34 THEN '2. Age 25-34'
            WHEN age BETWEEN 35 AND 44 THEN '3. Age 35-44'
            WHEN age BETWEEN 45 AND 54 THEN '4. Age 45-54'
            ELSE                           '5. Age 55+'
        END AS age_group,
        COUNT(*)                                          AS total_employees,
        SUM(attrition_flag)                               AS left_company,
        ROUND(SUM(attrition_flag) * 100.0 / COUNT(*), 1) AS attrition_rate_pct
    FROM employees
    GROUP BY age_group
    ORDER BY age_group
    """
)


# =============================================================================
# QUERY 7 — ATTRITION BY YEARS AT COMPANY
# =============================================================================
# How long do people last before leaving?

run_query(
    "Q7: Attrition by Tenure Group (Years at Company)",
    """
    SELECT
        CASE
            WHEN yearsatcompany <= 1  THEN '1. 0-1 Years'
            WHEN yearsatcompany <= 3  THEN '2. 1-3 Years'
            WHEN yearsatcompany <= 5  THEN '3. 3-5 Years'
            WHEN yearsatcompany <= 10 THEN '4. 5-10 Years'
            ELSE                           '5. 10+ Years'
        END AS tenure_group,
        COUNT(*)                                          AS total_employees,
        SUM(attrition_flag)                               AS left_company,
        ROUND(SUM(attrition_flag) * 100.0 / COUNT(*), 1) AS attrition_rate_pct
    FROM employees
    GROUP BY tenure_group
    ORDER BY tenure_group
    """
)


# =============================================================================
# QUERY 8 — TOP 10 HIGH RISK EMPLOYEES PROFILE
# =============================================================================
# SQL explanation:
# WHERE  → filter rows (like a condition)
# AND    → combine multiple conditions
# LIMIT  → only show first N rows
# This query finds the profile of employees MOST likely to leave.

run_query(
    "Q8: Profile of High-Risk Employees (Left + Overtime + Low Pay)",
    """
    SELECT
        department,
        jobrole,
        age,
        monthlyincome,
        overtime,
        yearsatcompany,
        jobsatisfaction
    FROM employees
    WHERE attrition_flag = 1          -- only employees who left
      AND overtime = 'Yes'            -- who worked overtime
      AND monthlyincome < 3000        -- and earned less than $3,000
    ORDER BY monthlyincome ASC        -- lowest paid first
    LIMIT 10
    """
)


# =============================================================================
# QUERY 9 — JOB SATISFACTION vs ATTRITION
# =============================================================================
# jobsatisfaction is rated 1-4 in this dataset
# 1 = Low, 2 = Medium, 3 = High, 4 = Very High
# Does low satisfaction predict leaving?

run_query(
    "Q9: Job Satisfaction vs Attrition",
    """
    SELECT
        jobsatisfaction                                   AS satisfaction_score,
        CASE
            WHEN jobsatisfaction = 1 THEN 'Low'
            WHEN jobsatisfaction = 2 THEN 'Medium'
            WHEN jobsatisfaction = 3 THEN 'High'
            ELSE                          'Very High'
        END AS satisfaction_label,
        COUNT(*)                                          AS total_employees,
        SUM(attrition_flag)                               AS left_company,
        ROUND(SUM(attrition_flag) * 100.0 / COUNT(*), 1) AS attrition_rate_pct
    FROM employees
    GROUP BY jobsatisfaction
    ORDER BY jobsatisfaction
    """
)


# =============================================================================
# QUERY 10 — DEPARTMENT + OVERTIME COMBINED (DEEP DIVE)
# =============================================================================
# This is a multi-dimension query — we look at two factors together.
# This is the kind of query that impresses in interviews.

run_query(
    "Q10: Attrition by Department AND Overtime (Multi-Dimension)",
    """
    SELECT
        department,
        overtime,
        COUNT(*)                                          AS total_employees,
        SUM(attrition_flag)                               AS left_company,
        ROUND(SUM(attrition_flag) * 100.0 / COUNT(*), 1) AS attrition_rate_pct
    FROM employees
    GROUP BY department, overtime
    ORDER BY attrition_rate_pct DESC
    """
)


# =============================================================================
# STEP 2 — SAVE ALL RESULTS TO EXCEL
# =============================================================================
# We now save every query result as a separate sheet in one Excel file.
# This Excel file goes straight into your portfolio.

print(f"\n{'=' * 60}")
print("  Saving all query results to Excel...")
print(f"{'=' * 60}")

excel_path = os.path.join(OUTPUT_DIR, "02_hr_sql_results.xlsx")

# pd.ExcelWriter lets us write multiple sheets into one Excel file
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:

    queries = {
        "1_Overall Summary"     : "SELECT COUNT(*) AS total_employees, SUM(attrition_flag) AS employees_left, ROUND(SUM(attrition_flag)*100.0/COUNT(*),1) AS attrition_rate_pct FROM employees",
        "2_By Department"       : "SELECT department, COUNT(*) AS total, SUM(attrition_flag) AS left_company, ROUND(SUM(attrition_flag)*100.0/COUNT(*),1) AS rate_pct FROM employees GROUP BY department ORDER BY rate_pct DESC",
        "3_By Job Role"         : "SELECT jobrole, COUNT(*) AS total, SUM(attrition_flag) AS left_company, ROUND(SUM(attrition_flag)*100.0/COUNT(*),1) AS rate_pct FROM employees GROUP BY jobrole ORDER BY rate_pct DESC",
        "4_Income Comparison"   : "SELECT CASE WHEN attrition='Yes' THEN 'Left' ELSE 'Stayed' END AS status, ROUND(AVG(monthlyincome),0) AS avg_income FROM employees GROUP BY attrition",
        "5_Overtime Impact"     : "SELECT overtime, COUNT(*) AS total, SUM(attrition_flag) AS left_company, ROUND(SUM(attrition_flag)*100.0/COUNT(*),1) AS rate_pct FROM employees GROUP BY overtime ORDER BY rate_pct DESC",
        "6_By Age Group"        : "SELECT CASE WHEN age<25 THEN 'Under 25' WHEN age BETWEEN 25 AND 34 THEN '25-34' WHEN age BETWEEN 35 AND 44 THEN '35-44' WHEN age BETWEEN 45 AND 54 THEN '45-54' ELSE '55+' END AS age_group, COUNT(*) AS total, SUM(attrition_flag) AS left_company, ROUND(SUM(attrition_flag)*100.0/COUNT(*),1) AS rate_pct FROM employees GROUP BY age_group ORDER BY age_group",
        "7_By Tenure"           : "SELECT CASE WHEN yearsatcompany<=1 THEN '0-1 Yrs' WHEN yearsatcompany<=3 THEN '1-3 Yrs' WHEN yearsatcompany<=5 THEN '3-5 Yrs' WHEN yearsatcompany<=10 THEN '5-10 Yrs' ELSE '10+ Yrs' END AS tenure, COUNT(*) AS total, SUM(attrition_flag) AS left_company, ROUND(SUM(attrition_flag)*100.0/COUNT(*),1) AS rate_pct FROM employees GROUP BY tenure ORDER BY tenure",
        "8_Job Satisfaction"    : "SELECT jobsatisfaction, COUNT(*) AS total, SUM(attrition_flag) AS left_company, ROUND(SUM(attrition_flag)*100.0/COUNT(*),1) AS rate_pct FROM employees GROUP BY jobsatisfaction ORDER BY jobsatisfaction",
        "9_Dept+Overtime"       : "SELECT department, overtime, COUNT(*) AS total, SUM(attrition_flag) AS left_company, ROUND(SUM(attrition_flag)*100.0/COUNT(*),1) AS rate_pct FROM employees GROUP BY department, overtime ORDER BY rate_pct DESC",
    }

    for sheet_name, sql in queries.items():
        result_df = pd.read_sql_query(sql, conn)
        result_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"\n  Excel file saved: {excel_path}")

# Close the database connection — always do this at the end
conn.close()

print(f"\n{'=' * 60}")
print("  ALL QUERIES COMPLETE — PHASE 2 DONE!")
print(f"{'=' * 60}")
print("""
  What we answered:
  - WHAT  : Who is leaving, which dept, which role
  - WHY   : Overtime, low pay, low satisfaction, young age
  - HOW   : High-risk profiles identified

  Files saved:
  - hr_database.db        (SQLite database)
  - 02_hr_sql_results.xlsx (all query results, 9 sheets)

  Next step → Phase 3: Excel Cost Model
""")
