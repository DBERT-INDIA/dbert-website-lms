#!/usr/bin/env python3
"""
scripts/deploy_acceptance_dossier_email_to_ec2.py
Deploys apps/portal/app.py to EC2 and restarts dbert-portal.service.
"""

import os
import sys
import subprocess

REMOTE_HOST = "ubuntu@3.26.237.171"
SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"

def run_cmd(cmd, check=True):
    print(f"[RUN] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print(f"[STDERR] {res.stderr.strip()}", file=sys.stderr)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with code {res.returncode}")
    return res

def main():
    print("=== DEPLOYING ENROLLMENT ACCEPTANCE DOSSIER EMAIL TO EC2 ===")
    
    # 1. SCP app.py
    local_app_py = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "apps", "portal", "app.py")
    if not os.path.exists(local_app_py):
        raise FileNotFoundError(f"Missing {local_app_py}")
    
    scp_cmd = f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no "{local_app_py}" {REMOTE_HOST}:{REMOTE_PORTAL_DIR}/app.py'
    run_cmd(scp_cmd)
    
    # 2. Remote syntax check & restart service
    remote_cmds = (
        f"cd {REMOTE_PORTAL_DIR} && "
        "/var/www/dbert-website-lms/apps/portal/.venv/bin/python -m py_compile app.py && "
        "sudo systemctl restart dbert-portal.service && "
        "sleep 2 && "
        "systemctl is-active dbert-portal.service"
    )
    ssh_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no {REMOTE_HOST} "{remote_cmds}"'
    res = run_cmd(ssh_cmd)
    
    if "active" in res.stdout:
        print("\n[SUCCESS] dbert-portal.service is ACTIVE and restarted successfully!")
    else:
        print("\n[ERROR] Service status check did not return 'active'!")
        sys.exit(1)

if __name__ == "__main__":
    main()
