#!/usr/bin/env python3
"""
deploy_mobile_fixes_to_ec2.py
Deploys updated portal responsive CSS and templates to EC2:
- apps/portal/static/css/dbert-theme.css
- apps/portal/templates/portal.html
- apps/portal/templates/_head.html
Restarts dbert-portal.service and verifies HTTP 200.
"""

import subprocess
import sys
import time

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"

FILES = [
    ("apps/portal/static/css/dbert-theme.css", f"{REMOTE_PORTAL_DIR}/static/css/dbert-theme.css"),
    ("apps/portal/templates/portal.html", f"{REMOTE_PORTAL_DIR}/templates/portal.html"),
    ("apps/portal/templates/_head.html", f"{REMOTE_PORTAL_DIR}/templates/_head.html"),
]

def run_cmd(cmd, check=True):
    print(f"[RUN] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        print(f"[STDERR] {res.stderr.strip()}", file=sys.stderr)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with code {res.returncode}")
    return res

def main():
    print("=== DEPLOYING RESPONSIVE MOBILE FIXES TO EC2 ===")
    for local_file, remote_file in FILES:
        print(f"[SCP] Uploading {local_file} -> {remote_file}...")
        scp_cmd = f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes "{local_file}" {HOST}:{remote_file}'
        run_cmd(scp_cmd)

    print("[SSH] Restarting dbert-portal.service on EC2...")
    restart_cmd = (
        f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {HOST} '
        '"sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"'
    )
    res = run_cmd(restart_cmd)
    print(f"[STATUS] Portal service is: {res.stdout.strip()}")
    print("=== DEPLOYMENT COMPLETE ===")

if __name__ == "__main__":
    main()
