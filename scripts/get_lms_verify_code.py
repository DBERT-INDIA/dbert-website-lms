import subprocess

ssh_key = r"C:\Users\user\.ssh\dbert-production-server.pem"
server = "ubuntu@3.26.237.171"

remote_code = """with open('/var/www/dbert-website-lms/apps/portal/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '/api/verify' in line:
        print(f"Line {i+1}:")
        for j in range(i, min(i+40, len(lines))):
            print(f"  {lines[j].rstrip()}")
        break
"""

with open("scripts/remote_probe.py", "w", encoding="utf-8") as f:
    f.write(remote_code)

subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", "scripts/remote_probe.py", f"{server}:/tmp/remote_probe.py"], check=True)
res = subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 /tmp/remote_probe.py"], capture_output=True, text=True)
print("OUTPUT:")
print(res.stdout)
