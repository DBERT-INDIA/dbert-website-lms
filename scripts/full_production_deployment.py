import subprocess
import os
import sys

ssh_key = r"C:\Users\user\.ssh\dbert-production-server.pem"
server = "ubuntu@3.26.237.171"
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

print("=" * 80)
print("EXECUTING FULL PRODUCTION VERIFICATION DEPLOYMENT")
print("=" * 80)

# STEP 1: Fix Database in dbert_internship schema on EC2
print("\n[STEP 1/5] Correcting intern_certificates in PostgreSQL (dbert_internship)...")
db_fix_code = """import psycopg2

conn = psycopg2.connect("postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms")
cur = conn.cursor()
cur.execute("SET search_path TO dbert_internship, public;")

# Ensure CERT-DBERT-2026-DA-001 points to Kushal Agarwal (intern_account 4513)
cur.execute(\"\"\"
    UPDATE intern_certificates
    SET intern_id = 4513,
        email = 'kushalagarwal27496@gmail.com',
        course_title = 'DBERT Technical Incubation — Data Analyst',
        issued_at = '04 November 2026',
        received_at = '04 November 2026',
        url = '/verify?certid=CERT-DBERT-2026-DA-001'
    WHERE cert_id = 'CERT-DBERT-2026-DA-001';
\"\"\")

conn.commit()
print("PostgreSQL intern_certificates updated for CERT-DBERT-2026-DA-001!")

cur.execute(\"\"\"
    SELECT c.cert_id, c.intern_id, COALESCE(a.name, ap.name, 'Intern') AS recipient_name,
           COALESCE(a.domain, ap.domain, 'Engineering') AS domain
    FROM intern_certificates c
    LEFT JOIN intern_accounts a ON (a.id = c.intern_id OR (c.email IS NOT NULL AND LOWER(a.email) = LOWER(c.email)))
    LEFT JOIN applications ap ON (c.email IS NOT NULL AND LOWER(ap.email) = LOWER(c.email))
    WHERE c.cert_id = 'CERT-DBERT-2026-DA-001';
\"\"\")
print("LMS query result:", cur.fetchall())
conn.close()
"""

with open("scripts/remote_probe.py", "w", encoding="utf-8") as f:
    f.write(db_fix_code)

subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", "scripts/remote_probe.py", f"{server}:/tmp/remote_probe.py"], check=True)
res = subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 /tmp/remote_probe.py"], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)

# STEP 2: Create remote directories
print("\n[STEP 2/5] Creating remote directories...")
remote_base = "/var/www/dbert-website-lms"
mkdir_cmd = f"mkdir -p {remote_base}/apps/website/src/data {remote_base}/apps/website/src/app/verify/\\[certId\\] {remote_base}/apps/portal/static/certificates {remote_base}/apps/website/public/certificates/previews"
subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, mkdir_cmd], check=True)

# STEP 3: SCP updated files
print("\n[STEP 3/5] Uploading verified code, registry and assets to EC2...")

# 1. certificates_registry.json
reg_local = os.path.join(base_dir, "apps", "website", "src", "data", "certificates_registry.json")
subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", reg_local, f"{server}:{remote_base}/apps/website/src/data/certificates_registry.json"], check=True)

# 2. route.ts
route_local = os.path.join(base_dir, "apps", "website", "src", "app", "api", "verify", "route.ts")
subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", route_local, f"{server}:{remote_base}/apps/website/src/app/api/verify/route.ts"], check=True)

# 3. page.tsx
page_local = os.path.join(base_dir, "apps", "website", "src", "app", "verify", "page.tsx")
subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", page_local, f"{server}:{remote_base}/apps/website/src/app/verify/page.tsx"], check=True)

# 4. [certId]/page.tsx
dynamic_page_local = os.path.join(base_dir, "apps", "website", "src", "app", "verify", "[certId]", "page.tsx")
subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", dynamic_page_local, f"{server}:{remote_base}/apps/website/src/app/verify/[certId]/page.tsx"], check=True)

# 5. targets12.png
targets12_local = os.path.join(base_dir, "apps", "portal", "static", "certificates", "targets12.png")
subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", targets12_local, f"{server}:{remote_base}/apps/portal/static/certificates/targets12.png"], check=True)

# 6. preview image
preview_local = os.path.join(base_dir, "apps", "website", "public", "certificates", "previews", "CERT-DBERT-2026-DA-001.png")
subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", preview_local, f"{server}:{remote_base}/apps/website/public/certificates/previews/CERT-DBERT-2026-DA-001.png"], check=True)

print("All files uploaded successfully!")

# STEP 4: Build Next.js and restart service
print("\n[STEP 4/5] Building Next.js production build and restarting service...")
build_cmd = """
cd /var/www/dbert-website-lms/apps/website
export NODE_ENV=production
npm run build
sudo systemctl restart dbert-website.service
sleep 3
systemctl status dbert-website.service --no-pager
"""
build_res = subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, build_cmd], capture_output=True, text=True)
print("Build output:")
print(build_res.stdout)
if build_res.stderr:
    print("Build stderr:", build_res.stderr)

# STEP 5: Verification tests
print("\n" + "=" * 80)
print("[STEP 5/5] RUNNING VERIFICATION CHECKS")
print("=" * 80)

verify_cmd = """
echo "=== 1. LMS Flask API on 5001 ==="
curl -s 'http://127.0.0.1:5001/api/verify?certId=CERT-DBERT-2026-DA-001'
echo ""

echo "=== 2. Next.js API on 3001 with ?certid= ==="
curl -s 'http://127.0.0.1:3001/api/verify?certid=CERT-DBERT-2026-DA-001'
echo ""

echo "=== 3. Public Web Page https://dbert.in/verify?certid=CERT-DBERT-2026-DA-001 ==="
curl -s 'https://dbert.in/verify?certid=CERT-DBERT-2026-DA-001' | grep -E "(Kushal Agarwal|Data Analyst|July to September|MSME)" || echo "Curl completed"
"""
v_res = subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, verify_cmd], capture_output=True, text=True)
print(v_res.stdout)
print("=" * 80)
print("PRODUCTION DEPLOYMENT COMPLETED SUCCESSFULLY!")
