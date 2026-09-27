import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.database.adapter import get_db_adapter

def run():
    print("Executing Phase 6 Schema Migration...")
    try:
        db = get_db_adapter()
        with db.get_connection() as conn:
            cur = conn.cursor()
            print("Creating gl_learning_turns table...")
            cur.execute('''
                CREATE TABLE IF NOT EXISTS gl_learning_turns (
                    id SERIAL PRIMARY KEY,
                    turn_uuid TEXT UNIQUE NOT NULL,
                    session_id TEXT NOT NULL,
                    student_id INTEGER NOT NULL,
                    concept_id TEXT NOT NULL,
                    idempotency_key TEXT,
                    student_input TEXT NOT NULL,
                    evaluation_json TEXT NOT NULL,
                    recommendation_json TEXT NOT NULL,
                    assistant_response TEXT,
                    status TEXT DEFAULT 'completed',
                    created_at TEXT NOT NULL,
                    completed_at TEXT NOT NULL
                );
            ''')
            
            print("Creating indexes...")
            cur.execute('CREATE INDEX IF NOT EXISTS idx_gl_turns_session ON gl_learning_turns(session_id);')
            cur.execute('CREATE INDEX IF NOT EXISTS idx_gl_turns_student ON gl_learning_turns(student_id);')
            cur.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_gl_turns_idem ON gl_learning_turns(idempotency_key) WHERE idempotency_key IS NOT NULL;')
            
            if hasattr(conn, "commit"):
                conn.commit()
            print("Migration successful.")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == '__main__':
    run()
