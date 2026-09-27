import psycopg2

def run():
    try:
        conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM intern_accounts WHERE id=2161")
        row = cur.fetchone()
        print("intern_accounts id=2161:", row)
        
        cur.execute("SELECT id, email FROM intern_accounts LIMIT 5")
        print("Sample:", cur.fetchall())
        
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    run()
