import psycopg2
import json

DB_URL = "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms"
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

cur.execute("""
    SELECT e.id, e.name, e.email, e.phone, e.domain, e.product, e.amount, e.payment_status, e.utr, 
           e.payment_screenshot, e.created_at, e.admin_note, a.status as app_status
    FROM enrollments e
    LEFT JOIN applications a ON LOWER(a.email) = LOWER(e.email)
    WHERE e.payment_status = 'Pending Verification' 
       OR (e.payment_screenshot IS NOT NULL AND e.payment_screenshot != '')
       OR (e.utr IS NOT NULL AND e.utr != '')
    ORDER BY e.created_at DESC
""")
cols = [desc[0] for desc in cur.description]
rows = [dict(zip(cols, r)) for r in cur.fetchall()]
print(f"Total matching enrollments: {len(rows)}")
for r in rows[:10]:
    print(r)

cur.close()
conn.close()
