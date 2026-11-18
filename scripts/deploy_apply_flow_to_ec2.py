import subprocess
import sys
import time

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"

FILES_TO_DEPLOY = [
    ("apps/portal/app.py", f"{REMOTE_PORTAL_DIR}/app.py"),
    ("apps/portal/templates/post_detail.html", f"{REMOTE_PORTAL_DIR}/templates/post_detail.html"),
    ("apps/portal/templates/scraped_internship_detail.html", f"{REMOTE_PORTAL_DIR}/templates/scraped_internship_detail.html"),
]

def run_cmd(cmd):
    print(f"[CMD] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] (Code {res.returncode}):\n{res.stderr}")
        return False, res.stderr
    print(res.stdout)
    return True, res.stdout

def deploy():
    print("=== DEPLOYING JOB APPLY FLOW TO PRODUCTION EC2 ===")

    # 1. SCP files
    for local_f, remote_f in FILES_TO_DEPLOY:
        scp_cmd = f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes "{local_f}" "{HOST}:{remote_f}"'
        ok, out = run_cmd(scp_cmd)
        if not ok:
            print(f"Failed to scp {local_f}")
            sys.exit(1)
        print(f"Uploaded: {local_f} -> {remote_f}")

    # 2. Restart dbert-portal.service
    print("\n--- Restarting dbert-portal.service on EC2 ---")
    restart_cmd = (
        f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {HOST} '
        '"sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"'
    )
    ok, out = run_cmd(restart_cmd)
    if not ok or "active" not in out:
        print("Failed to restart dbert-portal.service or service is not active!")
        sys.exit(1)

    print("\n--- Service active status confirmed! ---")

if __name__ == "__main__":
    deploy()
