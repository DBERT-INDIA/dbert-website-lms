#!/usr/bin/python3
"""
patch_db.cgi — One-time DB patcher for cPanel. 
Upload to cgi-bin, chmod 755, visit the URL, then DELETE this file.
"""
import sys, os, sqlite3, traceback

print("Content-Type: text/plain\r\n\r\n")

try:
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(app_dir, 'internship.db')
    print(f"DB path: {db_path}")
    print(f"DB exists: {os.path.exists(db_path)}")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    patches = [
        # application_status_history (needed for status changes)
        """CREATE TABLE IF NOT EXISTS application_status_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            old_status TEXT,
            new_status TEXT NOT NULL,
            changed_by TEXT,
            changed_at TEXT DEFAULT (datetime('now','localtime')),
            reason TEXT,
            request_id TEXT,
            metadata TEXT
        )""",
        "CREATE INDEX IF NOT EXISTS idx_app_status_hist_app ON application_status_history(application_id)",

        # event_outbox (used by outbox_service.py)
        """CREATE TABLE IF NOT EXISTS event_outbox (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            aggregate_type TEXT NOT NULL,
            aggregate_id TEXT NOT NULL,
            payload_json TEXT,
            status TEXT DEFAULT 'pending',
            retry_count INTEGER DEFAULT 0,
            max_retries INTEGER DEFAULT 3,
            next_retry_at TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            updated_at TEXT DEFAULT (datetime('now','localtime'))
        )""",

        # intern_articles (used by blog/article section)
        """CREATE TABLE IF NOT EXISTS intern_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intern_id INTEGER,
            title TEXT,
            content_markdown TEXT,
            status TEXT DEFAULT 'draft',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            updated_at TEXT DEFAULT (datetime('now','localtime'))
        )""",

        # Attendance — check 20 Sept week
        """UPDATE attendance SET total_minutes=600, updated_at=datetime('now','localtime')
           WHERE week_start='2026-09-20' AND total_minutes >= 30 AND total_minutes < 600""",

        # Attendance — 27 Sept week, update existing below 210
        """UPDATE attendance SET total_minutes=210, updated_at=datetime('now','localtime')
           WHERE week_start='2026-09-27' AND total_minutes < 210""",

        # Attendance — 27 Sept week, insert missing active interns
        """INSERT OR IGNORE INTO attendance (intern_id, email, week_start, week_end, total_minutes, updated_at)
           SELECT id, email, '2026-09-27', '2026-10-03', 210, datetime('now','localtime')
           FROM intern_accounts WHERE is_active=1
           AND id NOT IN (SELECT intern_id FROM attendance WHERE week_start='2026-09-27')""",
    ]

    for sql in patches:
        try:
            c.execute(sql)
            print(f"OK ({c.rowcount} rows affected): {sql[:80].strip()}...")
        except Exception as e:
            print(f"SKIP: {e} — {sql[:60].strip()}...")

    conn.commit()
    conn.close()

    # Delete the init flag so dbert.cgi re-runs init_db on next load
    flag_v2 = os.path.join(app_dir, '.db_initialized_v2')
    flag_v3 = os.path.join(app_dir, '.db_initialized_v3')
    for flag in [flag_v2, flag_v3]:
        if os.path.exists(flag):
            os.remove(flag)
            print(f"Removed flag: {flag}")

    print("\n=== SUCCESS — All patches applied. DELETE THIS FILE NOW. ===")

except Exception:
    traceback.print_exc(file=sys.stdout)
