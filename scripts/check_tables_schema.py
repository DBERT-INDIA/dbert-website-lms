import os
import psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

def show_cols(table):
    c.execute(f"""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = '{table}'
        ORDER BY ordinal_position;
    """)
    rows = c.fetchall()
    print(f"\n--- Columns in {table} ---")
    for r in rows:
        print(f"  {r[0]} ({r[1]}, nullable={r[2]})")

show_cols('intern_accounts')
show_cols('intern_offer_letters')
show_cols('applications')
