import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.database.adapter import get_db_adapter

def run():
    print("Executing Phase 12 Schema Migration...")
    try:
        db = get_db_adapter()
        with db.get_connection() as conn:
            cur = conn.cursor()
            
            print("Creating gl_teacher_learning_instructions table...")
            cur.execute('''
                CREATE TABLE IF NOT EXISTS gl_teacher_learning_instructions (
                    id SERIAL PRIMARY KEY,
                    teacher_id INTEGER NOT NULL,
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    concept_id TEXT,
                    instruction TEXT NOT NULL,
                    priority INTEGER DEFAULT 0,
                    starts_at TEXT,
                    expires_at TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(teacher_id) REFERENCES mentors(id),
                    FOREIGN KEY(student_id) REFERENCES intern_accounts(id),
                    FOREIGN KEY(course_id) REFERENCES courses(id)
                );
            ''')
            
            print("Creating index on student_id, course_id, concept_id...")
            cur.execute('''
                CREATE INDEX IF NOT EXISTS idx_gl_teacher_inst_student 
                ON gl_teacher_learning_instructions(student_id, course_id, concept_id);
            ''')
            
            if hasattr(conn, "commit"):
                conn.commit()
            print("Migration successful.")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == '__main__':
    run()
