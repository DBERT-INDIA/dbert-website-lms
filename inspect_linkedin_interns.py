import os, sys
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

db_url = "postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms"
conn = psycopg2.connect(db_url)
cur = conn.cursor(cursor_factory=RealDictCursor)

print("--- 1. Interns with linkedin_url in intern_accounts ---")
cur.execute("""
    SELECT id, name, email, phone, domain, college,
           linkedin_url, linkedin_verified, linkedin_verification_status,
           upi_id_encrypted, stipend_verified, stipend_amount, created_at
    FROM intern_accounts
    WHERE linkedin_url IS NOT NULL AND TRIM(linkedin_url) != ''
    ORDER BY id ASC
""")
rows = cur.fetchall()
print(f"Total interns with non-empty linkedin_url: {len(rows)}")
for r in rows:
    has_upi = bool(r['upi_id_encrypted'])
    print(f"ID: {r['id']} | Name: {r['name']} | Email: {r['email']} | LinkedIn: {r['linkedin_url']} | Has UPI: {has_upi} | Status: {r['linkedin_verification_status']}")

print("\n--- 2. Also check if cvs or applications have linkedin ---")
cur.execute("""
    SELECT DISTINCT email, linkedin_url FROM (
        SELECT email, linkedin_url FROM intern_accounts WHERE linkedin_url IS NOT NULL AND TRIM(linkedin_url) != ''
        UNION
        SELECT email, linkedin FROM cvs WHERE linkedin IS NOT NULL AND TRIM(linkedin) != ''
    ) t
""")
cv_rows = cur.fetchall()
print(f"Total distinct emails with linkedin in accounts or cvs: {len(cv_rows)}")

conn.close()
