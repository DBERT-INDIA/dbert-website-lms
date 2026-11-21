import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect('data/dbert_whatsapp.db')
cur = conn.cursor()

cur.execute("""
    SELECT intern_id, name, email, phone, cert_id, account_used, status, error_message, sent_at
    FROM stipend_dispatch_log
    WHERE id IN (
        SELECT MAX(id) FROM stipend_dispatch_log GROUP BY intern_id
    )
    ORDER BY intern_id ASC
""")
rows = cur.fetchall()

csv_path = "data/dispatch_tracking_stipend_299.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["intern_id", "name", "email", "phone", "cert_id", "account_used", "status", "error_message", "sent_at"])
    for r in rows:
        writer.writerow(r)

print(f"Exported {len(rows)} records to {csv_path}")

sent_count = sum(1 for r in rows if r[6] == 'SENT')
fail_count = sum(1 for r in rows if r[6] != 'SENT')
print(f"SENT: {sent_count}, FAILED: {fail_count}")
