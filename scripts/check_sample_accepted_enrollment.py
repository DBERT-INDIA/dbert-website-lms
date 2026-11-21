import os, psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

c.execute("SELECT id, name, email, payment_status, deposit_paid, amount_paid, joining_date, batch_label, product, amount FROM enrollments WHERE payment_status = 'Accepted' ORDER BY id DESC LIMIT 3;")
for r in c.fetchall():
    print(r)
