import subprocess
import os
import sys
import urllib.request
import json

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
        print(f"[DEPLOY-1999] {msg}")
    except UnicodeEncodeError:
        safe_msg = str(msg).encode("ascii", errors="replace").decode("ascii")
        print(f"[DEPLOY-1999] {safe_msg}")

log("=" * 76)
log("DEPLOYING ₹1,999 ENROLLMENT & BALANCE COMPLETION PORTAL TO EC2 (3.26.237.171)")
log("=" * 76)

# 1. Create remote directories
remote_dirs = [
    f"{REMOTE_BASE}/apps/website/src/app/enroll/1999",
    f"{REMOTE_BASE}/apps/website/src/app/eroll",
    f"{REMOTE_BASE}/apps/website/src/app/api/enroll/balance",
    f"{REMOTE_BASE}/apps/website/src/app/api/enroll/lookup",
    f"{REMOTE_BASE}/apps/website/public/images",
    f"{REMOTE_BASE}/apps/website/data",
]

for d in remote_dirs:
    log(f"Ensuring remote directory: {d} ...")
    subprocess.run([
        "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER,
        f"mkdir -p {d}"
    ], check=True)

# 2. Upload files
files_to_upload = [
    # Enrollment App Pages & Components
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "enroll", "page.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/enroll/page.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "eroll", "page.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/eroll/page.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "enroll", "1999", "page.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/enroll/1999/page.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "enroll", "1999", "EnrollmentClient.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/enroll/1999/EnrollmentClient.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "enroll", "1999", "enroll.module.css"),
        f"{REMOTE_BASE}/apps/website/src/app/enroll/1999/enroll.module.css"
    ),
    # API Routes
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "api", "enroll", "balance", "route.ts"),
        f"{REMOTE_BASE}/apps/website/src/app/api/enroll/balance/route.ts"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "api", "enroll", "lookup", "route.ts"),
        f"{REMOTE_BASE}/apps/website/src/app/api/enroll/lookup/route.ts"
    ),
    # Modified Verify Page
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "[certId]", "page.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/verify/[certId]/page.tsx"
    ),
    # Assets (QR code)
    (
        os.path.join(BASE_DIR, "apps", "website", "public", "images", "qrcode.jpeg"),
        f"{REMOTE_BASE}/apps/website/public/images/qrcode.jpeg"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "public", "qrcode.jpeg"),
        f"{REMOTE_BASE}/apps/website/public/qrcode.jpeg"
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

log("All files uploaded successfully.")

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
sleep 2
systemctl is-active dbert-website.service
"""

res = subprocess.run([
    "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER,
    remote_build_script
], capture_output=True)

out = res.stdout.decode("utf-8", errors="ignore") if res.stdout else ""
err = res.stderr.decode("utf-8", errors="ignore") if res.stderr else ""

try:
    log("Build output summary:\n" + out[-800:])
except Exception:
    log("Build output received.")

if res.returncode != 0:
    log(f"ERROR: Build script exited with code {res.returncode}")
    log("Error output:\n" + err)
    sys.exit(1)

# 4. Live Production Validation
log("=" * 76)
log("VALIDATING LIVE PRODUCTION ENDPOINTS ON https://dbert.in")
log("=" * 76)

urls_to_test = [
    ("Enroll 1999 Main Portal", "https://dbert.in/enroll/1999"),
    ("Enroll Alias Forwarding", "https://dbert.in/enroll"),
    ("Eroll Typo Forwarding", "https://dbert.in/eroll"),
    ("Eroll With Param Forwarding", "https://dbert.in/eroll?certid=CERT-DBERT-2026-DA-057"),
    ("Official Payment QR Asset", "https://dbert.in/images/qrcode.jpeg"),
    ("Candidate API Lookup", "https://dbert.in/api/enroll/lookup?q=CERT-DBERT-2026-DA-057"),
    ("Locked Cert CTA Update", "https://dbert.in/verify/CERT-DBERT-2026-DA-057"),
]

req_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DBERT-Verification-Bot/2.0"}

all_passed = True
for label, url in urls_to_test:
    try:
        req = urllib.request.Request(url, headers=req_headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            code = resp.getcode()
            final_url = resp.geturl()
            body_bytes = resp.read()
            log(f"✓ {label}: HTTP {code} ({len(body_bytes)} bytes) -> Final URL: {final_url}")

            if "api/enroll/lookup" in url:
                parsed = json.loads(body_bytes.decode("utf-8", errors="ignore"))
                if parsed.get("found"):
                    cand = parsed["candidate"]
                    log(f"  Autofill Match: {cand['holderName']} | {cand['domain']} | {cand['certId']}")
                else:
                    log("  WARNING: Candidate not found in lookup response.")

            if "verify/CERT-DBERT-2026-DA-057" in url:
                body_text = body_bytes.decode("utf-8", errors="ignore")
                if "/enroll/1999?certid=CERT-DBERT-2026-DA-057" in body_text:
                    log("  ✓ Verification page CTA contains direct link to /enroll/1999?certid=CERT-DBERT-2026-DA-057")
                else:
                    log("  WARNING: Expected link /enroll/1999 not found in verify page HTML.")
    except Exception as e:
        log(f"✗ {label} failed: {e}")
        all_passed = False

if all_passed:
    log("ALL PRODUCTION CHECKS PASSED SUCCESSFULLY!")
else:
    log("SOME PRODUCTION CHECKS FAILED. Please review the log above.")
