import sys
import os

# Ensure we can import the app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.database.adapter import get_db_adapter

def heal_database():
    try:
        adapter = get_db_adapter()
        conn = adapter._raw_conn
        
        print("Connected to PostgreSQL database.")
        
        # We must disable autocommit to run REINDEX inside psycopg2 if it was in a transaction,
        # but actually psycopg2 starts a transaction by default. We must SET autocommit = True
        # so it doesn't wrap REINDEX in a transaction block.
        conn.autocommit = True
        cur = conn.cursor()
        
        tables_to_reindex = [
            "intern_accounts",
            "applications",
            "courses",
            "course_enrollments",
            "post_applications",
            "posts",
            "companies",
            "attendance",
            "user_sessions"
        ]
        
        for table in tables_to_reindex:
            print(f"Reindexing table {table}...")
            try:
                cur.execute(f"REINDEX TABLE {table};")
                print(f"  -> Reindex Success.")
                
                # Sync sequence if it has an id column
                cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table}' AND column_name='id'")
                if cur.fetchone():
                    # Get max id
                    cur.execute(f"SELECT MAX(id) FROM {table}")
                    max_id_row = cur.fetchone()
                    max_id = max_id_row[0] if max_id_row and max_id_row[0] else 0
                    
                    if max_id > 0:
                        # Find the sequence name
                        seq_name = f"{table}_id_seq"
                        try:
                            cur.execute(f"SELECT setval('{seq_name}', {max_id});")
                            print(f"  -> Sequence '{seq_name}' synced to {max_id}.")
                        except Exception as seq_err:
                            print(f"  -> Could not sync sequence '{seq_name}': {seq_err}")
                            # rollback any error state so the loop can continue
                            pass
            except Exception as e:
                print(f"  -> Error: {e}")
                
        print("Database healed successfully.")
        
    except Exception as e:
        print(f"Failed to heal database: {e}")

if __name__ == "__main__":
    heal_database()
