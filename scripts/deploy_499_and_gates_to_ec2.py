import os
import sys
import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_PORTAL = "/var/www/dbert-website-lms/apps/portal"

FILES_TO_UPLOAD = [
    ("apps/portal/app.py", f"{REMOTE_PORTAL}/app.py"),
    ("apps/portal/templates/portal.html", f"{REMOTE_PORTAL}/templates/portal.html"),
    ("apps/portal/templates/stipend_tasks.html", f"{REMOTE_PORTAL}/templates/stipend_tasks.html"),
    ("apps/portal/templates/admin_articles.html", f"{REMOTE_PORTAL}/templates/admin_articles.html"),
]

def run_cmd(cmd):
    print(f"\n[RUNNING] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout)
    if res.stderr:
        print(f"[STDERR] {res.stderr}")
    if res.returncode != 0:
        print(f"[FAILED] Code {res.returncode}")
        sys.exit(res.returncode)
    return res.stdout

def main():
    print("=" * 80)
    print("Deploying Modernized ₹499 Payment & 4-Gate Progression to EC2...")
    print("=" * 80)

    for local_f, remote_f in FILES_TO_UPLOAD:
        print(f"Uploading {local_f} -> {remote_f}...")
        scp_cmd = f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no "{local_f}" {HOST}:{remote_f}'
        run_cmd(scp_cmd)

    print("\nRestarting dbert-portal.service on EC2...")
    ssh_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no {HOST} "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"'
    out = run_cmd(ssh_cmd)
    if "active" in out:
        print("\n✓ dbert-portal.service is ACTIVE and running on production!")
    else:
        print(f"\n[WARN] Service status: {out}")

    print("\nLive testing portal endpoints on EC2...")
    probe_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no {HOST} "curl -sI https://lms.dbert.in/portal | head -n 5"'
    run_cmd(probe_cmd)

    print("\nDeployment complete successfully!")

if __name__ == "__main__":
    main()
