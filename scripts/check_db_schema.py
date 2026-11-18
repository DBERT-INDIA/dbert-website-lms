import psycopg2
import json

DB_URL = "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms"
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

def print_cols(table):
    cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}'")
    print(f"\n--- {table} ---")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]}")

print_cols('enrollments')
print_cols('applications')
print_cols('intern_certificates')
print_cols('intern_accounts')

conn.close()
