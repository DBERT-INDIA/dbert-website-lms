import subprocess

code = """
import subprocess

cmd = "sudo grep -E '14.194.31.190|152.57.82.33|134.82.69.66' /var/log/nginx/access.log | tail -n 40"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate()
print("NGINX ACCESS LOGS:")
print(out)
if err:
    print("ERR:", err)
"""

p = subprocess.Popen(
    ["ssh", "-i", r"C:\Users\user\.ssh\dbert-production-server.pem", "-o", "StrictHostKeyChecking=no", "ubuntu@3.26.237.171", "/var/www/dbert-website-lms/apps/portal/.venv/bin/python", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
out, err = p.communicate(input=code)
print(out)
if err:
    print("ERR:", err)
