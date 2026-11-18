import subprocess
import sys
import os

PEM_PATH = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

FILES_TO_SCP = [
    ("apps/portal/app.py", f"{REMOTE_BASE}/apps/portal/app.py"),
    ("apps/portal/templates/index.html", f"{REMOTE_BASE}/apps/portal/templates/index.html"),
    ("apps/portal/templates/portal.html", f"{REMOTE_BASE}/apps/portal/templates/portal.html"),
    ("apps/portal/templates/admin.html", f"{REMOTE_BASE}/apps/portal/templates/admin.html"),
    ("AGENTS.md", f"{REMOTE_BASE}/AGENTS.md"),
    ("GEMINI.md", f"{REMOTE_BASE}/GEMINI.md"),
]

def run(cmd):
    print(f">> {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)
    if res.returncode != 0:
        print(f"FAILED with code {res.returncode}")
        sys.exit(1)

print("=== Uploading Stage Funnel & Profile Completion Fixes to EC2 ===")
for local_f, remote_f in FILES_TO_SCP:
    print(f"Uploading {local_f} -> {remote_f}")
    scp_cmd = f'scp -i "{PEM_PATH}" -o StrictHostKeyChecking=no {local_f} {REMOTE_HOST}:{remote_f}'
    run(scp_cmd)

print("\\n=== Restarting dbert-portal.service on EC2 ===")
restart_cmd = f'ssh -i "{PEM_PATH}" -o StrictHostKeyChecking=no {REMOTE_HOST} "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"'
run(restart_cmd)

print("\\n=== Deployment Finished Successfully ===")
