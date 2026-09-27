import os
import psycopg2

def main():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("Set DATABASE_URL")
        return

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
    """)
    tables = [r[0] for r in cur.fetchall()]

    print(f"{'TABLE_NAME':<30} | {'PUBLIC_COUNT':<12} | {'DBERT_COUNT':<12}")
    print("-" * 60)
    for table in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM public.{table}")
            pub_count = cur.fetchone()[0]
        except Exception:
            conn.rollback()
            pub_count = "ERROR"

        try:
            cur.execute(f"SELECT COUNT(*) FROM dbert_internship.{table}")
            dbert_count = cur.fetchone()[0]
        except Exception:
            conn.rollback()
            dbert_count = "MISSING"

        print(f"{table:<30} | {str(pub_count):<12} | {str(dbert_count):<12}")

if __name__ == "__main__":
    main()
