import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

script = """
import os

with open('/var/www/dbert-website-lms/apps/portal/app.py') as f:
    text = f.read()

import re
for m in re.finditer(r'Logged out', text):
    start = max(0, text.rfind('\\n', 0, m.start()-100))
    end = min(len(text), text.find('\\n', m.end()+100))
    print(text[start:end])
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
