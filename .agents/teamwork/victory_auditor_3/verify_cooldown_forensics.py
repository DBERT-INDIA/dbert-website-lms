import sqlite3
import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

dbs = glob.glob('**/*.db', recursive=True)
print(f'Total SQLite databases found: {len(dbs)}')

target_emails = ['ain.sharma.abhinav@gmail.com', 'ajnatechrpa@gmail.com']

for db in dbs:
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        
        for tname in tables:
            cursor.execute(f"PRAGMA table_info({tname})")
            cols = [col[1] for col in cursor.fetchall()]
            
            email_cols = [c for c in cols if any(k in c.lower() for k in ['email', 'recipient', 'to', 'addr'])]
            
            if 'email_log' in tname.lower():
                print(f"\n=== Database: {db} | Table: {tname} ===")
                cursor.execute(f"SELECT count(*) FROM {tname}")
                total = cursor.fetchone()[0]
                print(f"Total records in {tname}: {total}")
                
                # Check for target recipients in email_log
                for target in target_emails:
                    cursor.execute(f"SELECT rowid, * FROM {tname} WHERE email LIKE ?", (f"%{target}%",))
                    target_rows = cursor.fetchall()
                    print(f"  Rows matching '{target}': {len(target_rows)}")
                    for r in target_rows:
                        # Print timestamp and subject/status
                        print(f"    Target Row: {r}")
                
                # Check for any records created recently (after Nov 4, 2026)
                cursor.execute(f"SELECT rowid, email, subject, status, timestamp FROM {tname} WHERE timestamp >= '2026-11-04' ORDER BY timestamp DESC")
                nov_rows = cursor.fetchall()
                print(f"  Rows in November 2026: {len(nov_rows)}")
                for nr in nov_rows[:20]:
                    print(f"    Recent Nov: {nr}")

        conn.close()
    except Exception as e:
        print(f"Error checking {db}: {e}")
