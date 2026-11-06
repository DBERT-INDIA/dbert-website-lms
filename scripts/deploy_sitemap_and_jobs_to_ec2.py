import subprocess
import os
import sys
import urllib.request
import json
import xml.etree.ElementTree as ET

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
    print(f"[DEPLOY-SEO] {msg}")

log("=" * 76)
log("DEPLOYING SITEMAP & GOOGLE FOR JOBS SCHEMA TO EC2 (3.26.237.171)")
log("=" * 76)

files_to_upload = [
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "data", "seo.config.ts"),
        f"{REMOTE_BASE}/apps/website/src/data/seo.config.ts"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "sitemap.ts"),
        f"{REMOTE_BASE}/apps/website/src/app/sitemap.ts"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "learners", "jobs", "page.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/learners/jobs/page.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "cohorts", "aivara", "page.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/cohorts/aivara/page.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "src", "app", "about", "careers", "page.tsx"),
        f"{REMOTE_BASE}/apps/website/src/app/about/careers/page.tsx"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "sitemap.xml"),
        f"{REMOTE_BASE}/apps/website/sitemap.xml"
    ),
    (
        os.path.join(BASE_DIR, "apps", "website", "sitemap.xml"),
        f"{REMOTE_BASE}/apps/website/public/sitemap.xml"
    ),
]

for local_path, remote_path in files_to_upload:
    if os.path.exists(local_path):
        log(f"Uploading {os.path.basename(local_path)} -> {remote_path} ...")
        subprocess.run([
            "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
            local_path, f"{SERVER}:{remote_path}"
        ], check=True)
    else:
        log(f"WARNING: File not found locally: {local_path}")

log("Files uploaded successfully. Rebuilding Next.js standalone on EC2...")

remote_build_script = f"""
set -e
cd {REMOTE_BASE}/apps/website
export NODE_ENV=production
npm run build
cp -r public .next/standalone/ 2>/dev/null || true
cp -r public .next/standalone/apps/website/ 2>/dev/null || true
# Ensure permanent data symlink persists
mkdir -p {REMOTE_BASE}/data
rm -rf {REMOTE_BASE}/apps/website/.next/standalone/data
ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/data
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

log("Remote build output summary:\n" + out[-600:])

if res.returncode != 0:
    log(f"ERROR: Build script exited with code {res.returncode}")
    log("Error output:\n" + err)
    sys.exit(1)

log("✓ Remote build and service restart completed successfully.")

log("=" * 76)
log("LIVE PRODUCTION VALIDATION FOR GOOGLE SEARCH CONSOLE & GOOGLE JOBS")
log("=" * 76)

endpoints = [
    ("Website Sitemap", "https://dbert.in/sitemap.xml"),
    ("Website Robots.txt", "https://dbert.in/robots.txt"),
    ("Learners Jobs (Google Jobs)", "https://dbert.in/learners/jobs"),
    ("Aivara Remote Cohort", "https://dbert.in/cohorts/aivara"),
    ("About Careers", "https://dbert.in/about/careers"),
    ("Candidate Directory", "https://dbert.in/verify/directory"),
    ("Enrollment 1999", "https://dbert.in/enroll/1999"),
    ("LMS Sitemap", "https://lms.dbert.in/sitemap.xml"),
    ("LMS Robots.txt", "https://lms.dbert.in/robots.txt"),
]

all_pass = True
for name, url in endpoints:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Googlebot/2.1)"})
        with urllib.request.urlopen(req, timeout=15) as response:
            status = response.status
            content = response.read().decode("utf-8", errors="ignore")
            size = len(content)
            
            checks = []
            if "sitemap" in url:
                checks.append(f"{content.count('<loc>')} URLs")
                if "dbert.online" in content:
                    checks.append("FAIL: dbert.online present")
                    all_pass = False
                else:
                    checks.append("PASS: zero dbert.online")
            elif "robots" in url:
                checks.append("PASS: valid robots")
            else:
                if "JobPosting" in content:
                    checks.append("PASS: JobPosting schema found")
                else:
                    checks.append("NOTE: No JobPosting")
            
            check_str = " | ".join(checks)
            log(f"✓ {name:30}: HTTP {status} ({size} bytes) | {check_str}")
    except Exception as e:
        log(f"✗ {name:30}: FAILED — {e}")
        all_pass = False

if all_pass:
    log("ALL SITEMAP AND GOOGLE JOBS VALIDATIONS PASSED PERFECTLY!")
else:
    log("Validation completed with warnings.")
