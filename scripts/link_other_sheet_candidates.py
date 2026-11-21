import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')

from app import app, get_db
from services.certificate_service import CertificateService

with app.app_context():
    with get_db() as conn:
        targets = [
            (4640, "Oishani Majumder", "skylvies@gmail.com", "majumderoishani@gmail.com", "CERT-DBERT-2026-DA-009", "Data Analyst"),
            (4931, "Pravallika Potnuru", "pravallikapotnuru1816@gmail.com", "pravallikapotnuru18@gmail.com", "CERT-DBERT-2026-FSD-028", "Full Stack Development"),
            (4949, "Siva Sankar Thirumalasetty", "t.sivasankardell@gmail.com", "sivasankar.t1606@gmail.com", "CERT-DBERT-2026-DA-067", "Data Analyst"),
        ]
        
        for intern_id, name, lms_email, sheet_email, cert_id, track in targets:
            v_before = CertificateService.is_intern_verified(conn, intern_id=intern_id, email=lms_email)
            print(f"\n{name} (ID {intern_id}) before link: verified={v_before.get('verified')}, status={v_before.get('status')}")
            
            existing = conn.execute("SELECT id FROM intern_certificates WHERE intern_id = ? OR email = ?", (intern_id, lms_email)).fetchone()
            if not existing:
                print(f"Linking {name} ({lms_email}) to {cert_id}...")
                conn.execute("""
                    INSERT INTO intern_certificates 
                    (intern_id, course_id, course_title, cert_id, issued_at, url, tier, email)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (intern_id, 0, track, cert_id, "2026-11-16", f"/verify/{cert_id}", "verified", lms_email))
                conn.commit()
            
            v_after = CertificateService.is_intern_verified(conn, intern_id=intern_id, email=lms_email)
            print(f"{name} (ID {intern_id}) after link: verified={v_after.get('verified')}, status={v_after.get('status')}, cert={v_after.get('cert_id')}")
