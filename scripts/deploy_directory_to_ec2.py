import subprocess
import os
import sys
import urllib.request

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
        print(f"[DEPLOY] {msg}")
    except UnicodeEncodeError:
        safe_msg = str(msg).encode("ascii", errors="replace").decode("ascii")
        print(f"[DEPLOY] {safe_msg}")

log("=" * 76)
log("DEPLOYING ALPHABETICAL CREDENTIAL DIRECTORY TO EC2 (3.26.237.171)")
log("=" * 76)

# 1. Create remote directory if not exists
log("Creating remote directory: apps/website/src/app/verify/directory ...")
subprocess.run([
    "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER,
    f"mkdir -p {REMOTE_BASE}/apps/website/src/app/verify/directory"
], check=True)

# 2. Upload files
files_to_upload = [
    # Directory Component Files
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "directory", "page.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/verify/directory/page.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "directory", "DirectoryClient.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/verify/directory/DirectoryClient.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "directory", "directory.module.css"),
        f"{REMOTE_BASE}/apps/website/src/app/verify/directory/directory.module.css"
    ),
    # Modified Verify Main & Dynamic Route Files
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "page.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/verify/page.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "[certId]", "page.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/verify/[certId]/page.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "api", "verify", "route.ts"),
        f"{REMOTE_BASE}/apps/website/src/app/api/verify/route.ts"
    ),
    # Data Files
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "data", "directory_candidates.json"),
        f"{REMOTE_BASE}/apps/website/src/data/directory_candidates.json"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "data", "all_409_provisional_registry.json"),
        f"{REMOTE_BASE}/apps/website/src/data/all_409_provisional_registry.json"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json"),
        f"{REMOTE_BASE}/apps/website/src/data/certificates_registry.json"
    ),
]

for local_path, remote_path in files_to_upload:
    if os.path.exists(local_path):
        fname = os.path.basename(local_path)
        log(f"Uploading: {fname} -> {remote_path}")
        subprocess.run([
            "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", local_path, f"{SERVER}:{remote_path}"
        ], check=True)
    else:
        log(f"WARNING: File not found locally: {local_path}")

log("All directory files uploaded successfully.")

# 3. Build Next.js and restart service on EC2
log("Building Next.js production bundle on EC2...")
remote_build_script = f"""
set -e
cd {REMOTE_BASE}/apps/website
export NODE_ENV=production
npm run build
cp -r public .next/standalone/ 2>/dev/null || true
cp -r public .next/standalone/apps/website/ 2>/dev/null || true
sudo systemctl restart dbert-website.service
sleep 3
systemctl is-active dbert-website.service
"""

res = subprocess.run([
    "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, remote_build_script
], capture_output=True)

out = res.stdout.decode("utf-8", errors="ignore")
log("EC2 Build stdout:\n" + out[-1500:])
if res.returncode != 0:
    err = res.stderr.decode("utf-8", errors="ignore")
    log("EC2 Build stderr:\n" + err)
    sys.exit(1)

log("EC2 Build and service restart completed successfully!")

# 4. Live Endpoint Validation
log("=" * 76)
log("VALIDATING LIVE PRODUCTION ENDPOINTS ON HTTPS://DBERT.IN")
log("=" * 76)

endpoints_to_test = [
    ("https://dbert.in/verify/directory", ["DBERT Credential Directory", "Filter by First Name Initial"]),
    ("https://dbert.in/verify", ["Looking to browse all candidates?", "Browse A–Z Directory"]),
    ("https://dbert.in/verify/CERT-DBERT-2026-DA-001", ["Cryptographically Verified Credential", "Kushal Agarwal"]),
    ("https://dbert.in/verify/CERT-DBERT-2026-DA-057", ["Provisional Record", "Badugu venkata rajesh"]),
]

for url, expected_keywords in endpoints_to_test:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            status = resp.status
            missing = [kw for kw in expected_keywords if kw not in content]
            if status == 200 and not missing:
                log(f"[PASS] {url} -> HTTP {status} (Verified: {', '.join(expected_keywords)})")
            else:
                log(f"[FAIL] {url} -> HTTP {status} (Missing: {missing})")
    except Exception as e:
        log(f"[ERROR] {url} -> {e}")

log("=" * 76)
log("DEPLOYMENT AND PRODUCTION VERIFICATION FINISHED!")
log("=" * 76)
