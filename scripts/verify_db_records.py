import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')

from app import app, get_db

with app.app_context():
    with get_db() as conn:
        rows = conn.execute("""
            SELECT cert_id, tier, email, intern_id 
            FROM intern_certificates 
            WHERE cert_id IN ('CERT-DBERT-2026-DA-111', 'CERT-DBERT-2026-UIUX-034', 'CERT-DBERT-2026-FSD-072', 'CERT-DBERT-2026-DA-188')
        """).fetchall()
        print(f"Found {len(rows)} verified certs in PostgreSQL:")
        for r in rows:
            print(dict(r))
