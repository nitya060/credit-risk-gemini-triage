import pandas as pd

# 1. Load the engineered dataset from Day 3
df = pd.read_csv("data/engineered_credit_data.csv")

print("--- STEP 1: LOADED ENGINEERED PORTFOLIO ---")
print(f"Total Borrowers in Portfolio: {len(df)}")

# 2. Triage Query: Filter specifically for High-Risk Borrowers
high_risk_df = df[df["Risk_Tier"] == "High Risk"]

print(f"\n--- STEP 2: HIGH-RISK BORROWER TRIAGE QUEUE ---")
print(f"Total High-Risk Applicants Flagged for Review: {len(high_risk_df)}")
print("Preview of High-Risk Borrowers:")
print(high_risk_df[["Income", "Loan", "Loan_to_Income", "Default"]])

# 3. Financial Analysis: Calculate Default Rate Percentage by Risk Tier
print("\n--- STEP 3: PORTFOLIO RISK AUDIT (Default Rate by Tier) ---")
# Group by Risk Tier and calculate the percentage of defaults
default_analysis = df.groupby("Risk_Tier")["Default"].mean() * 100
default_analysis = default_analysis.round(2)

desired_order = ["High Risk", "Moderate Risk", "Low Risk"]
default_analysis = default_analysis.reindex(desired_order)

for tier, rate in default_analysis.items():
    print(f"-> {tier} Default Rate: {rate}%")

# 4. Export the specialized High-Risk queue for loan officers
high_risk_df.to_csv("data/high_risk_triage_queue.csv", index=False)

print("\n--- STEP 4: TRIAGE ASSISTANT COMPLETE ---")
print("Successfully exported prioritized review list as 'high_risk_triage_queue.csv'.")
