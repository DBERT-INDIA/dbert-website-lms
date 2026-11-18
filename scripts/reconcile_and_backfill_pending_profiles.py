import subprocess

code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

CORRECTIONS = [
    # (email, correct_domain)
    ('nakshathiraa07@gmail.com', 'Python Automation'),
    ('bhatayush55@gmail.com', 'Cybersecurity'),
    ('mdrazaali151@gmail.com', 'Data Analyst'),
    ('laxmanaddagatla0506@gmail.com', 'UI/UX Design'),
    ('rimjhimkanaujia24@gmail.com', 'Cybersecurity'),
    ('vaipatil05@gmail.com', 'DevOps & Cloud'),
    ('jishnanisham.jn40@gmail.com', 'Cybersecurity'),
]

with get_db() as conn:
    print('--- Step 1: Correcting domain for leads where target track is known ---')
    for email, domain in CORRECTIONS:
        conn.execute('UPDATE applications SET domain=? WHERE LOWER(email)=LOWER(?)', (domain, email))
        conn.execute('UPDATE intern_accounts SET domain=? WHERE LOWER(email)=LOWER(?)', (domain, email))
        print(f'Updated {email} -> domain: {domain}')

    print('\\n--- Step 2: Categorizing Pending Profile direct signups as Apply Pending ---')
    cur = conn.execute('''
        UPDATE applications 
        SET status='Apply Pending'
        WHERE college='Pending Profile' 
          AND status='Under Review'
          AND why_join='Enrolled via DBERT portal direct registration.'
    ''')
    print(f'Updated {cur.rowcount} applications from Under Review to Apply Pending')
    conn.commit()

    print('\\n--- Step 3: Verification of recent applications ---')
    rows = conn.execute('''
        SELECT id, name, email, domain, college, status 
        FROM applications 
        WHERE id >= 5190 
        ORDER BY id DESC
    ''').fetchall()
    for r in rows:
        print(dict(r))
"""

p = subprocess.Popen(
    ["ssh", "-i", r"C:\Users\user\.ssh\dbert-production-server.pem", "-o", "StrictHostKeyChecking=no", "ubuntu@3.26.237.171", "/var/www/dbert-website-lms/apps/portal/.venv/bin/python", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
out, err = p.communicate(input=code)
print(out)
if err:
    print("ERR:", err)
