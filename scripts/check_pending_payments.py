import psycopg2
import json

DB_URL = "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms"
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

cur.execute("SELECT DISTINCT payment_status, COUNT(*) FROM enrollments GROUP BY payment_status")
print("Enrollments payment_status:", cur.fetchall())

cur.execute("SELECT COUNT(*) FROM enrollments WHERE utr IS NOT NULL AND utr != ''")
print("Enrollments with UTR:", cur.fetchall())

cur.execute("SELECT COUNT(*) FROM enrollments WHERE payment_screenshot IS NOT NULL AND payment_screenshot != ''")
print("Enrollments with payment_screenshot:", cur.fetchall())

# Look at applications status
cur.execute("SELECT DISTINCT status, COUNT(*) FROM applications GROUP BY status")
print("Applications status:", cur.fetchall())

# Look at tables
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [r[0] for r in cur.fetchall()]
pay_tables = [t for t in tables if any(k in t for k in ['pay', 'enroll', 'cert', 'submiss', 'trans'])]
print("Relevant Tables in DB:", pay_tables)

if 'course_payments' in tables:
    cur.execute("SELECT DISTINCT status, COUNT(*) FROM course_payments GROUP BY status")
    print("course_payments status:", cur.fetchall())

if 'stipend_tasks' in tables:
    cur.execute("SELECT DISTINCT status, COUNT(*) FROM stipend_tasks GROUP BY status")
    print("stipend_tasks status:", cur.fetchall())

cur.close()
conn.close()
