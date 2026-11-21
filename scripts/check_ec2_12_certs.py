import json
import psycopg2

subs = json.load(open('/var/www/dbert-website-lms/data/verification_submissions_299.json'))[4:]

DB_URL = "postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms"
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

print(f"Checking {len(subs)} candidates in PostgreSQL dbert_lms:")
print("=" * 90)
print(f"{'#':<3} | {'Cert ID':<24} | {'Email':<32} | {'DB Tier':<15} | {'Intern ID'}")
print("-" * 90)

for idx, s in enumerate(subs, 1):
    cid = s.get('certId')
    email = (s.get('email') or '').strip().lower()
    
    cur.execute("SELECT id, cert_id, tier, intern_id FROM intern_certificates WHERE LOWER(cert_id) = %s OR LOWER(email) = %s", (cid.lower(), email))
    rows = cur.fetchall()
    
    if rows:
        for r in rows:
            print(f"{idx:<3} | {cid:<24} | {email[:30]:<32} | {r[2]:<15} | {r[3]}")
    else:
        # Check intern_accounts
        cur.execute("SELECT id FROM intern_accounts WHERE LOWER(email) = %s", (email,))
        acct = cur.fetchone()
        intern_id = acct[0] if acct else "NO ACCOUNT"
        print(f"{idx:<3} | {cid:<24} | {email[:30]:<32} | {'NOT IN CERTS':<15} | {intern_id}")

cur.close()
conn.close()
