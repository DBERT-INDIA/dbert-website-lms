#!/usr/bin/env python3
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

conn = get_db()
cur = conn.cursor()
cur.execute('''
    SELECT ia.id, ia.name, ia.email, ia.domain, ia.linkedin_url, ia.github_url,
           CASE WHEN ia.upi_id_encrypted IS NOT NULL AND ia.upi_id_encrypted != '' THEN true ELSE false END as has_upi,
           ic.tier, art.title, art.status
    FROM intern_articles art
    LEFT JOIN intern_accounts ia ON art.intern_id = ia.id
    LEFT JOIN intern_certificates ic ON LOWER(ia.email) = LOWER(ic.email)
    WHERE art.status ILIKE '%publish%'
''')
authors = cur.fetchall()
print(f'Published Article Authors ({len(authors)}):')
for a in authors:
    print(f'* {a[1]} ({a[2]}) | Domain: {a[3]} | LinkedIn: {bool(a[4])} | GitHub: {bool(a[5])} | UPI: {a[6]} | CertTier: {a[7]} | Article: {a[8][:40]}')
