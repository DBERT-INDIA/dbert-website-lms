import subprocess
import os

ssh_key = r"C:\Users\user\.ssh\dbert-production-server.pem"
server = "ubuntu@3.26.237.171"

script_content = """import psycopg2

conn = psycopg2.connect("postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms")
cur = conn.cursor()

try:
    cur.execute('SELECT count(*) FROM "Certificate"')
    print('Prisma Certificate table count:', cur.fetchone()[0])
except Exception as e:
    print('Prisma Certificate table error:', e)
    conn.rollback()

try:
    cur.execute('SELECT count(*) FROM intern_certificates')
    print('LMS intern_certificates table count:', cur.fetchone()[0])
    cur.execute('SELECT cert_id, course_title FROM intern_certificates LIMIT 5')
    print('Sample intern_certificates:', cur.fetchall())
except Exception as e:
    print('LMS intern_certificates error:', e)
"""

with open("scripts/remote_probe.py", "w") as f:
    f.write(script_content)

# scp to server
subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", "scripts/remote_probe.py", f"{server}:/tmp/remote_probe.py"])

# run on server using the portal virtual environment
res = subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 /tmp/remote_probe.py"], capture_output=True, text=True)
print("STDOUT:")
print(res.stdout)
print("STDERR:")
print(res.stderr)
