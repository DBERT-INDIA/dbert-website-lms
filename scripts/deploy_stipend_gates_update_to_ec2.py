import subprocess
import sys
import os

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

def run_cmd(cmd, check=True):
    print(f"Executing: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout)
    if res.stderr:
        print(res.stderr, file=sys.stderr)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {res.returncode}")
    return res

def deploy():
    print("=== DEPLOYING STIPEND GATES UPDATE TO EC2 ===")
    
    # 1. SCP modified files
    files = [
        ("apps/portal/services/certificate_service.py", f"{REMOTE_BASE}/apps/portal/services/certificate_service.py"),
        ("apps/portal/templates/stipend_tasks.html", f"{REMOTE_BASE}/apps/portal/templates/stipend_tasks.html"),
        ("apps/portal/templates/portal.html", f"{REMOTE_BASE}/apps/portal/templates/portal.html")
    ]
    
    for local_f, remote_f in files:
        if not os.path.exists(local_f):
            raise FileNotFoundError(f"Local file not found: {local_f}")
        scp_cmd = f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes "{local_f}" {HOST}:{remote_f}'
        run_cmd(scp_cmd)
        print(f"✓ Uploaded {local_f} -> {remote_f}")

    # 2. Restart dbert-portal.service on EC2
    restart_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {HOST} "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"'
    res = run_cmd(restart_cmd)
    print(f"Service status: {res.stdout.strip()}")
    
    # 3. Live verification on EC2
    verify_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {HOST} "python3 -c \\"import urllib.request; resp = urllib.request.urlopen(\'http://127.0.0.1:5001/stipend/tasks\'); print(\'HTTP Status:\', resp.status)\\""'
    verify_res = run_cmd(verify_cmd, check=False)
    print(f"Live verification output: {verify_res.stdout.strip()}")

    print("=== DEPLOYMENT AND VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    deploy()
