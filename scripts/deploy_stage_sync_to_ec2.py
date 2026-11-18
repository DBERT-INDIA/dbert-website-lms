import subprocess
import sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_DIR = "/var/www/dbert-website-lms/apps/portal"

files = [
    ("apps/portal/app.py", f"{REMOTE_DIR}/app.py"),
    ("apps/portal/templates/portal.html", f"{REMOTE_DIR}/templates/portal.html"),
    ("apps/portal/templates/portal_offer_letter.html", f"{REMOTE_DIR}/templates/portal_offer_letter.html"),
]

for local_f, remote_f in files:
    print(f"Uploading {local_f} -> {remote_f}...")
    cmd = [
        "scp",
        "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        local_f,
        f"{HOST}:{remote_f}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error uploading {local_f}: {res.stderr}")
        sys.exit(1)
    print(f"Successfully uploaded {local_f}")

print("Restarting dbert-portal.service on EC2...")
restart_cmd = [
    "ssh",
    "-i", SSH_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "BatchMode=yes",
    HOST,
    "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"
]
res = subprocess.run(restart_cmd, capture_output=True, text=True)
print(f"Service status: {res.stdout.strip()}")
if res.returncode != 0:
    print(f"Error restarting service: {res.stderr}")
    sys.exit(1)

print("Deployment complete and verified!")
