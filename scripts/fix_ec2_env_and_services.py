import subprocess
import sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

REMOTE_SCRIPT = """
set -euo pipefail

echo "=== 1. Updating dbert-api .env with strong secrets ==="
python3 -c '
import secrets
from cryptography.fernet import Fernet

admin_key = secrets.token_urlsafe(32)
admin_pwd = secrets.token_urlsafe(24)
fernet_key = Fernet.generate_key().decode()

env_file = "/var/www/dbert-website-lms/dbert-api-package/.env"
with open(env_file, "r") as f:
    lines = f.readlines()

new_lines = []
has_admin_key = False
for line in lines:
    if line.startswith("ADMIN_KEY="):
        new_lines.append(f"ADMIN_KEY={admin_key}\\n")
        has_admin_key = True
    elif line.startswith("ADMIN_PASSWORD="):
        new_lines.append(f"ADMIN_PASSWORD={admin_pwd}\\n")
    elif line.startswith("FERNET_KEY="):
        new_lines.append(f"FERNET_KEY={fernet_key}\\n")
    else:
        new_lines.append(line)

if not has_admin_key:
    new_lines.append(f"ADMIN_KEY={admin_key}\\n")

with open(env_file, "w") as f:
    f.writelines(new_lines)
print("dbert-api .env updated successfully.")
'

echo "=== 2. Restarting dbert-api.service ==="
sudo systemctl restart dbert-api.service
sleep 3

echo "=== 3. Checking dbert-api.service status ==="
systemctl is-active dbert-api.service

echo "=== 4. Checking dbert-api port 8000 response ==="
curl -s http://127.0.0.1:8000/docs | head -n 10 || echo "FastAPI docs check"

echo "=== 5. Checking LMS Flask portal routing ==="
# Check Flask routes in apps/portal
python3 -c '
import sys
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
try:
    from app import app
    print("Listing LMS URL rules matching login or home:")
    for rule in app.url_map.iter_rules():
        if "login" in rule.rule or "auth" in rule.rule or rule.rule == "/":
            print(f"  {rule.rule} -> {rule.endpoint}")
except Exception as e:
    print(f"Error inspecting app: {e}")
'
"""

def main():
    script_bytes = REMOTE_SCRIPT.replace("\r", "").encode("utf-8")
    cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", HOST, "bash -s"]
    res = subprocess.run(cmd, input=script_bytes, capture_output=True)
    print("STDOUT:\n", res.stdout.decode("utf-8", errors="replace"))
    if res.stderr:
        print("STDERR:\n", res.stderr.decode("utf-8", errors="replace"))
    return res.returncode

if __name__ == "__main__":
    sys.exit(main())
