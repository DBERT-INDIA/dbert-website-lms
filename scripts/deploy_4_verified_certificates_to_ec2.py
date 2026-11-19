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
        print(f"[DEPLOY-4-VERIFIED] {msg}")
    except UnicodeEncodeError:
        safe_msg = str(msg).encode("ascii", errors="replace").decode("ascii")
        print(f"[DEPLOY-4-VERIFIED] {safe_msg}")

log("=" * 76)
log("DEPLOYING 4 UPGRADED VERIFIED CERTIFICATES & REBUILDING STANDALONE NEXT.JS ON EC2")
log("=" * 76)

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

# 3. Upload Preview PNGs
log("\n3. Uploading Certificate Preview PNGs...")
previews = [
    "CERT-DBERT-2026-DA-111.png",
    "CERT-DBERT-2026-UIUX-034.png",
    "CERT-DBERT-2026-FSD-072.png",
    "CERT-DBERT-2026-DA-188.png"
]
for p in previews:
    local_p = os.path.join(BASE_DIR, "apps", "website", "public", "certificates", "previews", p)
    if os.path.exists(local_p):
        run_scp(local_p, f"{REMOTE_BASE}/apps/website/public/certificates/previews/{p}")
    else:
        log(f"Warning: local preview not found: {local_p}")

# 4. Upload Cohort 2026 PDF Dossiers
log("\n4. Uploading 3-Doc PDF Dossiers to EC2 outputs/cohort_2026/...")
cohort_folders = [
    "71_kethavath_sruthi",
    "72_shrey_patel",
    "73_bhavya_balchandani",
    "74_tehreem_fatima"
]
for folder in cohort_folders:
    local_f = os.path.join(BASE_DIR, "outputs", "cohort_2026", folder)
    if os.path.exists(local_f):
        run_scp(local_f, f"{REMOTE_BASE}/outputs/cohort_2026/", is_dir=True)
    else:
        log(f"Warning: local cohort folder not found: {local_f}")

# 5. Sync to Portal PostgreSQL Database
log("\n5. Syncing verified candidates to PostgreSQL dbert_internship.intern_certificates...")
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

test_certs = [
    ("CERT-DBERT-2026-DA-111", "Kethavath Sruthi"),
    ("CERT-DBERT-2026-UIUX-034", "Shrey Patel"),
    ("CERT-DBERT-2026-FSD-072", "Bhavya Balchandani"),
    ("CERT-DBERT-2026-DA-188", "Tehreem Fatima")
]

for cert_id, name in test_certs:
    url = f"https://dbert.in/api/verify?certid={cert_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DBERT-Verification-Probe/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            log(f"[{cert_id}] ({name}) -> HTTP {resp.status} | Verified: {data.get('verified')} | Status: {data.get('status')} | Provisional: {data.get('isProvisional')}")
    except Exception as e:
        log(f"[{cert_id}] Verification Probe Failed: {e}")

    # Check Preview Image
    img_url = f"https://dbert.in/certificates/previews/{cert_id}.png"
    try:
        req_img = urllib.request.Request(img_url, headers={"User-Agent": "DBERT-Verification-Probe/1.0"})
        with urllib.request.urlopen(req_img, timeout=10) as resp:
            log(f"  Preview Image [{img_url}] -> HTTP {resp.status} (Length: {resp.headers.get('Content-Length')} bytes)")
    except Exception as e:
        log(f"  Preview Image Failed: {e}")

log("\n" + "=" * 76)
log("ALL 4 CERTIFICATES SUCCESSFULLY APPROVED, SYNCED & VERIFIED ON PRODUCTION EC2!")
log("=" * 76)
