import sqlite3
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

conn = sqlite3.connect("apps/portal/internship.db")
c = conn.cursor()
targets = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]
for target in targets:
    c.execute("SELECT id, timestamp, email, subject, email_sent, provider, message_id, error_message FROM email_log WHERE email = ?", (target,))
    rows = c.fetchall()
    print(f"\nTarget: {target} -> found {len(rows)} rows:")
    for r in rows:
        print(" ", r)

print("\n--- All emails logged since 2026-11-04 00:00:00 ---")
c.execute("SELECT id, timestamp, email, subject, email_sent, provider FROM email_log WHERE timestamp >= '2026-11-04 00:00:00' ORDER BY id ASC")
for r in c.fetchall():
    print(" ", r)

conn.close()
