import os
import sys

# we can just use the adapter from the app to run raw queries!
sys.path.append('apps/portal')
from services.database.adapter import get_db_adapter

try:
    adapter = get_db_adapter()
    print(f"Adapter: {type(adapter)}")
    
    with adapter as conn:
        print("Executing test queries...")
        # Check if 3167 is in intern_accounts
        res = conn.execute("SELECT id FROM intern_accounts WHERE id=3167").fetchone()
        print(f"Result 3167: {res}")
        
        # Check foreign keys
        res = conn.execute("""
            SELECT conname, pg_get_constraintdef(c.oid)
            FROM pg_constraint c
            JOIN pg_class t ON c.conrelid = t.oid
            WHERE t.relname = 'course_enrollments' AND contype = 'f';
        """).fetchall()
        for r in res:
            print(f"FK: {r}")
            
except Exception as e:
    print(f"Error: {e}")
