import psycopg2
import json

DB_URL = "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms"
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Get all active interns with GitHub or LinkedIn submitted who do NOT have verified certificates
cur.execute('''
    SELECT ia.id, ia.email, ia.name, ia.phone, ia.domain, ia.college, ia.linkedin_url, ia.github_url, ia.updated_at,
           (SELECT count(*) FROM intern_certificates c WHERE LOWER(c.email) = LOWER(ia.email) AND c.tier IN ('verified', 'dbert_verified')) as is_verified
    FROM intern_accounts ia
    WHERE ia.is_active = 1
    ORDER BY ia.updated_at DESC NULLS LAST
''')
all_active = cur.fetchall()

unverified_gate_active = [
    {
        "id": a[0], "email": a[1], "name": a[2], "phone": a[3], "domain": a[4], "college": a[5],
        "linkedin_url": a[6], "github_url": a[7], "updated_at": str(a[8]),
        "conversion_target": "₹299 Verification & Executive Dossier (Gate 3 to Unlock ₹5,000 Stipend)",
        "priority_tier": 3,
        "priority_label": "Fellowship Milestone Active (Sprint Unlocking - ₹299)"
    }
    for a in all_active if a[9] == 0 and (a[6] or a[7])
]

print(f"Total Active LMS Accounts: {len(all_active)}")
print(f"Unverified Gate Active Fellows (₹299 pool): {len(unverified_gate_active)}")

with open('/tmp/unverified_gate_active.json', 'w') as f:
    json.dump(unverified_gate_active, f, indent=2)

conn.close()
