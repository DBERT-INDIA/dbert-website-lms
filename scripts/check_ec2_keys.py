import subprocess

remote_code = """
import sys, os
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
os.chdir('/var/www/dbert-website-lms/apps/portal')
from dotenv import load_dotenv
load_dotenv('.env')

from app import get_db
with get_db() as conn:
    rows = conn.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'intern_offer_letters'").fetchall()
    print("Columns:", [dict(r) for r in rows])
"""

cmd = [
    "ssh",
    "-i", r"C:\Users\user\.ssh\dbert-production-server.pem",
    "-o", "StrictHostKeyChecking=no",
    "ubuntu@3.26.237.171",
    "/var/www/dbert-website-lms/apps/portal/.venv/bin/python"
]

res = subprocess.run(cmd, input=remote_code, capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
