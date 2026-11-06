import subprocess

ssh_key = r"C:\Users\user\.ssh\dbert-production-server.pem"
server = "ubuntu@3.26.237.171"

remote_code = """import psycopg2

conn = psycopg2.connect("postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms")
cur = conn.cursor()
cur.execute("SET search_path TO dbert_internship, public;")

cur.execute("SELECT id, name, email FROM intern_accounts WHERE email = 'kushalagarwal27496@gmail.com';")
print("Kushal in intern_accounts:", cur.fetchall())

cur.execute("SELECT id, name, email FROM applications WHERE email = 'kushalagarwal27496@gmail.com';")
print("Kushal in applications:", cur.fetchall())

conn.close()
"""

with open("scripts/remote_probe.py", "w", encoding="utf-8") as f:
    f.write(remote_code)

subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", "scripts/remote_probe.py", f"{server}:/tmp/remote_probe.py"], check=True)
res = subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 /tmp/remote_probe.py"], capture_output=True, text=True)
print("OUTPUT:")
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
