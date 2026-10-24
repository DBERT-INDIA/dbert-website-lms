import sqlite3
conn = sqlite3.connect('apps/portal/internship.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
print("Tables:", tables)

for t in ['interns', 'post_applications', 'scraped_internships', 'posts']:
    if t in tables:
        c.execute(f"PRAGMA table_info({t})")
        print(f"\n{t} columns:", [r[1] for r in c.fetchall()])
