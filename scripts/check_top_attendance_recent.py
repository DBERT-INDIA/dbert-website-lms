import os, psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

print("=== CURRENT WEEK (2026-11-15 to 2026-11-21) TOP 15 INTERNS ===")
c.execute("""
    SELECT a.intern_id, ia.name, a.email, a.total_minutes, round(a.total_minutes/60.0, 2) as hrs, a.updated_at
    FROM attendance a
    LEFT JOIN intern_accounts ia ON ia.id = a.intern_id
    WHERE a.week_start = '2026-11-15'
    ORDER BY a.total_minutes DESC
    LIMIT 15;
""")
for r in c.fetchall():
    print(f"  Intern #{r[0]}: {r[1]} ({r[2]}) -> {r[3]} mins ({r[4]} hrs) [Last Active: {r[5]}]")

print("\n=== PREVIOUS WEEK (2026-11-08 to 2026-11-14) TOP 15 INTERNS ===")
c.execute("""
    SELECT a.intern_id, ia.name, a.email, a.total_minutes, round(a.total_minutes/60.0, 2) as hrs, a.updated_at
    FROM attendance a
    LEFT JOIN intern_accounts ia ON ia.id = a.intern_id
    WHERE a.week_start = '2026-11-08'
    ORDER BY a.total_minutes DESC
    LIMIT 15;
""")
for r in c.fetchall():
    print(f"  Intern #{r[0]}: {r[1]} ({r[2]}) -> {r[3]} mins ({r[4]} hrs) [Last Active: {r[5]}]")
