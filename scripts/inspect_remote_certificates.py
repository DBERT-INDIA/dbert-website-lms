import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')

from app import app, get_db

with app.app_context():
    with get_db() as conn:
        cols = conn.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = 'dbert_internship' AND table_name = 'intern_certificates'
            ORDER BY ordinal_position
        """).fetchall()
        print("Columns in intern_certificates:")
        for c in cols:
            print(f"  {c['column_name']} ({c['data_type']})")
            
        sample = conn.execute("SELECT * FROM intern_certificates LIMIT 3").fetchall()
        print(f"\nSample records ({len(sample)}):")
        for s in sample:
            print(dict(s))
            
        # Check if our 4 candidates exist in intern_certificates
        cert_ids = ['CERT-DBERT-2026-DA-111', 'CERT-DBERT-2026-UIUX-034', 'CERT-DBERT-2026-FSD-072', 'CERT-DBERT-2026-DA-188']
        existing = conn.execute("SELECT * FROM intern_certificates WHERE certificate_id = ANY(%s)", (cert_ids,)).fetchall()
        print(f"\nExisting in intern_certificates matching the 4 certs ({len(existing)}):")
        for e in existing:
            print(dict(e))
            
        # Also check intern_accounts for these 4 candidates
        emails = ['24211a7259@bvrit.ac.in', 'shreyn18007@gmail.com', 'bhavyabalchandani23@gmail.com', 'tehreemfatimabsmath@gmail.com']
        accounts = conn.execute("SELECT id, name, email, role FROM intern_accounts WHERE email = ANY(%s)", (emails,)).fetchall()
        print(f"\nMatching intern_accounts ({len(accounts)}):")
        for a in accounts:
            print(dict(a))
