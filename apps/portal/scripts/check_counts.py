import sys
import psycopg2

def run():
    try:
        conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
        cur = conn.cursor()
        
        tables = ['intern_accounts', 'applications', 'enrollments', 'attendance']
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            print(f"{table}: {cur.fetchone()[0]}")
            
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    run()
