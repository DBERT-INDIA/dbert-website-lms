import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_code = """
import psycopg2

conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
c = conn.cursor()

for t in ['security_deposits', 'payments', 'course_payments', 'intern_certificates', 'intern_offer_letters']:
    c.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{t}';")
    cols = [r[0] for r in c.fetchall()]
    print(f"{t}: {cols}")

conn.close()
"""

with open("scripts/remote_check_cols.py", "w", encoding="utf-8") as f:
    f.write(remote_code)

scp_cmd = f'scp -i "{PEM_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes scripts/remote_check_cols.py {REMOTE_HOST}:/tmp/remote_check_cols.py'
subprocess.run(scp_cmd, shell=True, check=True)

venv_py = "/var/www/dbert-website-lms/apps/portal/.venv/bin/python"
run_cmd = f'ssh -i "{PEM_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {REMOTE_HOST} "{venv_py} /tmp/remote_check_cols.py && rm -f /tmp/remote_check_cols.py"'
res = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
