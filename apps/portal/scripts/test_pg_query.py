import sys
import psycopg2
from datetime import datetime, timedelta

def run():
    try:
        conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
        cur = conn.cursor()
        
        sixty_days_ago = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
        STATUS_ACCEPTED = "Accepted"
        
        query = """
                SELECT ia.id, ia.name, ia.email, ia.domain,
                       e.joining_date, e.batch_label
                FROM intern_accounts ia
                LEFT JOIN enrollments e ON LOWER(e.email) = LOWER(ia.email)
                WHERE ia.is_active = 1
                  AND (e.joining_date IS NULL OR e.joining_date >= %s)
                  AND EXISTS (
                      SELECT 1 FROM applications a 
                      WHERE LOWER(a.email) = LOWER(ia.email) 
                        AND LOWER(a.status) = LOWER(%s)
                  )
        """
        cur.execute(query, (sixty_days_ago, STATUS_ACCEPTED))
        rows = cur.fetchall()
        print(f"PostgreSQL Query returned {len(rows)} rows.")
        
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    run()
