import subprocess
import sys
import os

PEM_PATH = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

def run_ssh(cmd):
    print(f"[SSH CMD] {cmd}")
    res = subprocess.run(
        ["ssh", "-i", PEM_PATH, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, cmd],
        capture_output=True,
        text=True
    )
    print("STDOUT:", res.stdout.strip())
    if res.stderr.strip():
        print("STDERR:", res.stderr.strip())
    if res.returncode != 0:
        print(f"FAILED with return code {res.returncode}")
        sys.exit(1)
    return res.stdout

def run_scp(local_path, remote_path):
    print(f"[SCP] {local_path} -> {remote_path}")
    res = subprocess.run(
        ["scp", "-i", PEM_PATH, "-o", "StrictHostKeyChecking=no", local_path, f"{REMOTE_HOST}:{remote_path}"],
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        print("SCP ERROR:", res.stderr)
        sys.exit(1)
    print("  ✓ Upload complete")

print("=== DEPLOYING SCREENSHOT ROUTE & UTR VOUCHER ENGINE FIXES TO EC2 ===")

# 1. Upload app.py
run_scp("apps/portal/app.py", "/var/www/dbert-website-lms/apps/portal/app.py")

# 2. Upload admin.html
run_scp("apps/portal/templates/admin.html", "/var/www/dbert-website-lms/apps/portal/templates/admin.html")

# 3. Upload nginx config to /tmp and copy to /etc/nginx/sites-available/dbert-unified.conf
run_scp("deploy/dbert-unified-nginx.conf", "/tmp/dbert-unified.conf")
run_ssh("sudo cp /tmp/dbert-unified.conf /etc/nginx/sites-available/dbert-unified.conf && sudo nginx -t && sudo systemctl reload nginx")

# 4. Restart dbert-portal service
run_ssh("sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service")

print("\n=== DEPLOYMENT AND RESTART SUCCESSFUL! ===")
