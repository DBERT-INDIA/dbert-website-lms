import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, get_db

with app.app_context():
    with get_db() as conn:
        targets = [
            '24211a7259@bvrit.ac.in',
            'shreyn18007@gmail.com',
            'bhavyabalchandani23@gmail.com',
            'tehreemfatimabsmath@gmail.com'
        ]
        for em in targets:
            row = conn.execute("SELECT id, name, email, phone, domain, college FROM intern_accounts WHERE email ILIKE ?", (em,)).fetchone()
            print(f"LMS Account for {em}:", dict(row) if row else "Not found in intern_accounts")
