import subprocess

pem = r"C:\Users\user\.ssh\dbert-production-server.pem"
host = "ubuntu@3.26.237.171"

remote_code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db, hash_password

p_hash = hash_password('TestPass123!')

with get_db() as conn:
    conn.execute("INSERT INTO applications (id, name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status, created_at, updated_at) VALUES (9200, 'Farhan Ali (Gate 1 Locked)', 'stipend_gate1_locked@dbert.test', '+91 98765 11111', 'Mumbai', 'BITS Pilani', 'B.Tech IT', 8, 2026, 'Full Stack Web Development', 'Gate 1 locked test candidate', 'Enrolled', NOW(), NOW()) ON CONFLICT (id) DO UPDATE SET status = 'Enrolled'")
    conn.execute("INSERT INTO intern_accounts (id, application_id, name, email, phone, city, college, course, semester, year_of_passing, domain, password_hash, password_set, is_active, created_at, updated_at, email_verified, account_status) VALUES (9200, 9200, 'Farhan Ali (Gate 1 Locked)', 'stipend_gate1_locked@dbert.test', '+91 98765 11111', 'Mumbai', 'BITS Pilani', 'B.Tech IT', 8, 2026, 'Full Stack Web Development', ?, 1, 1, NOW(), NOW(), 1, 'active') ON CONFLICT (id) DO UPDATE SET password_hash = EXCLUDED.password_hash, password_set = 1, is_active = 1", (p_hash,))
    conn.commit()
    print("✓ stipend_gate1_locked@dbert.test seeded successfully!")
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
