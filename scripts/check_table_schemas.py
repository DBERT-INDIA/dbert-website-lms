import os, psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

c.execute("""
    SELECT table_schema, table_name 
    FROM information_schema.tables 
    WHERE table_name IN ('intern_accounts', 'enrollments', 'applications', 'attendance');
""")
for r in c.fetchall():
    print(r)
