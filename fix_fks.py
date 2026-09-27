import sys
import os
sys.path.append('apps/portal')
from services.database.adapter import get_db_adapter

try:
    adapter = get_db_adapter()
    conn = adapter._raw_conn
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute("ALTER TABLE course_enrollments DROP CONSTRAINT IF EXISTS course_enrollments_intern_id_fkey;")
    print("Dropped course_enrollments_intern_id_fkey")
except Exception as e:
    print(f"Error: {e}")
