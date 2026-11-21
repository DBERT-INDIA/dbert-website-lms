import sqlite3
import os
import json
from datetime import datetime

# Check SQLite DB
print("=== Checking data/dbert_whatsapp.db ===")
if os.path.exists("data/dbert_whatsapp.db"):
    conn = sqlite3.connect("data/dbert_whatsapp.db")
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in c.fetchall()]
    print("Tables in dbert_whatsapp.db:", tables)
    for t in tables:
        c.execute(f"SELECT count(*) FROM {t};")
        print(f"  {t}: {c.fetchone()[0]} rows")
        c.execute(f"PRAGMA table_info({t});")
        cols = [r[1] for r in c.fetchall()]
        print(f"    cols: {cols}")
    conn.close()
else:
    print("data/dbert_whatsapp.db not found!")

# Check other potential tracking files
for fn in [
    "data/dispatch_tracking_stipend_299.csv",
    "data/dbert_unified_omnichannel_tracking.csv",
    "data/dbert_whatsapp_sent_today.json",
    "data/campaign_dispatch_acc1.json",
    "data/campaign_dispatch_acc2.json"
]:
    if os.path.exists(fn):
        print(f"Found {fn} (Size: {os.path.getsize(fn)} bytes)")
