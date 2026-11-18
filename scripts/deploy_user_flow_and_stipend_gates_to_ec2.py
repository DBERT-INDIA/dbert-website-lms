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
        print(f"[DEPLOY-GATES] {msg}")
    except UnicodeEncodeError:
        safe_msg = str(msg).encode("ascii", errors="replace").decode("ascii")
        print(f"[DEPLOY-GATES] {safe_msg}")

log("=" * 76)
log("DEPLOYING USER FLOW & STIPEND GATES UPDATES TO EC2 (3.26.237.171)")
log("=" * 76)

# 1. Ensure remote directories exist
remote_dirs = [
    f"{REMOTE_BASE}/apps/website/src/components/analytics",
    f"{REMOTE_BASE}/apps/portal/templates",
]

for d in remote_dirs:
    log(f"Ensuring remote directory: {d} ...")
    subprocess.run([
        "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", SERVER,
        f"mkdir -p {d}"
    ], check=True)

# 2. Upload files
files_to_upload = [
    # Flask LMS Backend & Templates
    (
        os.path.join(BASE_DIR, "apps", "portal", "app.py"),
        f"{REMOTE_BASE}/apps/portal/app.py"
    ),
    (
        os.path.join(BASE_DIR, "apps", "portal", "templates", "portal_offer_letter.html"),
        f"{REMOTE_BASE}/apps/portal/templates/portal_offer_letter.html"
    ),
    (
        os.path.join(BASE_DIR, "apps", "portal", "templates", "portal.html"),
        f"{REMOTE_BASE}/apps/portal/templates/portal.html"
    ),
    (
        os.path.join(BASE_DIR, "apps", "portal", "templates", "stipend_tasks.html"),
        f"{REMOTE_BASE}/apps/portal/templates/stipend_tasks.html"
    ),
    # Next.js Cross-Domain Attendance Heartbeat
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "components", "analytics", "AttendanceHeartbeat.tsx"),
        f"{REMOTE_BASE}/apps/website/src/components/analytics/AttendanceHeartbeat.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "layout.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/layout.tsx"
    ),
]

for local_path, remote_path in files_to_upload:
    log(f"Uploading {os.path.basename(local_path)} -> {remote_path} ...")
    subprocess.run([
        "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
        local_path, f"{SERVER}:{remote_path}"
    ], check=True)

log("All files uploaded successfully.")

# 3. Remote build and restart services
remote_cmd = f"""
set -e
echo "Restarting dbert-portal.service..."
sudo systemctl restart dbert-portal.service
sleep 2
systemctl is-active dbert-portal.service

echo "Rebuilding Next.js Standalone in apps/website..."
cd {REMOTE_BASE}/apps/website
export NODE_ENV=production
npm run build
cp -r public .next/standalone/ 2>/dev/null || true
cp -r public .next/standalone/apps/website/ 2>/dev/null || true

mkdir -p {REMOTE_BASE}/data
rm -rf {REMOTE_BASE}/apps/website/.next/standalone/data
ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/data

echo "Restarting dbert-website.service..."
sudo systemctl restart dbert-website.service
sleep 2
systemctl is-active dbert-website.service
"""

log("Executing remote build and service restarts...")
subprocess.run([
    "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", SERVER,
    remote_cmd
], check=True)

log("Remote services restarted successfully.")

# 4. Live probes
log("Running live verification probes...")
ctx = urllib.request.ssl._create_unverified_context()

try:
    req = urllib.request.Request("https://dbert.in", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        log(f"dbert.in -> HTTP {resp.status} (OK)")
except Exception as e:
    log(f"dbert.in probe error: {e}")

try:
    req = urllib.request.Request("https://lms.dbert.in/portal/offer", headers={"User-Agent": "Mozilla/5.0"})
    # Expect 302 to #signin
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
    with opener.open(req) as resp:
        log(f"lms.dbert.in/portal/offer -> HTTP {resp.status} (Final URL: {resp.url})")
except urllib.error.HTTPError as e:
    log(f"lms.dbert.in/portal/offer -> HTTP {e.code}")
except Exception as e:
    log(f"lms.dbert.in/portal/offer probe error: {e}")

log("=" * 76)
log("MISSION ACCOMPLISHED: EC2 PRODUCTION DEPLOYMENT & VERIFICATION COMPLETE")
log("=" * 76)
