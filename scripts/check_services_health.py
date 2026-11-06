import subprocess
import sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

REMOTE_SCRIPT = """
echo "=== 1. Checking portal .venv python modules ==="
/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 -c '
try:
    import psycopg2
    print("psycopg2 is installed in portal .venv!")
except Exception as e:
    print(f"portal .venv psycopg2 check: {e}")
'

echo "=== 2. Check dbert-portal.service status ==="
sudo systemctl status dbert-portal.service --no-pager -l || true

echo "=== 3. Test LMS home page via curl ==="
curl -s -I http://127.0.0.1:5001/ || true

echo "=== 4. Test dbert-api /docs via curl ==="
curl -s -I http://127.0.0.1:8000/docs || true
"""

def main():
    script_bytes = REMOTE_SCRIPT.replace("\r", "").encode("utf-8")
    cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", HOST, "bash -s"]
    res = subprocess.run(cmd, input=script_bytes, capture_output=True)
    out_str = res.stdout.decode("utf-8", errors="replace").encode("ascii", errors="replace").decode("ascii")
    err_str = res.stderr.decode("utf-8", errors="replace").encode("ascii", errors="replace").decode("ascii")
    print("STDOUT:\n", out_str)
    if err_str:
        print("STDERR:\n", err_str)
    return res.returncode

if __name__ == "__main__":
    sys.exit(main())
