import os, psycopg2, json
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

emails = [
    'ratnadeepratu737@gmail.com',
    'sabreensaed861@gmail.com',
    'anvisha70917@gmail.com',
    'srimathiece157@gmail.com',
    'ritwikaabanerjee5@gmail.com',
    'sagarabhinand342@gmail.com',
    'srgayathri0519@gmail.com',
    'karthikaraja112008@gmail.com',
    'srikarivaranasi05@gmail.com',
    'muguntharajank@gmail.com'
]

for email in emails:
    c.execute("""
        SELECT ia.id, ia.name, ia.email, ia.signup_stage, ia.account_status,
               a.id, a.status, a.domain
        FROM applications a
        LEFT JOIN intern_accounts ia ON LOWER(ia.email) = LOWER(a.email)
        WHERE LOWER(a.email) = %s;
    """, (email,))
    rows = c.fetchall()
    print(f"Email: {email} -> {rows}")
