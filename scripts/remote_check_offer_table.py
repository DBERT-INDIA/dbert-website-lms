
import os
import psycopg2

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    # Read from .env
    with open('/var/www/dbert-website-lms/apps/portal/.env') as f:
        for line in f:
            if line.startswith('DATABASE_URL='):
                db_url = line.strip().split('=', 1)[1].strip('"').strip("'")
                break

conn = psycopg2.connect(db_url)
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'intern_offer_letters'")
print("Tables found:", cur.fetchall())

cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'intern_offer_letters' ORDER BY ordinal_position")
for col, dt in cur.fetchall():
    print(f"  {col}: {dt}")

conn.close()
