#!/usr/bin/env python3
"""
scripts/deploy_monorepo_master_to_ec2.py
Comprehensive Production Deployment for DBERT Monorepo:
1. Deploys updated portal code, services, templates, and static assets.
2. Deletes obsolete templates/routes on EC2.
3. Restarts dbert-portal.service.
4. Packages and uploads apps/website/src and public assets.
5. Runs remote standalone Next.js compilation (npm run build).
6. Syncs sitemaps and enforces permanent data symlink.
7. Restarts dbert-website.service.
8. Runs comprehensive live smoke tests on dbert.in and lms.dbert.in.
"""

import os
import sys
import time
import tarfile
import tempfile
import subprocess
import urllib.request
import ssl

sys.stdout.reconfigure(encoding="utf-8")

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"
REMOTE_PORTAL_DIR = f"{REMOTE_BASE}/apps/portal"
REMOTE_WEBSITE_DIR = f"{REMOTE_BASE}/apps/website"

PORTAL_FILES = [
    # Core Application & Services
    ("apps/portal/app.py", f"{REMOTE_PORTAL_DIR}/app.py"),
    ("apps/portal/services/grading_service.py", f"{REMOTE_PORTAL_DIR}/services/grading_service.py"),
    ("apps/portal/services/certificate_packet_service.py", f"{REMOTE_PORTAL_DIR}/services/certificate_packet_service.py"),
    ("apps/portal/services/ai/stipend_evaluator.py", f"{REMOTE_PORTAL_DIR}/services/ai/stipend_evaluator.py"),
    ("apps/portal/services/ai/gemini_discovery.py", f"{REMOTE_PORTAL_DIR}/services/ai/gemini_discovery.py"),
    # Templates
    ("apps/portal/templates/company_signup.html", f"{REMOTE_PORTAL_DIR}/templates/company_signup.html"),
    ("apps/portal/templates/account_gemini_key.html", f"{REMOTE_PORTAL_DIR}/templates/account_gemini_key.html"),
    ("apps/portal/templates/portal.html", f"{REMOTE_PORTAL_DIR}/templates/portal.html"),
    ("apps/portal/templates/portal_offer_letter.html", f"{REMOTE_PORTAL_DIR}/templates/portal_offer_letter.html"),
    ("apps/portal/templates/portal_offer_print.html", f"{REMOTE_PORTAL_DIR}/templates/portal_offer_print.html"),
    ("apps/portal/templates/tasks_list.html", f"{REMOTE_PORTAL_DIR}/templates/tasks_list.html"),
    ("apps/portal/templates/stipend_tasks.html", f"{REMOTE_PORTAL_DIR}/templates/stipend_tasks.html"),
    ("apps/portal/templates/staff_dashboard.html", f"{REMOTE_PORTAL_DIR}/templates/staff_dashboard.html"),
    ("apps/portal/templates/staff_project_queue.html", f"{REMOTE_PORTAL_DIR}/templates/staff_project_queue.html"),
    ("apps/portal/templates/staff_task_queue.html", f"{REMOTE_PORTAL_DIR}/templates/staff_task_queue.html"),
    ("apps/portal/templates/dev_qa_matrix.html", f"{REMOTE_PORTAL_DIR}/templates/dev_qa_matrix.html"),
    # Static Assets & Documentation
    ("apps/portal/static/css/dbert-theme.css", f"{REMOTE_PORTAL_DIR}/static/css/dbert-theme.css"),
    ("MASTER.md", f"{REMOTE_BASE}/MASTER.md"),
]

def log(msg):
    print(f"[DEPLOY] {msg}", flush=True)

def run_ssh(cmd, timeout=300):
    full_cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        HOST,
        cmd
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    if res.returncode != 0:
        log(f"SSH Command Failed (code {res.returncode}):\n{res.stderr.strip()}")
    return res

def scp_file(local_path, remote_path):
    full_cmd = [
        "scp", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        local_path,
        f"{HOST}:{remote_path}"
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        log(f"SCP ERROR ({local_path} -> {remote_path}): {res.stderr.strip()}")
        return False
    return True

def create_website_tarball():
    tar_path = os.path.join(tempfile.gettempdir(), "website_master_payload.tar.gz")
    log(f"Creating local website tarball at {tar_path}...")
    with tarfile.open(tar_path, "w:gz") as tar:
        # Add apps/website/src
        src_dir = os.path.join("apps", "website", "src")
        tar.add(src_dir, arcname="src")
        
        # Add public previews if present
        previews_dir = os.path.join("apps", "website", "public", "certificates", "previews")
        if os.path.exists(previews_dir):
            tar.add(previews_dir, arcname="public/certificates/previews")
            
        images_dir = os.path.join("apps", "website", "public", "images")
        if os.path.exists(images_dir):
            tar.add(images_dir, arcname="public/images")
            
    size_mb = os.path.getsize(tar_path) / (1024 * 1024)
    log(f"Website tarball created: {size_mb:.2f} MB")
    return tar_path

def main():
    log("=" * 80)
    log("DBERT PRODUCTION MASTER DEPLOYMENT TO EC2 (3.26.237.171)")
    log("=" * 80)

    # 1. Pre-flight SSH check
    res = run_ssh("echo CONNECTED && uptime")
    if res.returncode != 0 or "CONNECTED" not in res.stdout:
        log("Failed to connect to EC2! Aborting.")
        sys.exit(1)
    log(f"EC2 Node Active: {res.stdout.strip()}")

    # 2. Deploy Portal Files
    log("\n--- STEP 1: Deploying Portal Files & Services ---")
    for local_path, remote_path in PORTAL_FILES:
        if os.path.exists(local_path):
            log(f"Uploading {local_path} -> {remote_path}")
            if not scp_file(local_path, remote_path):
                log(f"Failed to upload {local_path}! Aborting.")
                sys.exit(1)
        else:
            log(f"Warning: {local_path} not found locally, skipping.")

    # 3. Clean dead files on EC2 & restart Portal service
    log("\n--- STEP 2: Cleaning Dead Files & Restarting Portal Service ---")
    cleanup_cmd = f"""
    set -e
    # Remove dead routes and templates
    rm -f {REMOTE_PORTAL_DIR}/routes/masterclass.py
    rm -f {REMOTE_PORTAL_DIR}/templates/masterclass_data_analyst.html
    rm -f {REMOTE_PORTAL_DIR}/templates/certificate_dossier.html
    rm -f {REMOTE_PORTAL_DIR}/templates/sample_certificate.html
    rm -f {REMOTE_PORTAL_DIR}/templates/portal_ledger.html
    rm -f {REMOTE_PORTAL_DIR}/.htaccess.cgi {REMOTE_PORTAL_DIR}/passenger_wsgi.py {REMOTE_PORTAL_DIR}/php.ini {REMOTE_PORTAL_DIR}/test.php 2>/dev/null || true

    # Restart dbert-portal.service
    sudo systemctl restart dbert-portal.service
    sleep 2
    sudo systemctl is-active dbert-portal.service
    """
    res = run_ssh(cleanup_cmd)
    if res.returncode != 0:
        log(f"Portal service restart failed! Check EC2 logs.")
        sys.exit(1)
    log("Portal service is active and running!")

    # 4. Deploy Website Files
    log("\n--- STEP 3: Packaging & Uploading Website Source ---")
    tar_path = create_website_tarball()
    remote_tar = "/tmp/website_master_payload.tar.gz"
    if not scp_file(tar_path, remote_tar):
        log("Failed to upload website tarball!")
        sys.exit(1)

    # 5. Remote Next.js Standalone Build
    log("\n--- STEP 4: Executing Remote Standalone Build on EC2 ---")
    build_cmd = f"""
    set -e
    cd {REMOTE_WEBSITE_DIR}
    tar -xzf {remote_tar}
    rm -f {remote_tar}

    export NODE_ENV=production
    npm run build

    echo "[EC2] Syncing public assets to standalone..."
    cp -r public .next/standalone/ 2>/dev/null || true
    cp -r public .next/standalone/apps/website/ 2>/dev/null || true

    if [ -f .next/server/app/sitemap.xml.body ]; then
        echo "[EC2] Syncing generated sitemap.xml..."
        cp .next/server/app/sitemap.xml.body public/sitemap.xml
        cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml 2>/dev/null || true
        cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true
    fi

    echo "[EC2] Enforcing permanent data symlink..."
    mkdir -p {REMOTE_BASE}/data
    rm -rf {REMOTE_WEBSITE_DIR}/.next/standalone/data
    ln -s {REMOTE_BASE}/data {REMOTE_WEBSITE_DIR}/.next/standalone/data
    rm -rf {REMOTE_WEBSITE_DIR}/.next/standalone/apps/website/data 2>/dev/null || true
    ln -s {REMOTE_BASE}/data {REMOTE_WEBSITE_DIR}/.next/standalone/apps/website/data 2>/dev/null || true

    echo "[EC2] Restarting dbert-website.service..."
    sudo systemctl restart dbert-website.service
    sleep 3
    sudo systemctl is-active dbert-website.service
    """
    res = run_ssh(build_cmd, timeout=400)
    if res.returncode != 0:
        log("Remote build or dbert-website restart failed!")
        sys.exit(1)
    log("Website build succeeded and service restarted successfully!")

    try:
        os.remove(tar_path)
    except Exception:
        pass

    # 6. Live Production Health Checks
    log("\n--- STEP 5: Live Smoke Tests ---")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    test_urls = [
        ("Website Public Landing", "https://dbert.in"),
        ("Pre-Vetted Directory", "https://dbert.in/verify/directory"),
        ("Incubation Enrollment 1999", "https://dbert.in/enroll/1999"),
        ("Candidate Profile Dossier", "https://dbert.in/verify/CERT-DBERT-2026-AIML-902"),
        ("Portal LMS Root", "https://lms.dbert.in"),
        ("Portal PDF Credential Stream", "https://lms.dbert.in/portal/certificate/CERT-DBERT-2026-AIML-902/pdf"),
    ]

    all_ok = True
    for label, url in test_urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "DBERT-Deploy-SmokeTest/1.0"})
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                status = resp.status
                content_len = len(resp.read())
                log(f"[PASS] {label}: HTTP {status} ({content_len} bytes)")
        except urllib.error.HTTPError as e:
            # 302/401 may be expected for protected endpoints without auth
            if e.code in (200, 302, 401):
                log(f"[PASS (Guarded)] {label}: HTTP {e.code}")
            else:
                log(f"[FAIL] {label}: HTTP {e.code}")
                all_ok = False
        except Exception as e:
            log(f"[FAIL] {label}: {e}")
            all_ok = False

    if all_ok:
        log("\n" + "=" * 80)
        log("SUCCESS: ALL PRODUCTION SERVICES DEPLOYED & VERIFIED ON EC2!")
        log("=" * 80)
    else:
        log("\n" + "=" * 80)
        log("WARNING: SOME ENDPOINTS RETURNED NON-200 STATUS. REVIEW OUTPUT ABOVE.")
        log("=" * 80)

if __name__ == "__main__":
    main()
