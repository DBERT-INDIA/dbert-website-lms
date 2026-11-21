import os, sys, psycopg2, json
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

email = 'ratnadeepratu737@gmail.com'

print("=== APPLICATIONS ===")
c.execute("SELECT id, name, email, phone, domain, college, status, created_at, reviewed_at FROM applications WHERE LOWER(email) = %s;", (email,))
for r in c.fetchall():
    print(r)

print("\n=== INTERN_ACCOUNTS ===")
c.execute("SELECT id, application_id, name, email, phone, domain, signup_stage, account_status, is_active FROM intern_accounts WHERE LOWER(email) = %s;", (email,))
for r in c.fetchall():
    print(r)

print("\n=== INTERN_OFFER_LETTERS ===")
c.execute("SELECT id, offer_letter_id, intern_id, enrollment_id, email, name, domain, caution_deposit_status, pdf_unlocked, batch_start_date FROM intern_offer_letters WHERE LOWER(email) = %s;", (email,))
for r in c.fetchall():
    print(r)

print("\n=== ENROLLMENTS ===")
c.execute("SELECT id, name, email, phone, domain, joining_date, payment_status, utr, amount FROM enrollments WHERE LOWER(email) = %s;", (email,))
for r in c.fetchall():
    print(r)

print("\n=== COURSE_ENROLLMENTS_499 ===")
try:
    c.execute("SELECT * FROM course_enrollments_499 WHERE LOWER(email) = %s;", (email,))
    for r in c.fetchall():
        print(r)
except Exception as e:
    print(f"Error checking course_enrollments_499: {e}")
    conn.rollback()

print("\n=== PAYMENTS ===")
try:
    c.execute("SELECT * FROM payments WHERE LOWER(email) = %s;", (email,))
    for r in c.fetchall():
        print(r)
except Exception as e:
    print(f"Error checking payments: {e}")
    conn.rollback()
