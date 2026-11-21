#!/usr/bin/env python3
"""
Deploy Universal Responsive & Cross-Device UI/UX updates to production EC2.
Uploads modified portal templates, CSS, and website CSS modules, rebuilds Next.js standalone,
and restarts dbert-portal and dbert-website systemd services.
"""

import subprocess
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

PORTAL_FILES = [
    ("apps/portal/static/css/dbert-theme.css", f"{REMOTE_BASE}/apps/portal/static/css/dbert-theme.css"),
    ("apps/portal/templates/portal.html", f"{REMOTE_BASE}/apps/portal/templates/portal.html"),
    ("apps/portal/templates/ambassador.html", f"{REMOTE_BASE}/apps/portal/templates/ambassador.html"),
    ("apps/portal/templates/certificates.html", f"{REMOTE_BASE}/apps/portal/templates/certificates.html"),
    ("apps/portal/templates/task_guide.html", f"{REMOTE_BASE}/apps/portal/templates/task_guide.html"),
    ("apps/portal/templates/stipend_tasks.html", f"{REMOTE_BASE}/apps/portal/templates/stipend_tasks.html"),
    ("apps/portal/templates/account_notifications.html", f"{REMOTE_BASE}/apps/portal/templates/account_notifications.html"),
]

WEBSITE_FILES = [
    ("apps/website/src/components/layout/MegaMenu.module.css", f"{REMOTE_BASE}/apps/website/src/components/layout/MegaMenu.module.css"),
    ("apps/website/src/components/layout/WhatsAppFloat.module.css", f"{REMOTE_BASE}/apps/website/src/components/layout/WhatsAppFloat.module.css"),
    ("apps/website/src/components/ui/modal.module.css", f"{REMOTE_BASE}/apps/website/src/components/ui/modal.module.css"),
    ("apps/website/src/components/ui/CohortBanner.module.css", f"{REMOTE_BASE}/apps/website/src/components/ui/CohortBanner.module.css"),
    ("apps/website/src/components/ui/MultiStepForm.module.css", f"{REMOTE_BASE}/apps/website/src/components/ui/MultiStepForm.module.css"),
    ("apps/website/src/app/dbert-online/dbert-online.module.css", f"{REMOTE_BASE}/apps/website/src/app/dbert-online/dbert-online.module.css"),
    ("apps/website/src/app/about/about.module.css", f"{REMOTE_BASE}/apps/website/src/app/about/about.module.css"),
    ("apps/website/src/app/verify/directory/directory.module.css", f"{REMOTE_BASE}/apps/website/src/app/verify/directory/directory.module.css"),
    ("apps/website/src/app/verify/verify.module.css", f"{REMOTE_BASE}/apps/website/src/app/verify/verify.module.css"),
    ("apps/website/src/app/verify/unlock/unlock.module.css", f"{REMOTE_BASE}/apps/website/src/app/verify/unlock/unlock.module.css"),
]

def log(msg):
    print(f"[RESPONSIVE DEPLOY] {msg}", flush=True)

def run_ssh(cmd, timeout=300):
    full_cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        HOST,
        cmd
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
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

def main():
    log("=== Starting Universal Responsive UI/UX Deployment to Production EC2 ===")
    
    # 1. Upload Portal Files
    log("1/4 Uploading LMS Portal templates and CSS...")
    for local_f, remote_f in PORTAL_FILES:
        if not os.path.exists(local_f):
            log(f"ERROR: Local file not found: {local_f}")
            sys.exit(1)
        ok = scp_file(local_f, remote_f)
        if not ok:
            log(f"Failed to upload {local_f}")
            sys.exit(1)
        log(f"  ✓ Uploaded {local_f}")

    # 2. Upload Website Files
    log("2/4 Uploading Public Website CSS modules...")
    for local_f, remote_f in WEBSITE_FILES:
        if not os.path.exists(local_f):
            log(f"ERROR: Local file not found: {local_f}")
            sys.exit(1)
        ok = scp_file(local_f, remote_f)
        if not ok:
            log(f"Failed to upload {local_f}")
            sys.exit(1)
        log(f"  ✓ Uploaded {local_f}")

    # 3. Rebuild Website Standalone & Sync Assets
    log("3/4 Building Next.js Standalone on EC2...")
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
    echo "SERVICES STATUS:"
    systemctl is-active dbert-website.service
    systemctl is-active dbert-portal.service
    """
    res = run_ssh(build_cmd, timeout=360)
    log(f"Build & Restart Output:\n{res.stdout.strip()}")
    if res.returncode != 0:
        log(f"Build Error:\n{res.stderr.strip()}")
        sys.exit(1)

    log("4/4 Deployment completed successfully!")

if __name__ == "__main__":
    main()
