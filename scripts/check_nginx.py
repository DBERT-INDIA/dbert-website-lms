import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

script = """
import os
for f in os.listdir('/etc/nginx/sites-enabled'):
    print('=== ' + f + ' ===')
    with open('/etc/nginx/sites-enabled/' + f) as fp:
        print(fp.read())
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
