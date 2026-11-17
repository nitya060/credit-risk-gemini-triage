import pandas as pd

# 1. Load the raw dataset from your data folder
df = pd.read_csv("data/raw_credit_data.csv")
initial_rows = len(df)

# 2. Audit Report (Proof of inspection for your portfolio)
print("--- STEP 1: RAW DATA AUDIT REPORT ---")
print(f"Total Rows & Columns: {df.shape}")
print("Missing Values Check:")
print(df.isnull().sum())

# 3. Data Cleaning & Standardization Pipeline
print("\n--- STEP 2: RUNNING DATA CLEANING ---")

# Fix column name: Remove space so it works smoothly in databases/SQL ("Loan to Income" -> "Loan_to_Income")
df = df.rename(columns={"Loan to Income": "Loan_to_Income"})

# Clean Age: Convert decimal ages (like 40.92) into clean whole-number integers
df["Age"] = df["Age"].astype(int)

# Standardize Precision: Round currency and ratios to clean financial decimal places
df["Income"] = df["Income"].round(2)
df["Loan"] = df["Loan"].round(2)
df["Loan_to_Income"] = df["Loan_to_Income"].round(4)

# Drop any duplicate rows if they exist
df = df.drop_duplicates()

# 4. Save the polished dataset into a new cleaned file
df.to_csv("data/cleaned_credit_data.csv", index=False)

print("\n--- STEP 3: CLEANING COMPLETE ---")
print(f"Successfully processed and retained {len(df)} rows.")
print("\nHere is a preview of your newly cleaned data:")
print(df)
