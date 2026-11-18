import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, get_db

with app.app_context():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM enrollments WHERE intern_id IN (SELECT id FROM intern_accounts WHERE email = 'smoke.tester@dbert.test')")
    cur.execute("DELETE FROM intern_accounts WHERE email = 'smoke.tester@dbert.test'")
    conn.commit()
    print("Cleaned up smoke test records successfully from production DB.")
