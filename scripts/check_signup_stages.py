import os, psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

c.execute("SELECT signup_stage, account_status, count(*) FROM intern_accounts GROUP BY signup_stage, account_status ORDER BY count(*) DESC;")
for r in c.fetchall():
    print(r)
