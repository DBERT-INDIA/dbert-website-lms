import sqlite3
import os
import glob
from datetime import datetime, timedelta

import sqlite3
import os
import subprocess
from datetime import datetime, timedelta

def check_local_db():
    print("=== LOCAL DATABASE CHECK ===")
    db_path = 'apps/portal/internship.db'
    if not os.path.exists(db_path):
        print(f"File {db_path} does not exist.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT status, count(*) FROM applications GROUP BY status")
    print("\nApplications by status (Local):")
    for row in c.fetchall():
        print(f"  {row[0]}: {row[1]}")

    c.execute("SELECT count(*) FROM applications WHERE status IN ('Under Review', 'under_review', 'UNDER_REVIEW')")
    under_review_count = c.fetchone()[0]
    print(f"\nTotal 'Under Review': {under_review_count}")

    # Check status history
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='application_status_history'")
    if c.fetchone():
        print("\nChecking application_status_history...")
        c.execute("PRAGMA table_info(application_status_history)")
        print("Columns:", [r[1] for r in c.fetchall()])
        c.execute("""
            SELECT * FROM application_status_history 
            WHERE new_status IN ('Selected', 'selected')
            ORDER BY id DESC LIMIT 10
        """)
        for r in c.fetchall():
            print("  History:", dict(r))

    conn.close()

def check_ec2_db():
    print("\n=== EC2 PRODUCTION DATABASE CHECK ===")
    ssh_cmd = [
        "ssh", "-i", r"C:\Users\user\.ssh\dbert-production-server.pem",
        "-o", "StrictHostKeyChecking=no",
        "ubuntu@3.26.237.171",
        "python3 - << 'EOF'\n"
        "import sqlite3, os\n"
        "from datetime import datetime, timedelta\n"
        "db_path = '/var/www/dbert-website-lms/apps/portal/internship.db'\n"
        "conn = sqlite3.connect(db_path)\n"
        "conn.row_factory = sqlite3.Row\n"
        "c = conn.cursor()\n"
        "print('--- Applications by status on EC2 ---')\n"
        "c.execute('SELECT status, count(*) FROM applications GROUP BY status')\n"
        "for r in c.fetchall():\n"
        "    print(f'  {r[0]}: {r[1]}')\n"
        "\n"
        "c.execute('SELECT count(*) FROM applications WHERE status IN (\"Under Review\", \"under_review\")')\n"
        "print('Total Under Review on EC2:', c.fetchone()[0])\n"
        "\n"
        "c.execute('SELECT id, name, email, phone, domain, created_at, updated_at FROM applications WHERE status IN (\"Under Review\", \"under_review\") ORDER BY id DESC')\n"
        "under_rev = c.fetchall()\n"
        "print(f'Under Review rows: {len(under_rev)}')\n"
        "for r in under_rev:\n"
        "    print(f'  id={r[\"id\"]}, name={r[\"name\"]}, email={r[\"email\"]}, phone={r[\"phone\"]}, created={r[\"created_at\"]}')\n"
        "\n"
        "# Status changed to Selected in last 7 days\n"
        "seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')\n"
        "print(f'--- Status history to Selected since {seven_days_ago} ---')\n"
        "try:\n"
        "    c.execute('SELECT count(*) FROM application_status_history WHERE new_status=\"Selected\" AND changed_at >= ?', (seven_days_ago,))\n"
        "    print('History count to Selected in last 7 days:', c.fetchone()[0])\n"
        "    c.execute('SELECT h.*, a.name, a.email, a.phone FROM application_status_history h JOIN applications a ON h.application_id = a.id WHERE h.new_status=\"Selected\" AND h.changed_at >= ? ORDER BY h.id DESC', (seven_days_ago,))\n"
        "    hist_rows = c.fetchall()\n"
        "    for r in hist_rows[:20]:\n"
        "        print('  Selected in 7d (history):', dict(r))\n"
        "except Exception as e:\n"
        "    print('History query error:', e)\n"
        "\n"
        "# Also check applications table updated_at for Selected\n"
        "c.execute('SELECT count(*) FROM applications WHERE status=\"Selected\" AND (updated_at >= ? OR created_at >= ?)', (seven_days_ago, seven_days_ago))\n"
        "print(f'Applications table: status=Selected and updated/created in last 7 days: {c.fetchone()[0]}')\n"
        "c.execute('SELECT count(*) FROM applications WHERE status=\"Selected\"')\n"
        "print(f'Applications table: total status=Selected: {c.fetchone()[0]}')\n"
        "conn.close()\n"
        "EOF\n"
    ]
    res = subprocess.run(ssh_cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)

if __name__ == '__main__':
    check_local_db()
    check_ec2_db()


if __name__ == '__main__':
    check_local_db()
