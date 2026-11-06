import sqlite3
import glob
import os
import sys

print("=== FORENSIC SQLite DB SCAN ===")
dbs = glob.glob("**/*.db", recursive=True)
print(f"Found {len(dbs)} database file(s): {dbs}")

for db in dbs:
    print(f"\nDatabase: {db} (Size: {os.path.getsize(db)} bytes)")
    try:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        print(f"Tables: {tables}")
        if "email_log" in tables:
            cur.execute("PRAGMA table_info(email_log)")
            cols = [r[1] for r in cur.fetchall()]
            print(f"email_log columns: {cols}")
            
            cur.execute("SELECT COUNT(*) FROM email_log")
            total = cur.fetchone()[0]
            print(f"Total entries in email_log: {total}")
            
            cur.execute("SELECT * FROM email_log ORDER BY rowid DESC LIMIT 50")
            recent = cur.fetchall()
            print("Recent 50 records in email_log:")
            for r in recent:
                row_dict = dict(r)
                print("  ", row_dict)
                
            # Specifically check for ain.sharma.abhinav@gmail.com and ajnatechrpa@gmail.com
            cur.execute("SELECT * FROM email_log WHERE email LIKE '%ain.sharma%' OR email LIKE '%ajnatechrpa%'")
            matches = cur.fetchall()
            print(f"\nTarget recipient entries (ain.sharma / ajnatechrpa): {len(matches)}")
            for m in matches:
                print("  Target match:", dict(m))
                
            # Specifically check for any row with email_sent = 'YES' or sent != 'SKIPPED'
            cur.execute("SELECT * FROM email_log WHERE email_sent = 'YES'")
            yes_rows = cur.fetchall()
            print(f"\nEntries with email_sent = 'YES': {len(yes_rows)}")
            for yr in yes_rows:
                print("  LIVE SENT:", dict(yr))
        conn.close()
    except Exception as e:
        print(f"Error inspecting {db}: {e}")
