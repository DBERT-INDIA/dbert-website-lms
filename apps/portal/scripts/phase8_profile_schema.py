import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.database.adapter import get_db_adapter

def run():
    print("Executing Phase 8 Schema Migration...")
    try:
        db = get_db_adapter()
        with db as conn:
            cur = conn.cursor()
            print("Creating gl_student_learning_profile table...")
            cur.execute('''
                CREATE TABLE IF NOT EXISTS gl_student_learning_profile (
                    student_id INTEGER PRIMARY KEY,
                    overall_mastery REAL DEFAULT 0.0,
                    overall_confidence REAL DEFAULT 0.0,
                    learning_velocity REAL DEFAULT 1.0,
                    preferred_explanation_depth TEXT DEFAULT 'STANDARD',
                    practice_strength REAL DEFAULT 0.0,
                    conceptual_strength REAL DEFAULT 0.0,
                    recent_struggle_index REAL DEFAULT 0.0,
                    retention_index REAL DEFAULT 1.0,
                    mentor_interventions INTEGER DEFAULT 0,
                    last_learning_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
            ''')
            
            if hasattr(conn, "commit"):
                conn.commit()
            print("Migration successful.")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == '__main__':
    run()
