import psycopg2
import json

DB_URL = "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms"
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

print("--- Applications in 'Enrollment Pending' ---")
cur.execute("""
    SELECT a.id, a.name, a.email, a.phone, a.domain, a.status, a.created_at,
           e.id as enr_id, e.payment_status, e.payment_screenshot, e.utr, e.amount
    FROM applications a
    LEFT JOIN enrollments e ON LOWER(e.email) = LOWER(a.email)
    WHERE a.status = 'Enrollment Pending'
""")
cols = [desc[0] for desc in cur.description]
rows = [dict(zip(cols, r)) for r in cur.fetchall()]
print(f"Total Enrollment Pending: {len(rows)}")
for r in rows[:10]:
    print(r)

print("\n--- Enrollments with payment_screenshot ---")
cur.execute("""
    SELECT payment_status, COUNT(*) 
    FROM enrollments 
    WHERE payment_screenshot IS NOT NULL AND payment_screenshot != ''
    GROUP BY payment_status
""")
print(cur.fetchall())

print("\n--- Enrollments with UTR ---")
cur.execute("""
    SELECT payment_status, COUNT(*) 
    FROM enrollments 
    WHERE utr IS NOT NULL AND utr != ''
    GROUP BY payment_status
""")
print(cur.fetchall())

cur.close()
conn.close()
