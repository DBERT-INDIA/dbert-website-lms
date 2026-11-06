import subprocess

ssh_key = r"C:\Users\user\.ssh\dbert-production-server.pem"
server = "ubuntu@3.26.237.171"

remote_code = """import psycopg2

conn = psycopg2.connect("postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms")
cur = conn.cursor()

for tbl in ['applicants', 'applications']:
    try:
        cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{tbl}' ORDER BY ordinal_position;")
        cols = cur.fetchall()
        print(f"Table {tbl} exists with {len(cols)} columns:")
        for col in cols[:6]:
            print(f"  {col[0]}: {col[1]}")
    except Exception as e:
        print(f"Table {tbl} error:", e)
        conn.rollback()

conn.close()
"""

with open("scripts/remote_probe.py", "w") as f:
    f.write(remote_code)

subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", "scripts/remote_probe.py", f"{server}:/tmp/remote_probe.py"])
res = subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 /tmp/remote_probe.py"], capture_output=True, text=True)
print("OUTPUT:")
print(res.stdout)
if res.stderr:
    print("ERROR:")
    print(res.stderr)
