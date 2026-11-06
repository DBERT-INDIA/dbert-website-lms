import sqlite3
import glob
import os
import sys

print("=== Checking all SQLite databases for email_log ===")
for p in glob.glob("**/*.db", recursive=True):
    try:
        conn = sqlite3.connect(p)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='email_log'")
        if c.fetchone():
            print(f"\nDatabase: {p}")
            # Check columns
            c.execute("PRAGMA table_info(email_log)")
            cols = [col[1] for col in c.fetchall()]
            print(f"Columns: {cols}")
            c.execute("SELECT * FROM email_log ORDER BY rowid DESC LIMIT 20")
            rows = c.fetchall()
            print(f"Latest {len(rows)} entries:")
            for r in rows:
                print(" ", r)
        conn.close()
    except Exception as e:
        print(f"Error on {p}: {e}")
