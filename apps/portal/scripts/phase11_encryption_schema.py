import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.database.adapter import get_db_adapter

def run():
    print("Executing Phase 11 Schema Migration...")
    try:
        db = get_db_adapter()
        with db as conn:
            cur = conn.cursor()
            
            print("Adding encryption_version column if not exists...")
            cur.execute('ALTER TABLE user_api_keys ADD COLUMN IF NOT EXISTS encryption_version INTEGER DEFAULT 1;')
                
            if hasattr(conn, "commit"):
                conn.commit()
            print("Migration successful.")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == '__main__':
    run()
