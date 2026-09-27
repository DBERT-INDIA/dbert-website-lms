import sqlite3
import psycopg2

def run():
    try:
        s_conn = sqlite3.connect('apps/portal/internship.db')
        s_cur = s_conn.cursor()
        
        p_conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
        p_cur = p_conn.cursor()
        
        s_cur.execute("SELECT * FROM attendance LIMIT 5")
        rows = s_cur.fetchall()
        cols = [description[0] for description in s_cur.description]
        
        col_str = ", ".join([f'"{c}"' for c in cols])
        val_placeholders = ", ".join(["%s"] * len(cols))
        insert_query = f'INSERT INTO "public"."attendance" ({col_str}) VALUES ({val_placeholders}) ON CONFLICT DO NOTHING;'
        
        for row in rows:
            try:
                p_cur.execute(insert_query, row)
                p_conn.commit()
                print("Success:", row)
            except Exception as e:
                p_conn.rollback()
                print("Failed:", row, "Error:", e)
                
    except Exception as e:
        print("Fatal Error:", e)

if __name__ == "__main__":
    run()
