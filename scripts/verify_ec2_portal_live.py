import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

script = """
import os
import psycopg2

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    # Read from .env
    with open('/var/www/dbert-website-lms/apps/portal/.env') as f:
        for line in f:
            if line.startswith('DATABASE_URL='):
                db_url = line.strip().split('=', 1)[1].strip('"').strip("'")
                break

conn = psycopg2.connect(db_url)
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'intern_offer_letters'")
print("Tables found:", cur.fetchall())

cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'intern_offer_letters' ORDER BY ordinal_position")
for col, dt in cur.fetchall():
    print(f"  {col}: {dt}")

conn.close()
"""

# Upload check script
with open("scripts/remote_check_offer_table.py", "w") as f:
    f.write(script)

subprocess.run(f'scp -i "{SSH_KEY}" scripts/remote_check_offer_table.py {HOST}:/tmp/check_offer.py', shell=True)
res = subprocess.run(f'ssh -i "{SSH_KEY}" {HOST} "python3 /tmp/check_offer.py"', shell=True, capture_output=True, text=True)
print("Remote DB Output:")
print(res.stdout)
if res.stderr:
    print("Remote DB Stderr:", res.stderr)
