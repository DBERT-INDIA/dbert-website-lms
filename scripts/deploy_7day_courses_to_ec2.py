"""
DBERT LMS - Production Deployment Script for 7-Day Courses across All 9 Domains
================================================================================
Transfers updated app.py, courses_7day_catalog.py, executes database seeding
on PostgreSQL, restarts dbert-portal.service, and verifies live health.
================================================================================
"""

import subprocess
import sys
import time

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"
REMOTE_SCRIPTS_DIR = "/var/www/dbert-website-lms/scripts"
REMOTE_VENV_PYTHON = "/var/www/dbert-website-lms/apps/portal/.venv/bin/python"


def run_ssh(cmd, check=True):
    full_cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        HOST,
        cmd
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"[ERROR] Remote SSH failed: {res.stderr}")
        sys.exit(1)
    return res


def run_scp(local_path, remote_path):
    full_cmd = [
        "scp", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        local_path,
        f"{HOST}:{remote_path}"
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] SCP failed for {local_path} -> {remote_path}: {res.stderr}")
        sys.exit(1)
    print(f"[+] Transferred: {local_path} -> {remote_path}")


def main():
    print("=== Step 1: Ensure Remote Directories Exist ===")
    run_ssh(f"mkdir -p {REMOTE_PORTAL_DIR}/config {REMOTE_SCRIPTS_DIR}")

    print("\n=== Step 2: Upload Files to Production EC2 ===")
    run_scp("apps/portal/config/courses_7day_catalog.py", f"{REMOTE_PORTAL_DIR}/config/courses_7day_catalog.py")
    run_scp("apps/portal/app.py", f"{REMOTE_PORTAL_DIR}/app.py")
    run_scp("scripts/seed_all_9_domains_7day_courses.py", f"{REMOTE_SCRIPTS_DIR}/seed_all_9_domains_7day_courses.py")

    print("\n=== Step 3: Execute 7-Day Courses Seeding on Production PostgreSQL ===")
    seed_cmd = f"cd /var/www/dbert-website-lms && {REMOTE_VENV_PYTHON} scripts/seed_all_9_domains_7day_courses.py"
    seed_res = run_ssh(seed_cmd)
    print(seed_res.stdout)

    print("\n=== Step 4: Restart dbert-portal.service on EC2 ===")
    run_ssh("sudo systemctl restart dbert-portal.service")
    time.sleep(3)

    status_res = run_ssh("systemctl is-active dbert-portal.service")
    is_active = status_res.stdout.strip()
    print(f"Service status: {is_active}")
    assert is_active == "active", f"dbert-portal.service is {is_active}, expected 'active'"

    print("\n=== Step 5: Verify Live Endpoints & Audit on EC2 ===")
    # Re-run seeding script in audit mode to verify 0 missing and 100% complete
    audit_cmd = f"cd /var/www/dbert-website-lms && {REMOTE_VENV_PYTHON} scripts/seed_all_9_domains_7day_courses.py"
    audit_res = run_ssh(audit_cmd)
    print(audit_res.stdout)

    # Test HTTP 200 response on public courses API endpoint
    http_res = run_ssh("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5001/api/public/courses")
    http_code = http_res.stdout.strip()
    print(f"LMS API status code: HTTP {http_code}")
    assert http_code == "200", f"Expected HTTP 200 from /api/public/courses, got {http_code}"

    print("\n[SUCCESS] Production EC2 deployment and 7-day courses verification completed successfully!")


if __name__ == "__main__":
    main()
