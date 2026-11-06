import sqlite3
import glob
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

print("=== DEEP DIVE: EMAIL LOG RECORDS FOR 2026-11 AND TARGET RECIPIENTS ===")
dbs = glob.glob("**/*.db", recursive=True)

for db in dbs:
    if os.path.getsize(db) == 0:
        continue
    try:
        conn = sqlite3.connect(db)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        if "email_log" in tables:
            print(f"\nDB: {db}")
            # Check maximum timestamp in table
            cur.execute("SELECT MAX(timestamp), MIN(timestamp), COUNT(*) FROM email_log")
            max_ts, min_ts, cnt = cur.fetchone()
            print(f"  Total records: {cnt}, Min TS: {min_ts}, Max TS: {max_ts}")
            
            # Check any record in November 2026
            cur.execute("SELECT * FROM email_log WHERE timestamp LIKE '2026-11%'")
            nov_rows = cur.fetchall()
            print(f"  Records from 2026-11: {len(nov_rows)}")
            for r in nov_rows:
                print("    NOV ROW:", dict(r))
                
            # Check target recipients anytime
            cur.execute("SELECT * FROM email_log WHERE email LIKE '%ain.sharma%' OR email LIKE '%ajnatechrpa%'")
            target_rows = cur.fetchall()
            print(f"  Target recipient rows (ain.sharma / ajnatechrpa): {len(target_rows)}")
            for tr in target_rows:
                print("    TARGET ROW:", dict(tr))

            # Check any record with email_sent = 'YES' in all of 2026
            cur.execute("SELECT COUNT(*) FROM email_log WHERE email_sent = 'YES'")
            yes_cnt = cur.fetchone()[0]
            print(f"  Total with email_sent='YES': {yes_cnt}")
            if yes_cnt > 0:
                cur.execute("SELECT * FROM email_log WHERE email_sent = 'YES' ORDER BY rowid DESC LIMIT 5")
                for yr in cur.fetchall():
                    print("    YES ROW:", dict(yr))
        conn.close()
    except Exception as e:
        print(f"Error inspecting {db}: {e}")
