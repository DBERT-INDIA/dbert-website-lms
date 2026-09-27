import os
import psycopg2

def main():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL not set")
        return
        
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Find all foreign keys in dbert_internship that point to public
    cur.execute("""
        SELECT tc.table_name, tc.constraint_name, 
               kcu.column_name, 
               ccu.table_name AS foreign_table_name, 
               ccu.column_name AS foreign_column_name
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
    
    if not rows:
        print("No broken foreign keys found. Everything is already pointing to dbert_internship.")
        return
        
    print(f"Found {len(rows)} broken foreign keys pointing to the old schema. Fixing them now...")
    
    # Process them one by one
    for r in rows:
        table = r[0]
        constraint = r[1]
        column = r[2]
        f_table = r[3]
        f_column = r[4]
        
        drop_sql = f"ALTER TABLE dbert_internship.{table} DROP CONSTRAINT IF EXISTS {constraint};"
        add_sql = f"ALTER TABLE dbert_internship.{table} ADD CONSTRAINT {constraint} FOREIGN KEY ({column}) REFERENCES dbert_internship.{f_table}({f_column});"
        
        try:
            print(f"Fixing {table}.{column} -> {f_table}.{f_column}...")
            cur.execute(drop_sql)
            cur.execute(add_sql)
        except Exception as e:
            print(f"Error fixing {constraint}: {e}")
            conn.rollback()
            continue
            
    conn.commit()
    print("All Foreign Keys successfully repaired! Your coins and tasks will now work properly.")

if __name__ == "__main__":
    main()
