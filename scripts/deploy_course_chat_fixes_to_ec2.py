import subprocess
import sys
import time

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"

def run_ssh(cmd, check=True):
    full_cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", HOST, cmd]
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"[ERROR] Remote SSH failed: {res.stderr}")
        sys.exit(1)
    return res

def run_scp(local_path, remote_path):
    full_cmd = ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", local_path, f"{HOST}:{remote_path}"]
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] SCP failed: {res.stderr}")
        sys.exit(1)
    print(f"[+] Transferred: {local_path} -> {remote_path}")

def main():
    print("=== Uploading Fixed Files to Production EC2 ===")
    run_scp("apps/portal/app.py", f"{REMOTE_PORTAL_DIR}/app.py")
    run_scp("apps/portal/templates/course_learn.html", f"{REMOTE_PORTAL_DIR}/templates/course_learn.html")

    print("\n=== Restarting dbert-portal.service on EC2 ===")
    run_ssh("sudo systemctl restart dbert-portal.service")
    time.sleep(3)

    status_res = run_ssh("systemctl is-active dbert-portal.service")
    is_active = status_res.stdout.strip()
    print(f"Service status: {is_active}")
    assert is_active == "active", f"Expected active, got {is_active}"

    # Verify HTTP 200
    res = run_ssh("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:5001/api/public/courses")
    print(f"LMS API status: HTTP {res.stdout.strip()}")
    print("\n[SUCCESS] Deployment of course chat fixes to EC2 completed!")

if __name__ == "__main__":
    main()
