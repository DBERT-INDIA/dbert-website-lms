import psycopg2
import json

with open('/tmp/certificates_registry.json', 'r', encoding='utf-8') as f:
    registry = json.load(f)

conn = psycopg2.connect("postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms")
cur = conn.cursor()

inserted_apps = 0
inserted_certs = 0
updated_certs = 0

for cert_id, rec in registry.items():
    holder_name = rec["holderName"]
    email = rec["email"]
    domain = rec["domain"]
    college = rec.get("college") or "Institution of Technology"
    phone = rec.get("phone") or "9999999999"
    course_title = f"DBERT Technical Incubation — {domain}"
    issued_at = rec.get("evalDate", "04 November 2026")
    url = f"/verify?certid={cert_id}"
    
    # Check if cert already exists
    cur.execute("SELECT id, intern_id FROM intern_certificates WHERE cert_id = %s;", (cert_id,))
    row = cur.fetchone()
    
    if row:
        intern_app_id = row[1]
        cur.execute("""
            UPDATE intern_certificates 
            SET course_title = %s, url = %s, email = %s, issued_at = %s, received_at = %s
            WHERE cert_id = %s;
        """, (course_title, url, email, issued_at, issued_at, cert_id))
        updated_certs += 1
    else:
        # Check if application exists by email
        cur.execute("SELECT id FROM applications WHERE email = %s LIMIT 1;", (email,))
        app_row = cur.fetchone()
        if app_row:
            intern_app_id = app_row[0]
        else:
            cur.execute("""
                INSERT INTO applications (name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status)
                VALUES (%s, %s, %s, 'India', %s, 'Computer Science / Engineering', '8th Semester', '2026', %s, 'Incubation & Credential Verification', 'Verified')
                RETURNING id;
            """, (holder_name, email, phone, college, domain))
            intern_app_id = cur.fetchone()[0]
            inserted_apps += 1
            
        cur.execute("""
            INSERT INTO intern_certificates (intern_id, course_id, course_title, cert_id, issued_at, url, received_at, tier, email)
            VALUES (%s, 1, %s, %s, %s, %s, %s, 'dbert_verified', %s);
        """, (intern_app_id, course_title, cert_id, issued_at, url, issued_at, email))
        inserted_certs += 1

conn.commit()
conn.close()

print(f"DATABASE SEEDING RESULT: {inserted_certs} certs inserted, {updated_certs} certs updated, {inserted_apps} applications created.")
