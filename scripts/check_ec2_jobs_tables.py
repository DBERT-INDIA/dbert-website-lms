import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_script = """
import os
import psycopg2
from pathlib import Path

# read .env
env_dict = {}
env_file = Path('/var/www/dbert-website-lms/apps/portal/.env')
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env_dict[k.strip()] = v.strip().strip('"').strip("'")

db_url = env_dict.get('DATABASE_URL', 'postgresql://ubuntu@localhost/dbert_portal')
conn = psycopg2.connect(db_url)
c = conn.cursor()
c.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [t[0] for t in c.fetchall()]
print('All tables on EC2 PostgreSQL:', tables)
"""

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
