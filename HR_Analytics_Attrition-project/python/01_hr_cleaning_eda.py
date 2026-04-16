# =============================================================================
# PROJECT 1 — HR Analytics | Simple Cleaning Script
# =============================================================================

import pandas as pd
import os

# --- FILE PATHS ---
RAW_PATH   = r"C:\Users\dell\Downloads\HR_Analytics_Project\data\raw\WA_Fn-UseC_-HR-Employee-Attrition.csv"
CLEAN_PATH = r"C:\Users\dell\Downloads\HR_Analytics_Project\data\clean\hr_clean.csv"
OUTPUT_DIR = r"C:\Users\dell\Downloads\HR_Analytics_Project\outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)

# --- STEP 1: LOAD DATA ---
print("Loading data...")
df = pd.read_csv(RAW_PATH)
print(f"Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")

# --- STEP 2: CHECK MISSING VALUES ---
print("\nMissing values:", df.isnull().sum().sum())

# --- STEP 3: REMOVE DUPLICATES ---
before = len(df)
df = df.drop_duplicates()
print(f"Duplicates removed: {before - len(df)}")

# --- STEP 4: REMOVE USELESS COLUMNS ---
df = df[[col for col in df.columns if df[col].nunique() > 1]]
print(f"Columns after cleanup: {df.shape[1]}")

# --- STEP 5: CLEAN COLUMN NAMES ---
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# --- STEP 6: ADD ATTRITION FLAG ---
df["attrition_flag"] = df["attrition"].map({"Yes": 1, "No": 0})

# --- STEP 7: KEY NUMBERS ---
total  = len(df)
left   = int(df["attrition_flag"].sum())
stayed = total - left
rate   = round((left / total) * 100, 1)

print("\n========== ATTRITION SUMMARY ==========")
print(f"Total employees     : {total}")
print(f"Employees who left  : {left}")
print(f"Employees who stayed: {stayed}")
print(f"Attrition rate      : {rate}%")
print("========================================")

# --- STEP 8: ATTRITION BY DEPARTMENT ---
print("\nAttrition by Department:")
dept = df.groupby("department")["attrition_flag"].agg(Total="count", Left="sum")
dept["Rate %"] = (dept["Left"] / dept["Total"] * 100).round(1)
print(dept.sort_values("Rate %", ascending=False))

# --- STEP 9: ATTRITION BY JOB ROLE ---
# Note: column name is 'jobrole' (no underscore) after our name cleaning
print("\nAttrition by Job Role:")
role = df.groupby("jobrole")["attrition_flag"].agg(Total="count", Left="sum")
role["Rate %"] = (role["Left"] / role["Total"] * 100).round(1)
print(role.sort_values("Rate %", ascending=False))

# --- STEP 10: AVERAGE INCOME — LEFT vs STAYED ---
print("\nAverage Monthly Income:")
income = df.groupby("attrition")["monthlyincome"].mean().round(0)
print(income)

# --- STEP 11: OVERTIME vs ATTRITION ---
print("\nOvertime vs Attrition:")
ot = df.groupby("overtime")["attrition_flag"].agg(Total="count", Left="sum")
ot["Rate %"] = (ot["Left"] / ot["Total"] * 100).round(1)
print(ot)

# --- STEP 12: SAVE CLEAN FILE ---
df.to_csv(CLEAN_PATH, index=False)
print(f"\nClean file saved to: {CLEAN_PATH}")
print("\nDONE! Phase 1 complete.")

