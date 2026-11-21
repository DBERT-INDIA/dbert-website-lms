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

def log(msg):
    print(f"[DEPLOY-2-VERIFIED] {msg}", flush=True)

log("=" * 80)
log("DEPLOYING 2 UPGRADED VERIFIED CERTIFICATES & UNLOCKING STIPEND GATE 1 ON EC2")
log("=" * 80)

def run_ssh(cmd, check=True):
    full_cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, cmd]
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0 and check:
        log(f"SSH Command failed: {cmd}\nStdout: {res.stdout}\nStderr: {res.stderr}")
        raise RuntimeError(f"SSH command failed with returncode {res.returncode}")
    return res

def run_scp(local_path, remote_path, is_dir=False):
    scp_cmd = ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no"]
    if is_dir:
        scp_cmd.append("-r")
    scp_cmd.extend([local_path, f"{SERVER}:{remote_path}"])
    res = subprocess.run(scp_cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        log(f"SCP failed for {local_path} -> {remote_path}\nStderr: {res.stderr}")
        raise RuntimeError(f"SCP command failed with returncode {res.returncode}")
    log(f"Uploaded: {os.path.basename(local_path)} -> {remote_path}")

# 1. Upload JSON Registries & Submissions
log("\n1. Uploading updated registries & payment submissions...")
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
    os.path.join(BASE_DIR, "data", "verification_submissions_299.json"),
    f"{REMOTE_BASE}/data/verification_submissions_299.json"
)
run_scp(
    os.path.join(BASE_DIR, "data", "verification_submissions_299.json"),
    f"{REMOTE_BASE}/apps/website/data/verification_submissions_299.json"
)

# 2. Upload Preview PNGs
log("\n2. Uploading certificate preview PNGs...")
run_scp(
    os.path.join(BASE_DIR, "apps", "website", "public", "certificates", "previews", "CERT-DBERT-2026-FSD-341.png"),
    f"{REMOTE_BASE}/apps/website/public/certificates/previews/CERT-DBERT-2026-FSD-341.png"
)
run_scp(
    os.path.join(BASE_DIR, "apps", "website", "public", "certificates", "previews", "CERT-DBERT-2026-FSD-342.png"),
    f"{REMOTE_BASE}/apps/website/public/certificates/previews/CERT-DBERT-2026-FSD-342.png"
)

# 3. Upload 3-Doc Dossiers
log("\n3. Uploading 3-doc dossiers to outputs/cohort_2026/...")
run_ssh(f"mkdir -p {REMOTE_BASE}/outputs/cohort_2026/91_molugu_nanda_yaso_vardhan")
run_scp(
    os.path.join(BASE_DIR, "outputs", "cohort_2026", "91_molugu_nanda_yaso_vardhan"),
    f"{REMOTE_BASE}/outputs/cohort_2026/",
    is_dir=True
)

run_ssh(f"mkdir -p {REMOTE_BASE}/outputs/cohort_2026/92_h_a_uday_bhasker")
run_scp(
    os.path.join(BASE_DIR, "outputs", "cohort_2026", "92_h_a_uday_bhasker"),
    f"{REMOTE_BASE}/outputs/cohort_2026/",
    is_dir=True
)

# 4. PostgreSQL Update for intern_certificates and intern_accounts
log("\n4. Updating EC2 PostgreSQL database (intern_certificates & intern_accounts)...")
pg_update_script = r"""
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    print('Updating intern_certificates...')
    certs_to_sync = [
        ('CERT-DBERT-2026-FSD-341', 5067, 'Full Stack Web Development', '2026-11-21', 'nandayasovardhan@gmail.com'),
        ('CERT-DBERT-2026-FSD-342', 2089, 'Full Stack Web Development', '2026-11-21', 'ubhoysala@gmail.com')
    ]
    
    for cid, intern_id, domain, issued_at, email in certs_to_sync:
        cur = conn.execute("SELECT id FROM intern_certificates WHERE cert_id = ?;", (cid,))
        row = cur.fetchone()
        if row:
            conn.execute("UPDATE intern_certificates SET tier = 'verified', email = ?, course_title = ? WHERE cert_id = ?;", (email, f"DBERT Technical Incubation — {domain}", cid))
            print(f"  Updated existing cert [{cid}] to tier='verified'")
        else:
            conn.execute(
                "INSERT INTO intern_certificates (intern_id, course_id, course_title, cert_id, issued_at, url, tier, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                (intern_id, 1, f"DBERT Technical Incubation — {domain}", cid, issued_at, f"https://dbert.in/verify?certid={cid}", "verified", email)
            )
            print(f"  Inserted new cert [{cid}] with tier='verified'")

    print('\nUnlocking Stipend Gate 1 (stipend_verified = 1) for both candidates...')
    target_emails = [
        'nandayasovardhan@gmail.com',
        'ubhoysala@gmail.com'
    ]
    for em in target_emails:
        cur = conn.execute("UPDATE intern_accounts SET stipend_verified = 1 WHERE LOWER(email) = ? RETURNING id, name, email, stipend_verified;", (em.lower(),))
        r = cur.fetchone()
        if r:
            print(f"  Account [{em}]: ID={r[0]}, Name={r[1]}, stipend_verified={r[3]}")
        else:
            print(f"  Account [{em}] not found in intern_accounts!")

    if hasattr(conn, 'commit'):
        conn.commit()
        print('Committed all database updates successfully!')
"""

res = subprocess.run(
    ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, f"{REMOTE_BASE}/apps/portal/.venv/bin/python3"],
    input=pg_update_script,
    text=True,
    capture_output=True,
    encoding="utf-8"
)
log(f"Database update output:\n{res.stdout}")
if res.stderr:
    log(f"Database update stderr:\n{res.stderr}")

# 5. Rebuild Next.js Standalone
log("\n5. Rebuilding Standalone Next.js Website on EC2...")
build_cmd = """
cd /var/www/dbert-website-lms/apps/website
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
mkdir -p /var/www/dbert-website-lms/data
rm -rf /var/www/dbert-website-lms/apps/website/.next/standalone/data
ln -s /var/www/dbert-website-lms/data /var/www/dbert-website-lms/apps/website/.next/standalone/data
sudo systemctl restart dbert-website.service
sudo systemctl restart dbert-portal.service
sleep 2
systemctl is-active dbert-website.service
systemctl is-active dbert-portal.service
"""
res = run_ssh(build_cmd)
log(f"Build and service restart output:\n{res.stdout}")

# 6. HTTP Verification
log("\n6. Running live HTTP endpoint verifications...")
time.sleep(3)

test_urls = [
    "https://dbert.in/verify/CERT-DBERT-2026-FSD-341",
    "https://dbert.in/verify/CERT-DBERT-2026-FSD-342",
    "https://dbert.in/certificates/previews/CERT-DBERT-2026-FSD-341.png",
    "https://dbert.in/certificates/previews/CERT-DBERT-2026-FSD-342.png",
    "https://dbert.in/verify/directory"
]

all_passed = True
for url in test_urls:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DBERT-Verification-Bot/1.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            code = resp.getcode()
            log(f"  [HTTP {code}] {url} -> OK")
    except Exception as e:
        log(f"  [FAILED] {url} -> {e}")
        all_passed = False

if all_passed:
    log("\n" + "=" * 80)
    log("ALL 2 VERIFIED CREDENTIALS DEPLOYED & TESTED SUCCESSFULLY ON PRODUCTION!")
    log("=" * 80)
else:
    log("\nWarning: Some verification endpoints encountered issues. Please check.")
