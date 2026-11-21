import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')

from app import app, get_db

with app.app_context():
    with get_db() as conn:
        tables = conn.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """).fetchall()
        table_names = [t['table_name'] for t in tables]
        print("Tables in PostgreSQL:", table_names)

        payment_tables = [t for t in table_names if any(w in t.lower() for w in ('pay', 'enroll', 'fee', 'utr', 'order', 'trans', 'stipend'))]
        print("\nRelevant payment/enrollment tables:", payment_tables)

        for pt in payment_tables:
            try:
                cnt = conn.execute(f"SELECT COUNT(*) as c FROM {pt}").fetchone()
                print(f"Table '{pt}' row count: {cnt['c']}")
            except Exception as e:
                print(f"Error querying {pt}: {e}")
