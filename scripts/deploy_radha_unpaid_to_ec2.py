import subprocess
import os
import sys
import json
import urllib.request
import time

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
SERVER = "ubuntu@3.26.237.171"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REMOTE_BASE = "/var/www/dbert-website-lms"

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def log(msg):
    try:
        print(f"[DEPLOY-RADHA-UNPAID] {msg}")
    except UnicodeEncodeError:
        safe_msg = str(msg).encode("ascii", errors="replace").decode("ascii")
        print(f"[DEPLOY-RADHA-UNPAID] {safe_msg}")

log("=" * 80)
log("DEMOTING RADHA BHAMODKAR TO UNPAID / PROVISIONAL & REBUILDING ON EC2")
log("=" * 80)

def run_ssh(cmd, check=True):
    full_cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, cmd]
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0 and check:
        log(f"SSH Command failed: {cmd}\nStdout: {res.stdout}\nStderr: {res.stderr}")
        raise RuntimeError(f"SSH command failed with returncode {res.returncode}")
    return res

def run_scp(local_path, remote_path):
    scp_cmd = ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", local_path, f"{SERVER}:{remote_path}"]
    res = subprocess.run(scp_cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        log(f"SCP failed for {local_path} -> {remote_path}\nStderr: {res.stderr}")
        raise RuntimeError(f"SCP command failed with returncode {res.returncode}")
    log(f"Uploaded: {os.path.basename(local_path)} -> {remote_path}")

# 1. Upload files
log("\n1. Uploading updated data files and code...")
run_scp(
    os.path.join(BASE_DIR, "data", "verification_submissions_299.json"),
    f"{REMOTE_BASE}/data/verification_submissions_299.json"
)
run_scp(
    os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json"),
    f"{REMOTE_BASE}/apps/website/src/data/certificates_registry.json"
)
run_scp(
    os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json"),
    f"{REMOTE_BASE}/data/certificates_registry.json"
)
run_scp(
    os.path.join(BASE_DIR, "apps", "website", "src", "data", "directory_candidates.json"),
    f"{REMOTE_BASE}/apps/website/src/data/directory_candidates.json"
)
run_scp(
    os.path.join(BASE_DIR, "apps", "website", "src", "app", "api", "enroll", "lookup", "route.ts"),
    f"{REMOTE_BASE}/apps/website/src/app/api/enroll/lookup/route.ts"
)
run_scp(
    os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "unlock", "UnlockClient.tsx"),
    f"{REMOTE_BASE}/apps/website/src/app/verify/unlock/UnlockClient.tsx"
)

# 2. Update PostgreSQL Database on EC2
log("\n2. Updating EC2 PostgreSQL database (dbert_lms)...")
sql_commands = """
sudo -u postgres psql -d dbert_lms << 'EOF'
UPDATE dbert_internship.intern_certificates 
SET tier = 'provisional' 
WHERE cert_id = 'CERT-DBERT-2026-DA-019';

UPDATE dbert_internship.intern_accounts 
SET stipend_verified = 0 
WHERE email = 'radhabhamodkar@gmail.com' OR id = 4979;

INSERT INTO dbert_internship.notifications (
    intern_id, title, message, type, is_read, created_at
) VALUES (
    4979,
    'Action Required: ₹299 Project Verification Repayment Required',
    'Your previously submitted UTR (956584485560) for the ₹299 verification fee could not be reconciled in the bank audit. Your official credentials and Gate 1 stipend release are currently paused. Please visit https://dbert.in/verify/unlock?certid=CERT-DBERT-2026-DA-019 to complete repayment and submit your updated UTR.',
    'alert',
    false,
    NOW()
);

SELECT id, cert_id, tier, email FROM dbert_internship.intern_certificates WHERE cert_id = 'CERT-DBERT-2026-DA-019';
SELECT id, name, email, stipend_verified FROM dbert_internship.intern_accounts WHERE id = 4979;
EOF
"""
db_res = run_ssh(sql_commands)
log(f"PostgreSQL output:\n{db_res.stdout}")

# 3. Next.js Standalone Build & Asset Sync
log("\n3. Rebuilding Next.js Standalone on EC2...")
remote_build_script = f"""
set -e
cd {REMOTE_BASE}/apps/website
export NODE_ENV=production
npm run build

if [ -f .next/server/app/sitemap.xml.body ]; then
    cp .next/server/app/sitemap.xml.body public/sitemap.xml
fi

cp -r public .next/standalone/ 2>/dev/null || true
cp -r public .next/standalone/apps/website/ 2>/dev/null || true

if [ -f .next/server/app/sitemap.xml.body ]; then
    cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml 2>/dev/null || true
    cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true
fi

mkdir -p {REMOTE_BASE}/data
rm -rf {REMOTE_BASE}/apps/website/.next/standalone/data
ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/data

sudo systemctl restart dbert-website.service
sudo systemctl restart dbert-portal.service
sleep 3

echo "=== Systemd Status ==="
systemctl is-active dbert-website.service
systemctl is-active dbert-portal.service
"""
build_res = run_ssh(remote_build_script)
log(f"Build output:\n{build_res.stdout}")

# 4. Verification Probes
log("\n4. Probing live production endpoints...")
time.sleep(2)

# Probe /api/verify
v_url = "https://dbert.in/api/verify?certid=CERT-DBERT-2026-DA-019"
req = urllib.request.Request(v_url, headers={"User-Agent": "DBERT-Probe/1.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    log(f"Verify API: Verified={data.get('verified')} | Provisional={data.get('isProvisional')} | Status={data.get('status')}")

# Probe /api/enroll/lookup
l_url = "https://dbert.in/api/enroll/lookup?certid=CERT-DBERT-2026-DA-019"
req_l = urllib.request.Request(l_url, headers={"User-Agent": "DBERT-Probe/1.0"})
with urllib.request.urlopen(req_l, timeout=10) as resp:
    data_l = json.loads(resp.read().decode("utf-8"))
    log(f"Lookup API: found={data_l.get('found')} | verStatus={data_l.get('verificationStatus')} | remarks={data_l.get('rejectionRemarks')}")

log("\n" + "=" * 80)
log("RADHA BHAMODKAR SUCCESSFULLY DEMOTED TO UNPAID ON PRODUCTION EC2!")
log("=" * 80)
