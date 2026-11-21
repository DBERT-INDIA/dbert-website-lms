import os, psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

c.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'dbert_internship' 
    ORDER BY table_name;
""")
tables = [r[0] for r in c.fetchall()]
print(f"Total tables in dbert_internship schema: {len(tables)}")
for t in tables:
    print(" ", t)
