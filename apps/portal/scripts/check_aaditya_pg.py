import sys
import psycopg2

def run():
    try:
        conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
        cur = conn.cursor()
        
        cur.execute("SELECT id, name, email FROM intern_accounts WHERE name = 'Aaditya kadam'")
        print("Intern Account:", cur.fetchone())
        
        cur.execute("SELECT * FROM attendance WHERE email LIKE '%aadityakadam432%'")
        rows = cur.fetchall()
        print("Attendance rows:", len(rows), rows)
        
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    run()
