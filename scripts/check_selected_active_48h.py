import sys
from datetime import datetime, timedelta
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

conn = get_db()
cur = conn.cursor()
t48 = (datetime.now() - timedelta(hours=48)).strftime('%Y-%m-%d %H:%M:%S')

cur.execute('''
    SELECT DISTINCT LOWER(s.email), a.name, a.domain, a.status, e.payment_status
    FROM user_sessions s
    JOIN applications a ON LOWER(s.email) = LOWER(a.email)
    LEFT JOIN enrollments e ON LOWER(s.email) = LOWER(e.email)
    WHERE s.created_at >= %s 
      AND a.status = 'Selected'
      AND (e.payment_status IS NULL OR e.payment_status NOT IN ('Accepted', 'Approved'))
''', (t48,))
rows = cur.fetchall()
print(f"Active 48h Selected (Unpaid) Users: {len(rows)}")
for r in rows:
    print(f"* {r[0]} ({r[1]}) | Domain: {r[2]} | App: {r[3]} | Enr: {r[4]}")
