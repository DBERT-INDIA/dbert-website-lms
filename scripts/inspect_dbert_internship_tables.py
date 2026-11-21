import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')

from app import app, get_db

with app.app_context():
    with get_db() as conn:
        tables = conn.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'dbert_internship'
            ORDER BY table_name
        """).fetchall()
        table_names = [t['table_name'] for t in tables]
        print("Tables in dbert_internship:", table_names)

        for t in table_names:
            cnt = conn.execute(f"SELECT COUNT(*) as c FROM {t}").fetchone()
            print(f"  {t}: {cnt['c']}")
