import random
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/credit_risk.db")
cursor = conn.cursor()

df = pd.read_csv("data/engineered_credit_data.csv")
df.to_sql("portfolio", conn, if_exists="replace", index=False)

cursor.execute("DROP VIEW IF EXISTS v_high_risk_queue;")
cursor.execute("CREATE VIEW v_high_risk_queue AS SELECT Income, Loan, Loan_to_Income, [Default] FROM portfolio WHERE Risk_Tier = 'High Risk';")

cursor.execute("CREATE TABLE IF NOT EXISTS underwriting_audit_log (Log_ID INTEGER PRIMARY KEY AUTOINCREMENT, Review_Date TEXT, Total_High_Risk_Flagged INTEGER, Action_Taken TEXT);")
cursor.execute("""
    INSERT INTO underwriting_audit_log (Review_Date, Total_High_Risk_Flagged, Action_Taken) 
    VALUES (
        DATE('now'), 
        MAX(0, (SELECT COUNT(*) FROM v_high_risk_queue) - (SELECT COUNT(*) FROM underwriting_audit_log)), 
        'Sent to Senior Underwriting Queue'
    );
""")
conn.commit()

possible_decisions = [
    "Approved by Senior Underwriter",
    "Declined by Senior Underwriter",
    "Pending Further Documentation"
]
cursor.execute("SELECT Log_ID FROM underwriting_audit_log WHERE Action_Taken = 'Sent to Senior Underwriting Queue';")
pending_ids = cursor.fetchall()

for (log_id,) in pending_ids:
    decision = random.choice(possible_decisions)
    cursor.execute("UPDATE underwriting_audit_log SET Action_Taken = ? WHERE Log_ID = ?;", (decision, log_id))

conn.commit()

cursor.execute("""
    UPDATE underwriting_audit_log 
    SET Total_High_Risk_Flagged = MAX(0, (SELECT COUNT(*) FROM v_high_risk_queue) - (Log_ID - 1));
""")
conn.commit()

print("--- LIVE SQL VIEW: HIGH-RISK QUEUE SAMPLE ---")
print(pd.read_sql("SELECT * FROM v_high_risk_queue", conn))

print("\n--- RELATIONAL AUDIT LOG TABLE ---")
print(pd.read_sql("SELECT * FROM underwriting_audit_log", conn))

conn.close()
print("\nRelational SQL database pipeline executed successfully.")
