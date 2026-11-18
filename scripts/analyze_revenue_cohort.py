import psycopg2
import json

DB_URL = "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms"
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# 1. Total enrollments breakdown by payment_status
cur.execute('''
    SELECT payment_status, count(*) 
    FROM enrollments 
    GROUP BY payment_status
''')
enroll_stats = cur.fetchall()
print("Enrollments by payment_status:", enroll_stats)

# 2. Details of rejected/flagged/pending enrollments
cur.execute('''
    SELECT e.id, e.email, e.name, e.phone, e.payment_status, e.utr, e.amount, e.created_at, ia.updated_at, ia.linkedin_url, ia.github_url
    FROM enrollments e
    LEFT JOIN intern_accounts ia ON LOWER(e.email) = LOWER(ia.email)
    WHERE e.payment_status IN ('rejected', 'flagged', 'pending') OR e.payment_status IS NULL
    ORDER BY e.created_at DESC
''')
pending_rejected = cur.fetchall()
print(f"Pending/Rejected Enrollments: {len(pending_rejected)}")

# 3. Selected applications without successful enrollment
cur.execute('''
    SELECT a.id, a.email, a.name, a.phone, a.status, a.domain, a.created_at, ia.updated_at,
           (SELECT count(*) FROM enrollments e WHERE LOWER(e.email) = LOWER(a.email) AND e.payment_status = 'approved') as approved_enrolls,
           (SELECT count(*) FROM enrollments e WHERE LOWER(e.email) = LOWER(a.email) AND e.payment_status IN ('rejected', 'flagged', 'pending')) as pending_enrolls
    FROM applications a
    LEFT JOIN intern_accounts ia ON LOWER(a.email) = LOWER(ia.email)
    WHERE a.status = 'selected'
    ORDER BY ia.updated_at DESC NULLS LAST
''')
selected_apps = cur.fetchall()
print(f"Selected apps: {len(selected_apps)}")

# 4. Provisional Certificates (Eligible for ₹299 verification)
cur.execute('''
    SELECT ic.id, ic.email, ic.cert_id, ic.tier, ic.issued_at, ia.name, ia.phone, ia.linkedin_url, ia.github_url, ia.updated_at
    FROM intern_certificates ic
    LEFT JOIN intern_accounts ia ON LOWER(ic.email) = LOWER(ia.email)
    WHERE ic.tier NOT IN ('verified', 'dbert_verified') OR ic.tier IS NULL
    ORDER BY ic.issued_at DESC NULLS LAST
''')
provisional_certs = cur.fetchall()
print(f"Provisional certs in intern_certificates: {len(provisional_certs)}")

# 5. Check active intern accounts that are working on gates (potential ₹299 verification converters)
cur.execute('''
    SELECT ia.id, ia.email, ia.name, ia.phone, ia.updated_at,
           (CASE WHEN ia.linkedin_url IS NOT NULL AND ia.linkedin_url != '' THEN 1 ELSE 0 END) as has_linkedin,
           (CASE WHEN ia.github_url IS NOT NULL AND ia.github_url != '' THEN 1 ELSE 0 END) as has_github,
           (SELECT count(*) FROM intern_articles art WHERE art.intern_id = ia.id) as art_count,
           (SELECT count(*) FROM intern_certificates c WHERE LOWER(c.email) = LOWER(ia.email) AND c.tier IN ('verified', 'dbert_verified')) as is_verified
    FROM intern_accounts ia
    WHERE ia.is_active = 1
    ORDER BY ia.updated_at DESC NULLS LAST
''')
active_interns = cur.fetchall()
print(f"Active interns: {len(active_interns)}")

data = {
    "enroll_stats": enroll_stats,
    "pending_rejected": [
        {"id": r[0], "email": r[1], "name": r[2], "phone": r[3], "payment_status": r[4], "utr": r[5], "amount": r[6], "created_at": str(r[7]), "ia_updated": str(r[8]), "linkedin": r[9], "github": r[10]}
        for r in pending_rejected
    ],
    "selected_apps": [
        {"id": r[0], "email": r[1], "name": r[2], "phone": r[3], "status": r[4], "domain": r[5], "created_at": str(r[6]), "ia_updated": str(r[7]), "approved_enrolls": r[8], "pending_enrolls": r[9]}
        for r in selected_apps
    ],
    "provisional_certs": [
        {"id": r[0], "email": r[1], "cert_id": r[2], "tier": r[3], "issued_at": str(r[4]), "name": r[5], "phone": r[6], "linkedin": r[7], "github": r[8], "ia_updated": str(r[9])}
        for r in provisional_certs
    ],
    "active_interns": [
        {"id": r[0], "email": r[1], "name": r[2], "phone": r[3], "updated_at": str(r[4]), "linkedin": r[5], "github": r[6], "art_count": r[7], "is_verified": r[8]}
        for r in active_interns
    ]
}

with open('/tmp/revenue_cohort_analysis.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Saved cleanly to /tmp/revenue_cohort_analysis.json")
conn.close()
