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
        print(f"[DEPLOY-14-VERIFIED] {msg}")
    except UnicodeEncodeError:
        safe_msg = str(msg).encode("ascii", errors="replace").decode("ascii")
        print(f"[DEPLOY-14-VERIFIED] {safe_msg}")

log("=" * 80)
log("DEPLOYING 14 UPGRADED VERIFIED CERTIFICATES & REBUILDING STANDALONE NEXT.JS ON EC2")
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

# 1. Ensure remote directories
log("\n1. Ensuring remote directory structure...")
dirs_to_create = [
    f"{REMOTE_BASE}/apps/website/src/data",
    f"{REMOTE_BASE}/apps/website/public/certificates/previews",
    f"{REMOTE_BASE}/outputs/cohort_2026",
    f"{REMOTE_BASE}/data",
    f"{REMOTE_BASE}/scripts"
]
run_ssh(f"mkdir -p {' '.join(dirs_to_create)}")

# 2. Upload JSON Registries & Submissions
log("\n2. Uploading updated registries & payment submissions...")
run_scp(
    os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json"),
    f"{REMOTE_BASE}/apps/website/src/data/certificates_registry.json"
)
# Also sync to REMOTE_BASE/data/ for portal fallback
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
    os.path.join(BASE_DIR, "scripts", "sync_verified_certificates_to_portal.py"),
    f"{REMOTE_BASE}/scripts/sync_verified_certificates_to_portal.py"
)

# 3. Upload Certificate Preview PNGs
log("\n3. Uploading Certificate Preview PNGs for all 14 candidates...")
candidate_cids = [
    "CERT-DBERT-2026-DA-173",
    "CERT-DBERT-2026-DA-048",
    "CERT-DBERT-2026-FSD-156",
    "CERT-DBERT-2026-FSD-046",
    "CERT-DBERT-2026-DA-019",
    "CERT-DBERT-2026-AIML-002",
    "CERT-DBERT-2026-AIML-013",
    "CERT-DBERT-2026-DA-049",
    "CERT-DBERT-2026-DA-117",
    "CERT-DBERT-2026-AIML-020",
    "CERT-DBERT-2026-DA-186",
    "CERT-DBERT-2026-DA-067",
    "CERT-DBERT-2026-DA-109",
    "CERT-DBERT-2026-FSD-056"
]

for cid in candidate_cids:
    png_name = f"{cid}.png"
    local_p = os.path.join(BASE_DIR, "apps", "website", "public", "certificates", "previews", png_name)
    if os.path.exists(local_p):
        run_scp(local_p, f"{REMOTE_BASE}/apps/website/public/certificates/previews/{png_name}")
    else:
        log(f"Warning: local preview not found: {local_p}")

# 4. Upload Bhargavi Poola Cohort Dossier
log("\n4. Uploading 3-Doc PDF Dossier for Bhargavi Poola...")
local_bhargavi_dir = os.path.join(BASE_DIR, "outputs", "cohort_2026", "75_bhargavi_poola")
if os.path.exists(local_bhargavi_dir):
    run_scp(local_bhargavi_dir, f"{REMOTE_BASE}/outputs/cohort_2026/", is_dir=True)

# 5. Sync to Portal PostgreSQL Database
log("\n5. Syncing verified candidates to PostgreSQL dbert_lms.intern_certificates...")
sync_res = run_ssh(f"{REMOTE_BASE}/apps/portal/.venv/bin/python {REMOTE_BASE}/scripts/sync_verified_certificates_to_portal.py")
log(f"Sync output:\n{sync_res.stdout}")

# 6. Standalone Build & Asset Sync on EC2
log("\n6. Running Standalone Next.js Build on EC2...")
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

# 7. Live Probes & Verification
log("\n7. Probing live verification APIs on production domain...")
time.sleep(2)

probe_candidates = [
    ("CERT-DBERT-2026-DA-173", "Sakthi P"),
    ("CERT-DBERT-2026-DA-048", "Pulluri Bhargavi"),
    ("CERT-DBERT-2026-FSD-156", "Bhargavi Poola"),
    ("CERT-DBERT-2026-FSD-046", "Yasharth Poddar"),
    ("CERT-DBERT-2026-DA-019", "Radha Bhamodkar"),
    ("CERT-DBERT-2026-AIML-002", "Shanmukha Sri Saikumar Medisetty"),
    ("CERT-DBERT-2026-AIML-013", "Shanu Sri Gowtham"),
    ("CERT-DBERT-2026-DA-049", "Kolloju Meghana"),
    ("CERT-DBERT-2026-DA-117", "M Brahmani"),
    ("CERT-DBERT-2026-AIML-020", "Bhargavi C K"),
    ("CERT-DBERT-2026-DA-186", "Deepanshu"),
    ("CERT-DBERT-2026-DA-067", "Siva Sankar Thirumalasetty"),
    ("CERT-DBERT-2026-DA-109", "Satya Patil"),
    ("CERT-DBERT-2026-FSD-056", "Kundan Kumhar")
]

all_passed = True
for cert_id, name in probe_candidates:
    url = f"https://dbert.in/api/verify?certid={cert_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DBERT-Verification-Probe/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            is_v = data.get('verified')
            is_p = data.get('isProvisional')
            st = data.get('status')
            log(f"[{cert_id}] ({name}) -> HTTP {resp.status} | Verified: {is_v} | Status: {st} | Provisional: {is_p}")
            if not is_v or is_p:
                all_passed = False
    except Exception as e:
        log(f"[{cert_id}] Verification Probe Failed: {e}")
        all_passed = False

    # Check Preview Image
    img_url = f"https://dbert.in/certificates/previews/{cert_id}.png"
    try:
        req_img = urllib.request.Request(img_url, headers={"User-Agent": "DBERT-Verification-Probe/1.0"})
        with urllib.request.urlopen(req_img, timeout=10) as resp:
            log(f"  Preview Image [{img_url}] -> HTTP {resp.status} (Length: {resp.headers.get('Content-Length')} bytes)")
    except Exception as e:
        log(f"  Preview Image Failed: {e}")
        all_passed = False

log("\n" + "=" * 80)
if all_passed:
    log("ALL 14 CERTIFICATES SUCCESSFULLY APPROVED, SYNCED & VERIFIED ON PRODUCTION EC2!")
else:
    log("DEPLOYMENT COMPLETED WITH SOME WARNINGS - PLEASE INSPECT LOGS ABOVE.")
log("=" * 80)
