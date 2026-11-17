import os
import sqlite3
from google import genai
import pandas as pd

conn = sqlite3.connect("data/credit_risk.db")
top_risk_df = pd.read_sql(
    "SELECT * FROM v_high_risk_queue ORDER BY Loan_to_Income DESC LIMIT 1;",
    conn,
)
conn.close()

borrower = top_risk_df.iloc[0]

prompt = f"""
You are a Senior Credit Risk Underwriter. Write a concise, formal Credit Underwriting Memo for this flagged high-risk loan applicant extracted from our SQLite database:

- Annual Income: ${borrower['Income']:,.2f}
- Requested Loan Amount: ${borrower['Loan']:,.2f}
- Loan-to-Income (LTI) Ratio: {borrower['Loan_to_Income']:.2%}
- Historical Default Flag: {int(borrower['Default'])}

Structure the memo with:
1. Executive Risk Summary
2. Key Financial Ratios & Stress Indicators
3. Final Underwriting Recommendation (Approve with Conditions, Decline, or Request Collateral)
"""

memo_text = ""
try:
  print("Attempting connection to Gemini API...")
  client = genai.Client()  
  response = client.models.generate_content(
      model="gemini-1.5-flash",
      contents=prompt,
  )
  memo_text = response.text
  print("Successfully generated memo using Gemini AI!")
except Exception as e:
  print(
      f"API Key not detected locally ({e}). Falling back to automated template"
      " generator for local execution."
  )
  
  memo_text = f"""# Credit Underwriting Memo: High-Risk Triage

Applicant Financial Profile
- Annual Income: ${borrower['Income']:,.2f}
- Requested Loan Amount: ${borrower['Loan']:,.2f}
- Loan-to-Income (LTI) Ratio: {borrower['Loan_to_Income']:.2%}
- Historical Default Flag: {int(borrower['Default'])}

1. Executive Risk Summary
The applicant has been flagged in the automated `v_high_risk_queue` due to an elevated Loan-to-Income (LTI) ratio of {borrower['Loan_to_Income']:.2%}. Immediate risk mitigation and portfolio exposure controls are required prior to capital disbursement.

2. Key Financial Ratios & Stress Indicators
- Debt Service Capacity: The requested facility of ${borrower['Loan']:,.2f} relative to an annual income of ${borrower['Income']:,.2f} presents severe cash flow vulnerability under macroeconomic stress testing.
- Default Probability: High statistical correlation with historical default cohorts exhibiting leveraged retail debt profiles.

 3. Final Underwriting Recommendation
- Conditional Decline / Collateral Requirement: Recommend declining the unsecured credit facility unless secondary liquid collateral or a qualified co-signer is formally attached to the underwriting agreement.
"""

print("\n--- FINAL UNDERWRITING MEMO OUTPUT ---")
print(memo_text)

os.makedirs("output", exist_ok=True)
with open("output/underwriting_memo.md", "w", encoding="utf-8") as f:
  f.write(memo_text)

print("\nSuccessfully saved memo to output/underwriting_memo.md!")

