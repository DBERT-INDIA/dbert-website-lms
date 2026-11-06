import subprocess
import sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

REMOTE_SCRIPT = """
echo "=== Check virtualenvs on EC2 ==="
ls -la /var/www/dbert-website-lms/apps/portal/
cat /etc/systemd/system/dbert-portal.service || true
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
