import sys
import os

if os.path.exists('/var/www/dbert-website-lms/apps/portal'):
    sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
else:
    sys.path.insert(0, 'apps/portal')

from app import get_db

with get_db() as conn:
    # Check intern_accounts for created_at, source, signup_stage
    rows = conn.execute("""
        SELECT a.id, a.name, a.email, a.phone, a.college, a.city, a.source, a.created_at,
               i.id as intern_id, i.created_at as account_created_at
        FROM applications a
        LEFT JOIN intern_accounts i ON LOWER(i.email) = LOWER(a.email)
        WHERE a.status = 'Under Review'
        ORDER BY a.id DESC
        LIMIT 10
    """).fetchall()

    for r in rows:
        d = dict(r) if hasattr(r, 'keys') else {'id': r[0], 'name': r[1], 'email': r[2], 'app_created': str(r[7]), 'acct_created': str(r[9])}
        print(f"App {d['id']}: {d['name']} ({d['email']}) | App Created: {d.get('created_at', d.get('app_created'))} | Acct Created: {d.get('account_created_at', d.get('acct_created'))}")
