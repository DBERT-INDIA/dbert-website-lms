import subprocess
import sys

files_to_deploy = [
    ("apps/portal/app.py", "/var/www/dbert-website-lms/apps/portal/app.py"),
    ("apps/portal/services/ai/gemini_discovery.py", "/var/www/dbert-website-lms/apps/portal/services/ai/gemini_discovery.py"),
    ("apps/portal/services/ai/model_registry.py", "/var/www/dbert-website-lms/apps/portal/services/ai/model_registry.py"),
]

ssh_key = r"C:\Users\user\.ssh\dbert-production-server.pem"
host = "ubuntu@3.26.237.171"

print("==> Uploading modified files to EC2...")
for local_f, remote_f in files_to_deploy:
    cmd = ["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", local_f, f"{host}:{remote_f}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Failed to copy {local_f}: {res.stderr}")
        sys.exit(1)
    print(f"Uploaded {local_f} -> {remote_f}")

print("==> Restarting dbert-portal.service on EC2...")
restart_cmd = ["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", host, "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"]
res = subprocess.run(restart_cmd, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
if "active" in res.stdout:
    print("==> dbert-portal.service is ACTIVE!")
else:
    print("==> Failed to verify active status!")
    sys.exit(1)
