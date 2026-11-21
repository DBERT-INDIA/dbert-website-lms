import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

# 1. SCP files
files_to_upload = [
    ("apps/portal/app.py", "/var/www/dbert-website-lms/apps/portal/app.py"),
    ("apps/portal/routes/auth.py", "/var/www/dbert-website-lms/apps/portal/routes/auth.py"),
]

for local_path, remote_path in files_to_upload:
    print(f"Uploading {local_path} -> {remote_path}...")
    res = subprocess.run([
        "scp", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
        local_path, f"{REMOTE_HOST}:{remote_path}"
    ], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Failed to upload {local_path}: {res.stderr}")
        exit(1)
    print("Uploaded successfully.")

# 2. Restart dbert-portal.service on EC2
print("Restarting dbert-portal.service on EC2...")
remote_cmd = """
sudo systemctl restart dbert-portal.service
sleep 2
systemctl is-active dbert-portal.service
"""
res = subprocess.run([
    "ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
    REMOTE_HOST, remote_cmd
], capture_output=True, text=True)
print("Remote output:\n", res.stdout)
if res.stderr:
    print("Remote err:\n", res.stderr)
