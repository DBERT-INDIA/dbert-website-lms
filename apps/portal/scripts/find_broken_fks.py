import os
import psycopg2

def main():
    db_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("""
        SELECT tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_schema AS foreign_table_schema, ccu.table_name AS foreign_table_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
          AND tc.table_schema = 'dbert_internship'
          AND ccu.table_schema = 'public';
    """)
    rows = cur.fetchall()
    print("BROKEN FOREIGN KEYS:")
    for r in rows:
        print(f"Table: {r[1]}, Constraint: {r[0]}, References: {r[3]}.{r[4]}")

if __name__ == "__main__":
    main()
