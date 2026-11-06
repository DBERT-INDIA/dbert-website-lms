import subprocess
import json
import os
import sys

ssh_key = r"C:\Users\user\.ssh\dbert-production-server.pem"
server = "ubuntu@3.26.237.171"
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

print("=" * 80)
print("DEPLOYING VERIFICATION ENGINE TO PRODUCTION EC2 (3.26.237.171)")
print("=" * 80)

# 1. Read certificates_registry.json
reg_path = os.path.join(base_dir, "apps", "website", "src", "data", "certificates_registry.json")
with open(reg_path, "r", encoding="utf-8") as f:
    registry = json.load(f)

print(f"Loaded {len(registry)} certificates from registry.")

# 2. Generate Database Seeding Script for EC2
seed_script = """import psycopg2
import json

with open('/tmp/certificates_registry.json', 'r', encoding='utf-8') as f:
    registry = json.load(f)

conn = psycopg2.connect("postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms")
cur = conn.cursor()

inserted_apps = 0
inserted_certs = 0
updated_certs = 0

for cert_id, rec in registry.items():
    holder_name = rec["holderName"]
    email = rec["email"]
    domain = rec["domain"]
    college = rec.get("college") or "Institution of Technology"
    phone = rec.get("phone") or "9999999999"
    course_title = f"DBERT Technical Incubation — {domain}"
    issued_at = rec.get("evalDate", "04 November 2026")
    url = f"/verify?certid={cert_id}"
    
    # Check if cert already exists
    cur.execute("SELECT id, intern_id FROM intern_certificates WHERE cert_id = %s;", (cert_id,))
    row = cur.fetchone()
    
    if row:
        intern_app_id = row[1]
        cur.execute(\"\"\"
            UPDATE intern_certificates 
            SET course_title = %s, url = %s, email = %s, issued_at = %s, received_at = %s
            WHERE cert_id = %s;
        \"\"\", (course_title, url, email, issued_at, issued_at, cert_id))
        updated_certs += 1
    else:
        # Check if application exists by email
        cur.execute("SELECT id FROM applications WHERE email = %s LIMIT 1;", (email,))
        app_row = cur.fetchone()
        if app_row:
            intern_app_id = app_row[0]
        else:
            cur.execute(\"\"\"
                INSERT INTO applications (name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status)
                VALUES (%s, %s, %s, 'India', %s, 'Computer Science / Engineering', '8th Semester', '2026', %s, 'Incubation & Credential Verification', 'Verified')
                RETURNING id;
            \"\"\", (holder_name, email, phone, college, domain))
            intern_app_id = cur.fetchone()[0]
            inserted_apps += 1
            
        cur.execute(\"\"\"
            INSERT INTO intern_certificates (intern_id, course_id, course_title, cert_id, issued_at, url, received_at, tier, email)
            VALUES (%s, 1, %s, %s, %s, %s, %s, 'dbert_verified', %s);
        \"\"\", (intern_app_id, course_title, cert_id, issued_at, url, issued_at, email))
        inserted_certs += 1

conn.commit()
conn.close()

print(f"DATABASE SEEDING RESULT: {inserted_certs} certs inserted, {updated_certs} certs updated, {inserted_apps} applications created.")
"""

with open("scripts/seed_remote_pg.py", "w", encoding="utf-8") as f:
    f.write(seed_script)

# 3. SCP registry and seeding script to EC2
print("\n[STEP 1/4] Uploading registry and database seed script to EC2...")
subprocess.run([
    "scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    reg_path, f"{server}:/tmp/certificates_registry.json"
], check=True)

subprocess.run([
    "scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    "scripts/seed_remote_pg.py", f"{server}:/tmp/seed_remote_pg.py"
], check=True)

# Run seed script on EC2
print("\n[STEP 2/4] Executing database seed on PostgreSQL (dbert_lms)...")
res = subprocess.run([
    "ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    server, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 /tmp/seed_remote_pg.py"
], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)

# 4. Upload updated Next.js files to EC2
print("\n[STEP 3/4] Uploading Next.js verification route, registry and pages to EC2...")
remote_base = "/var/www/dbert-website-lms"

# Ensure all remote target directories exist
subprocess.run([
    "ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    server, f"mkdir -p {remote_base}/apps/website/src/data {remote_base}/apps/website/src/app/verify/\\[certId\\] {remote_base}/apps/portal/static/certificates {remote_base}/apps/website/public/certificates/previews"
], check=True)

# Upload registry to website data dir
subprocess.run([
    "scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    reg_path, f"{server}:{remote_base}/apps/website/src/data/certificates_registry.json"
], check=True)

# Upload api verify route
subprocess.run([
    "scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    os.path.join(base_dir, "apps", "website", "src", "app", "api", "verify", "route.ts"),
    f"{server}:{remote_base}/apps/website/src/app/api/verify/route.ts"
], check=True)

# Upload verify page.tsx
subprocess.run([
    "scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    os.path.join(base_dir, "apps", "website", "src", "app", "verify", "page.tsx"),
    f"{server}:{remote_base}/apps/website/src/app/verify/page.tsx"
], check=True)

# Upload verify/[certId]/page.tsx
subprocess.run([
    "scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    os.path.join(base_dir, "apps", "website", "src", "app", "verify", "[certId]", "page.tsx"),
    f"{server}:{remote_base}/apps/website/src/app/verify/[certId]/page.tsx"
], check=True)

# Upload patched targets12.png
subprocess.run([
    "scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    os.path.join(base_dir, "apps", "portal", "static", "certificates", "targets12.png"),
    f"{server}:{remote_base}/apps/portal/static/certificates/targets12.png"
], check=True)

# Upload sample certificate preview
subprocess.run([
    "scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    os.path.join(base_dir, "apps", "website", "public", "certificates", "previews", "CERT-DBERT-2026-DA-001.png"),
    f"{server}:{remote_base}/apps/website/public/certificates/previews/CERT-DBERT-2026-DA-001.png"
], check=True)

print("All files uploaded successfully!")

# 5. Build Next.js and restart service
print("\n[STEP 4/4] Building Next.js application on EC2 and restarting service...")
build_cmd = """
cd /var/www/dbert-website-lms/apps/website
export NODE_ENV=production
npm run build
sudo systemctl restart dbert-website.service
sleep 2
systemctl status dbert-website.service --no-pager
"""
build_res = subprocess.run([
    "ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    server, build_cmd
], capture_output=True, text=True)
print("Build output:")
print(build_res.stdout)
if build_res.stderr:
    print("Build stderr:", build_res.stderr)

# 6. Verify live curl
print("\n" + "=" * 80)
print("VERIFYING LIVE PRODUCTION ENDPOINTS")
print("=" * 80)

verify_cmd = """
echo "1. Testing LMS /api/verify:"
curl -s 'http://127.0.0.1:5001/api/verify?certId=CERT-DBERT-2026-DA-001'
echo ""

echo "2. Testing Next.js /api/verify with ?certid= (lowercase):"
curl -s 'http://127.0.0.1:3001/api/verify?certid=CERT-DBERT-2026-DA-001'
echo ""

echo "3. Testing Next.js /api/verify with ?certId=:"
curl -s 'http://127.0.0.1:3001/api/verify?certId=CERT-DBERT-2026-DA-001'
echo ""

echo "4. Testing Public Website Verification Page:"
curl -s -I 'https://dbert.in/verify?certid=CERT-DBERT-2026-DA-001' | head -n 5
"""
verify_res = subprocess.run([
    "ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no",
    server, verify_cmd
], capture_output=True, text=True)
print(verify_res.stdout)
print("=" * 80)
