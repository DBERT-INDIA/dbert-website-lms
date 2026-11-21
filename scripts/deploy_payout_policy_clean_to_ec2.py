#!/usr/bin/env python3
"""
Deploy internal payout policy updates to production EC2:
- apps/portal/templates/stipend_tasks.html
- apps/website/src/data/qa_knowledge_base.json
- AGENTS.md, GEMINI.md, ARCHITECTURE_ROADMAP.md
Rebuilds Next.js on EC2 and restarts dbert-portal and dbert-website services.
"""

import subprocess
import os
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

FILES_TO_UPLOAD = [
    ("apps/portal/templates/stipend_tasks.html", f"{REMOTE_BASE}/apps/portal/templates/stipend_tasks.html"),
    ("apps/website/src/data/qa_knowledge_base.json", f"{REMOTE_BASE}/apps/website/src/data/qa_knowledge_base.json"),
    ("AGENTS.md", f"{REMOTE_BASE}/AGENTS.md"),
    ("GEMINI.md", f"{REMOTE_BASE}/GEMINI.md"),
    ("ARCHITECTURE_ROADMAP.md", f"{REMOTE_BASE}/ARCHITECTURE_ROADMAP.md"),
]

def log(msg):
    print(f"[DEPLOY-POLICY] {msg}", flush=True)

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
    log("Uploading updated templates, knowledge base, and docs to EC2...")
    for local_file, remote_file in FILES_TO_UPLOAD:
        if not os.path.exists(local_file):
            log(f"ERROR: Local file does not exist: {local_file}")
            return 1
        success = scp_file(local_file, remote_file)
        if not success:
            log(f"Failed to upload {local_file}")
            return 1
        log(f"Uploaded: {os.path.basename(local_file)} -> {remote_file}")

    log("Rebuilding Next.js standalone on EC2 and restarting services...")
    remote_script = f"""
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
    
    sudo systemctl restart dbert-portal.service
    sudo systemctl restart dbert-website.service
    sleep 2
    systemctl is-active dbert-portal.service
    systemctl is-active dbert-website.service
    """
    
    res = run_ssh(remote_script, timeout=600)
    print(res.stdout)
    if res.returncode != 0:
        log(f"Build/Restart failed with code {res.returncode}: {res.stderr}")
        return 1

    log("Deployment completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
