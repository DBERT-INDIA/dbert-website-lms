import psycopg2
import json

DB_URL = "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms"
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# 1. Check enrollments (499 payments)
cur.execute('''
    SELECT payment_status, count(*), sum(amount)
    FROM enrollments
    GROUP BY payment_status
''')
enroll_by_status = cur.fetchall()

cur.execute('''
    SELECT id, email, name, phone, amount, payment_status, utr, created_at, updated_at
    FROM enrollments
    WHERE payment_status = 'Accepted' OR payment_status ILIKE '%accept%' OR payment_status ILIKE '%approved%'
    ORDER BY created_at DESC
''')
accepted_499 = cur.fetchall()

# 2. Check 299 payments / verified certificates
cur.execute('''
    SELECT tier, count(*)
    FROM intern_certificates
    GROUP BY tier
''')
certs_by_tier = cur.fetchall()

cur.execute('''
    SELECT ic.id, ic.email, ic.cert_id, ic.tier, ic.issued_at, ia.name, ia.phone
    FROM intern_certificates ic
    LEFT JOIN intern_accounts ia ON LOWER(ic.email) = LOWER(ia.email)
    WHERE ic.tier IN ('verified', 'dbert_verified')
    ORDER BY ic.issued_at DESC NULLS LAST
''')
verified_299 = cur.fetchall()

# 3. Check stipend release details / task submissions
# Check tables related to stipend, tasks, ambassador payouts, withdrawals, upi_id
cur.execute('''
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' AND (
        table_name ILIKE '%stipend%' OR 
        table_name ILIKE '%task%' OR 
        table_name ILIKE '%payout%' OR 
        table_name ILIKE '%withdraw%' OR 
        table_name ILIKE '%wallet%' OR 
        table_name ILIKE '%coin%'
    )
''')
stipend_tables = cur.fetchall()

# Check intern accounts with upi_id configured
cur.execute('''
    SELECT id, email, name, phone, 
           CASE WHEN upi_id_encrypted IS NOT NULL AND upi_id_encrypted != '' THEN 1 ELSE 0 END as has_upi,
           linkedin_url, github_url
    FROM intern_accounts
    WHERE upi_id_encrypted IS NOT NULL AND upi_id_encrypted != ''
''')
upi_configured = cur.fetchall()

# Check task submissions if table exists
task_submissions = []
cur.execute("SELECT to_regclass('public.intern_tasks')")
has_intern_tasks = cur.fetchone()[0]

cur.execute("SELECT to_regclass('public.task_submissions')")
has_task_subs = cur.fetchone()[0]

cur.execute("SELECT to_regclass('public.stipend_submissions')")
has_stipend_subs = cur.fetchone()[0]

cur.execute("SELECT to_regclass('public.ambassador_payouts')")
has_ambassador_payouts = cur.fetchone()[0]

print("Tables found:", stipend_tables)
print("has_intern_tasks:", has_intern_tasks)
print("has_task_subs:", has_task_subs)
print("has_stipend_subs:", has_stipend_subs)
print("has_ambassador_payouts:", has_ambassador_payouts)

results = {
    "enroll_by_status": enroll_by_status,
    "accepted_499_count": len(accepted_499),
    "accepted_499_recent": [
        {"id": r[0], "email": r[1], "name": r[2], "phone": r[3], "amount": r[4], "status": r[5], "utr": r[6], "created_at": str(r[7]), "updated_at": str(r[8])}
        for r in accepted_499[:20]
    ],
    "certs_by_tier": certs_by_tier,
    "verified_299_count": len(verified_299),
    "verified_299_recent": [
        {"id": r[0], "email": r[1], "cert_id": r[2], "tier": r[3], "issued_at": str(r[4]), "name": r[5], "phone": r[6]}
        for r in verified_299[:20]
    ],
    "upi_configured_count": len(upi_configured),
    "upi_configured_recent": [
        {"id": r[0], "email": r[1], "name": r[2], "phone": r[3], "has_upi": r[4], "linkedin": r[5], "github": r[6]}
        for r in upi_configured[:20]
    ]
}

with open('/tmp/payments_and_stipend_report.json', 'w') as f:
    json.dump(results, f, indent=2)

print("Saved report to /tmp/payments_and_stipend_report.json successfully")
conn.close()
