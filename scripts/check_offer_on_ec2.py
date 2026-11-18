import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

cmd = """
with open('/var/www/dbert-website-lms/apps/portal/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '/portal/offer' in l:
        for j in range(max(0, i-2), min(len(lines), i+25)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
"""

with open("scripts/check_offer_ec2.py", "w", encoding="utf-8") as f:
    f.write(cmd)

subprocess.run([
    "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
    "scripts/check_offer_ec2.py", f"{HOST}:/tmp/check_offer_ec2.py"
], check=True)

res = subprocess.run([
    "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
    HOST,
    "/var/www/dbert-website-lms/apps/portal/.venv/bin/python /tmp/check_offer_ec2.py && rm -f /tmp/check_offer_ec2.py"
], capture_output=True, text=True)

print("STDOUT:\n", res.stdout)
print("STDERR:\n", res.stderr)
