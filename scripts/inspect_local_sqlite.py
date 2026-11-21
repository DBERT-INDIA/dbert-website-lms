import sqlite3

conn = sqlite3.connect('apps/portal/internship.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in c.fetchall()]
print(f"Local internship.db tables ({len(tables)}):", tables[:25])

for t in ['attendance', 'enrollments', 'user_sessions', 'login_history', 'study_sessions', 'intern_accounts', 'applications']:
    if t in tables:
        c.execute(f"SELECT count(*) FROM {t}")
        cnt = c.fetchone()[0]
        print(f"  {t}: {cnt} rows")
        if t == 'attendance':
            c.execute("SELECT week_start, count(*), sum(CASE WHEN total_minutes>=600 THEN 1 ELSE 0 END) FROM attendance GROUP BY week_start ORDER BY week_start DESC LIMIT 6;")
            print("  Attendance breakdown:")
            for w in c.fetchall():
                print(f"    Week {w[0]}: {w[1]} records, {w[2]} completed >= 10h")

conn.close()
