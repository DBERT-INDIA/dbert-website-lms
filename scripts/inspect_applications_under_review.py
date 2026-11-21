import sys
import os

# Check if running locally or remotely
if os.path.exists('/var/www/dbert-website-lms/apps/portal'):
    sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
else:
    sys.path.insert(0, 'apps/portal')

from app import get_db

with get_db() as conn:
    rows = conn.execute("SELECT status, COUNT(*) as cnt FROM applications GROUP BY status").fetchall()
    print("=== Applications by Status ===")
    for r in rows:
        print(f"  {r['status'] if isinstance(r, dict) or hasattr(r, 'keys') else r[0]}: {r['cnt'] if isinstance(r, dict) or hasattr(r, 'keys') else r[1]}")

    under_review = conn.execute("SELECT id, name, email, phone, domain, status, created_at FROM applications WHERE status = 'Under Review' ORDER BY id DESC").fetchall()
    print(f"\nTotal 'Under Review': {len(under_review)}")
    for row in under_review[:10]:
        d = dict(row) if hasattr(row, 'keys') else {'id': row[0], 'name': row[1], 'email': row[2], 'phone': row[3], 'domain': row[4], 'status': row[5], 'created_at': row[6]}
        print(f"  ID {d['id']}: {d['name']} | {d['email']} | {d['phone']} | {d['domain']} | {d['created_at']}")
