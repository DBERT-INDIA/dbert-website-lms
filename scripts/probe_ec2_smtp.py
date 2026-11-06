import subprocess
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

code = """
import smtplib, ssl
try:
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ctx) as s:
        s.login('abhinav.sharma@dbert.in', 'ckxnpudkapzgzbxl')
        s.sendmail('abhinav.sharma@dbert.in', ['abhinav.sharma@dbert.in'], 'Subject: Probe\\n\\nProbe')
        print('EC2: Send success!')
except Exception as e:
    print('EC2 SMTP Error:', e)
"""

b64 = base64.b64encode(code.encode('utf-8')).decode('utf-8')
ssh_cmd = [
    "ssh",
    "-i", r"C:\Users\user\.ssh\dbert-production-server.pem",
    "-o", "StrictHostKeyChecking=no",
    "-o", "BatchMode=yes",
    "ubuntu@3.26.237.171",
    f"python3 -c \"import base64; exec(base64.b64decode('{b64}').decode())\""
]

res = subprocess.run(ssh_cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
