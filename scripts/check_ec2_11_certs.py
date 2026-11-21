import psycopg2

conn = psycopg2.connect('postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms')
cur = conn.cursor()

cert_ids = [
    'CERT-DBERT-2026-DA-173', 'CERT-DBERT-2026-DA-048', 'CERT-DBERT-2026-FSD-156',
    'CERT-DBERT-2026-FSD-046', 'CERT-DBERT-2026-DA-019', 'CERT-DBERT-2026-AIML-002',
    'CERT-DBERT-2026-AIML-013', 'CERT-DBERT-2026-DA-049', 'CERT-DBERT-2026-DA-117',
    'CERT-DBERT-2026-AIML-020', 'CERT-DBERT-2026-DA-186'
]

cur.execute("""
    SELECT cert_id, intern_id, course_title, tier, email 
    FROM intern_certificates 
    WHERE cert_id = ANY(%s)
""", (cert_ids,))

rows = cur.fetchall()
print(f"Found {len(rows)} matching certs in DB out of {len(cert_ids)}:")
for r in rows:
    print(r)
