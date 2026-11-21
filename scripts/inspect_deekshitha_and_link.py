import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')

from app import app, get_db
from services.certificate_service import CertificateService

with app.app_context():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM intern_certificates WHERE intern_id = 4745 OR email ILIKE '%ndeekshitha%'").fetchall()
        print("Existing DB rows for Deekshitha:", [dict(r) for r in rows])
        
        # Check current verification status for 4745
        v1 = CertificateService.is_intern_verified(conn, intern_id=4745, email="ndeekshitha07.24@kgpian.iitkgp.ac.in")
        print("Verification status before link:", v1)
        
        # Let's ensure intern_certificates has the record for intern_id=4745 with cert_id='CERT-DBERT-2026-AIML-092'
        # Check if record exists
        existing = conn.execute("SELECT id FROM intern_certificates WHERE intern_id = 4745 OR email = 'ndeekshitha07.24@kgpian.iitkgp.ac.in'").fetchone()
        if not existing:
            print("Inserting verified certificate record for N Deekshitha (ID 4745)...")
            conn.execute("""
                INSERT INTO intern_certificates 
                (intern_id, course_id, course_title, cert_id, issued_at, url, tier, email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                4745, 
                0, 
                "Artificial Intelligence & Machine Learning", 
                "CERT-DBERT-2026-AIML-092", 
                "2026-11-16", 
                "/verify/CERT-DBERT-2026-AIML-092", 
                "verified", 
                "ndeekshitha07.24@kgpian.iitkgp.ac.in"
            ))
            conn.commit()
            print("Successfully inserted verified record into intern_certificates!")
        else:
            print("Existing record found:", dict(existing))
            
        # Re-check verification status
        v2 = CertificateService.is_intern_verified(conn, intern_id=4745, email="ndeekshitha07.24@kgpian.iitkgp.ac.in")
        print("Verification status after link:", v2)
