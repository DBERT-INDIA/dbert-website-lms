import sys
sys.path.append('apps/portal')
from app import get_db

with get_db() as conn:
    rows = conn.execute("""
        SELECT COUNT(DISTINCT ia.id) as c
        FROM intern_accounts ia
        WHERE ia.is_active = 1 AND (
            EXISTS (SELECT 1 FROM intern_certificates WHERE intern_id = ia.id OR LOWER(email) = LOWER(ia.email))
            OR EXISTS (SELECT 1 FROM task_submissions WHERE (intern_id = ia.id OR LOWER(email) = LOWER(ia.email)) AND status = 'approved')
            OR EXISTS (SELECT 1 FROM attendance WHERE intern_id = ia.id OR LOWER(email) = LOWER(ia.email))
            OR EXISTS (SELECT 1 FROM intern_articles WHERE intern_id = ia.id AND status = 'PUBLISHED')
        )
    """).fetchone()
    print("Candidates with any activity:", rows['c'])
