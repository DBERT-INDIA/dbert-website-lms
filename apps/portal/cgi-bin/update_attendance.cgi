#!/usr/bin/python3
import sys
import os
import sqlite3
from datetime import datetime

print("Content-Type: text/plain\n")

try:
    # Locate the internship.db file in the app root directory
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(app_dir, 'internship.db')
    
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        sys.exit(0)

    conn = sqlite3.connect(db_path)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. 20 Sept - 26 Sept
    cur1 = conn.execute(
        """
        UPDATE attendance 
        SET total_minutes = 600, updated_at = ?
        WHERE week_start = '2026-09-20' AND total_minutes >= 30 AND total_minutes < 600
        """,
        (now_str,)
    )
    print(f"SUCCESS: Updated {cur1.rowcount} interns to 10 hours for the week of 20 Sept - 26 Sept.")

    # 2. 27 Sept - 3 Oct (Update existing)
    cur2 = conn.execute(
        """
        UPDATE attendance
        SET total_minutes = 210, updated_at = ?
        WHERE week_start = '2026-09-27' AND total_minutes < 210
        """,
        (now_str,)
    )
    print(f"SUCCESS: Updated {cur2.rowcount} existing attendance records to 3.5 hours for the current week.")

    # 3. 27 Sept - 3 Oct (Insert for everyone else)
    cur3 = conn.execute(
        """
        INSERT INTO attendance (intern_id, email, week_start, week_end, total_minutes, updated_at)
        SELECT id, email, '2026-09-27', '2026-10-03', 210, ?
        FROM intern_accounts
        WHERE is_active = 1
          AND id NOT IN (
              SELECT intern_id FROM attendance WHERE week_start = '2026-09-27'
          )
        """,
        (now_str,)
    )
    print(f"SUCCESS: Inserted {cur3.rowcount} new attendance records with 3.5 hours for the current week.")

    conn.commit()
    conn.close()
    
    print("\nDatabase updated successfully! You can now delete this file from your cgi-bin directory.")

except Exception as e:
    import traceback
    print("A Python Error Occurred:")
    print("-" * 50)
    traceback.print_exc(file=sys.stdout)
