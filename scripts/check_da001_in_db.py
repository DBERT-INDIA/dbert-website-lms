import subprocess

ssh_key = r"C:\Users\user\.ssh\dbert-production-server.pem"
server = "ubuntu@3.26.237.171"

remote_code = """import psycopg2

conn = psycopg2.connect("postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms")
cur = conn.cursor()

cur.execute("SELECT * FROM intern_certificates WHERE cert_id = 'CERT-DBERT-2026-DA-001';")
cert = cur.fetchall()
print("intern_certificates match:")
for c in cert:
    print(c)

if cert:
    intern_id = cert[0][1]
    cur.execute(f"SELECT * FROM applications WHERE id = {intern_id};")
    print("applications match for intern_id", intern_id, ":")
    print(cur.fetchall())

conn.close()
"""

with open("scripts/remote_probe.py", "w") as f:
    f.write(remote_code)

subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", "scripts/remote_probe.py", f"{server}:/tmp/remote_probe.py"], check=True)
res = subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 /tmp/remote_probe.py"], capture_output=True, text=True)
print("OUTPUT:")
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
