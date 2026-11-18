import subprocess

pem = r"C:\Users\user\.ssh\dbert-production-server.pem"
host = "ubuntu@3.26.237.171"

remote_code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    cols = conn.execute("SELECT column_name FROM information_schema.columns WHERE table_schema='dbert_internship' AND table_name='mentor_availability_slots'").fetchall()
    print('mentor_availability_slots cols:', [c[0] for c in cols])
"""

p = subprocess.Popen(
    ["ssh", "-i", pem, "-o", "StrictHostKeyChecking=no", host, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
stdout, stderr = p.communicate(input=remote_code)
print("STDOUT:\n", stdout)
