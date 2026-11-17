import pandas as pd

# 1. Load the cleaned dataset from Day 2
df = pd.read_csv("data/cleaned_credit_data.csv")

print("--- STEP 1: LOADED CLEANED DATA ---")
print(f"Total Rows to Process: {len(df)}")

# 2. Feature Engineering: Assigning Credit Risk Tiers based on Debt-to-Income (Loan_to_Income)
def assign_risk_tier(dti):
    if dti < 0.08:
        return "Low Risk"
    elif dti <= 0.15:
        return "Moderate Risk"
    else:
        return "High Risk"

# Apply the custom risk logic across every single borrower row
df["Risk_Tier"] = df["Loan_to_Income"].apply(assign_risk_tier)

# 3. Audit Portfolio Risk Distribution
print("\n--- STEP 2: PORTFOLIO RISK TIER BREAKDOWN ---")
risk_counts = df["Risk_Tier"].value_counts()
print(risk_counts)

# 4. Save the final engineered dataset for your triage assistant
df.to_csv("data/engineered_credit_data.csv", index=False)

print("\n--- STEP 3: FEATURE ENGINEERING COMPLETE ---")
print("Saved final portfolio file as 'engineered_credit_data.csv'.")
print("\nHere is a preview of your risk-tiered borrowers:")
print(df[["Income", "Loan", "Loan_to_Income", "Risk_Tier", "Default"]])
