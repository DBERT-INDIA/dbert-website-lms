import psycopg2

conn = psycopg2.connect("postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms")
cur = conn.cursor()
cur.execute("SET search_path TO dbert_internship, public;")

# Ensure CERT-DBERT-2026-DA-001 points to Kushal Agarwal (intern_account 4513)
cur.execute("""
    UPDATE intern_certificates
    SET intern_id = 4513,
        email = 'kushalagarwal27496@gmail.com',
        course_title = 'DBERT Technical Incubation — Data Analyst',
        issued_at = '04 November 2026',
        received_at = '04 November 2026',
        url = '/verify?certid=CERT-DBERT-2026-DA-001'
    WHERE cert_id = 'CERT-DBERT-2026-DA-001';
""")

conn.commit()
print("PostgreSQL intern_certificates updated for CERT-DBERT-2026-DA-001!")

cur.execute("""
    SELECT c.cert_id, c.intern_id, COALESCE(a.name, ap.name, 'Intern') AS recipient_name,
           COALESCE(a.domain, ap.domain, 'Engineering') AS domain
    FROM intern_certificates c
    LEFT JOIN intern_accounts a ON (a.id = c.intern_id OR (c.email IS NOT NULL AND LOWER(a.email) = LOWER(c.email)))
    LEFT JOIN applications ap ON (c.email IS NOT NULL AND LOWER(ap.email) = LOWER(c.email))
    WHERE c.cert_id = 'CERT-DBERT-2026-DA-001';
""")
print("LMS query result:", cur.fetchall())
conn.close()
