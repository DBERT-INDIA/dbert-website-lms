import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.database.adapter import get_db_adapter

def run():
    print("Executing Phase 9 Schema Migration...")
    try:
        db = get_db_adapter()
        with db.get_connection() as conn:
            cur = conn.cursor()
            print("Creating gl_course_chunks table...")
            cur.execute('''
                CREATE TABLE IF NOT EXISTS gl_course_chunks (
                    chunk_id TEXT PRIMARY KEY,
                    course_id INTEGER NOT NULL,
                    course_version TEXT NOT NULL,
                    module_id INTEGER,
                    concept_id TEXT,
                    subtopic_id INTEGER,
                    difficulty INTEGER DEFAULT 1,
                    content_type TEXT NOT NULL,
                    source TEXT NOT NULL,
                    text_content TEXT NOT NULL,
                    embedding_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
            ''')
            
            print("Creating indexes...")
            cur.execute('CREATE INDEX IF NOT EXISTS idx_gl_chunks_course ON gl_course_chunks(course_id);')
            cur.execute('CREATE INDEX IF NOT EXISTS idx_gl_chunks_concept ON gl_course_chunks(concept_id);')
            
            if hasattr(conn, "commit"):
                conn.commit()
            print("Migration successful.")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == '__main__':
    run()
