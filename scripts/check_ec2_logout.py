import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

script = """
with open('/var/www/dbert-website-lms/apps/portal/app.py') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 15995 <= i <= 16025:
        print(f"{i+1}: {l}", end="")
"""

p = subprocess.Popen(
    ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "python3", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
out, err = p.communicate(input=script)
print("OUT:\n", out)
if err:
    print("ERR:\n", err)
