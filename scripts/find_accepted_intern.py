import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

c.execute("""
    SELECT a.id, a.email, a.status as app_status, enr.payment_status, enr.batch_label, ia.name
    FROM applications a
    JOIN intern_accounts ia ON LOWER(ia.email) = LOWER(a.email)
    LEFT JOIN enrollments enr ON LOWER(enr.email) = LOWER(a.email)
    WHERE a.status = 'Accepted'
    ORDER BY a.id DESC
    LIMIT 5;
""")
for r in c.fetchall():
    print(r)
