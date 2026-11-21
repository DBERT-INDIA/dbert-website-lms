import os, psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

c.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'enrollments'
    ORDER BY ordinal_position;
""")
for r in c.fetchall():
    print(f"  {r[0]} ({r[1]}, nullable={r[2]})")
