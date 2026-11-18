import sqlite3
import os
from datetime import datetime

db_path = 'apps/portal/internship.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT id, name, email, status FROM applications WHERE status IN ('Under Review', 'under_review')")
    rows = c.fetchall()
    print(f"Local DB: Found {len(rows)} Under Review applications.")
    
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for r in rows:
        app_id = r['id']
        old_status = r['status']
        c.execute("UPDATE applications SET status = 'Selected', updated_at = ? WHERE id = ?", (now_str, app_id))
        c.execute("""
            INSERT INTO application_status_history (
                application_id, old_status, new_status, changed_by, changed_at, reason
            ) VALUES (?, ?, 'Selected', 'admin', ?, 'Administrative Bulk Selection for Today Kickoff')
        """, (app_id, old_status, now_str))

    conn.commit()
    
    c.execute("SELECT count(*) FROM applications WHERE status IN ('Under Review', 'under_review')")
    print("Local DB: Remaining Under Review:", c.fetchone()[0])
    c.execute("SELECT count(*) FROM applications WHERE status = 'Selected'")
    print("Local DB: Total Selected:", c.fetchone()[0])
    conn.close()
