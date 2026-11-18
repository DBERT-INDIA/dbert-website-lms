import subprocess

code = """
import subprocess

cmd = "sudo journalctl -u dbert-portal.service --since '2026-11-17 00:00:00' | grep -iE 'signup|nakshathiraa|kowshikreddy|gowthamb|rkuma9141' | tail -n 50"
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate()
print("JOURNAL OUTPUT:")
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
