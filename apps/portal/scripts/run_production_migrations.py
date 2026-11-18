#!/usr/bin/env python3
"""
Master Production Migration Runner for DBERT-LMS on EC2.
Sequentially and idempotently applies all Guided Learning V2 and security migrations:
- Phase 1: PostgreSQL FK & Schema Repair
- Phase 6: gl_learning_turns (Atomic turn ledger)
- Phase 8: gl_student_learning_profile (True skill mastery profile)
- Phase 9: gl_course_chunks (RAG knowledge base)
- Phase 11: user_api_keys encryption_version (Key metadata versioning)
- Phase 12: gl_teacher_learning_instructions (Teacher/Mentor directives)
"""

import os
import sys

# Auto-load .env from apps/portal/.env if DATABASE_URL is not set
def load_env():
    portal_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(portal_dir, ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k not in os.environ:
                        os.environ[k] = v

load_env()
if not os.environ.get("DATABASE_URL") and os.path.exists("/var/www/dbert-website-lms/apps/portal/.env"):
    load_env()

# Ensure portal path is available
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database.adapter import get_db_adapter, PostgreSQLAdapter

MIGRATIONS = [
    ("Phase 1: PostgreSQL Relational Integrity Repair", """
        -- Phase 1 is executed via custom logic below if on postgres
    """),
    ("Phase 6: Learning Turns Ledger (gl_learning_turns)", """
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
        CREATE INDEX IF NOT EXISTS idx_gl_turns_session ON gl_learning_turns(session_id);
        CREATE INDEX IF NOT EXISTS idx_gl_turns_student ON gl_learning_turns(student_id);
        CREATE UNIQUE INDEX IF NOT EXISTS idx_gl_turns_idem ON gl_learning_turns(idempotency_key) WHERE idempotency_key IS NOT NULL;
    """),
    ("Phase 8: Student Learning Profile (gl_student_learning_profile)", """
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
    """),
    ("Phase 9: RAG Knowledge Chunks (gl_course_chunks)", """
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
        CREATE INDEX IF NOT EXISTS idx_gl_chunks_course ON gl_course_chunks(course_id);
        CREATE INDEX IF NOT EXISTS idx_gl_chunks_concept ON gl_course_chunks(concept_id);
    """),
    ("Phase 11: BYOK Key Encryption Versioning", """
        ALTER TABLE user_api_keys ADD COLUMN IF NOT EXISTS encryption_version INTEGER DEFAULT 1;
    """),
    ("Phase 12: Teacher/Mentor Learning Instructions (gl_teacher_learning_instructions)", """
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
        CREATE INDEX IF NOT EXISTS idx_gl_teacher_inst_student 
        ON gl_teacher_learning_instructions(student_id, course_id, concept_id);
    """),
    ("Phase 14: Technical Publishing Hub & Spotlights (intern_articles)", """
        CREATE TABLE IF NOT EXISTS intern_articles (
            id SERIAL PRIMARY KEY,
            intern_id INTEGER NOT NULL,
            domain TEXT,
            title TEXT NOT NULL,
            content_markdown TEXT NOT NULL,
            status TEXT DEFAULT 'DRAFT',
            mentor_feedback TEXT,
            published_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_intern_articles_intern ON intern_articles(intern_id, status);

        CREATE TABLE IF NOT EXISTS ecosystem_spotlights (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            url TEXT NOT NULL,
            target_brand TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS spotlight_clicks (
            id SERIAL PRIMARY KEY,
            intern_id INTEGER,
            spotlight_id INTEGER,
            clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """),
    ("Phase 15: Offer Letters and Admin Notes (intern_offer_letters)", """
        CREATE TABLE IF NOT EXISTS intern_offer_letters (
            id SERIAL PRIMARY KEY,
            offer_letter_id TEXT UNIQUE NOT NULL,
            intern_id INTEGER,
            enrollment_id INTEGER,
            email TEXT NOT NULL,
            name TEXT NOT NULL,
            domain TEXT NOT NULL,
            college TEXT,
            batch_start_date TEXT NOT NULL,
            batch_end_date TEXT NOT NULL,
            tenure_months INTEGER DEFAULT 2,
            stipend_amount INTEGER DEFAULT 5000,
            login_hours_per_week INTEGER DEFAULT 10,
            required_certifications INTEGER DEFAULT 2,
            required_bounty_tasks INTEGER DEFAULT 75,
            caution_deposit_amount INTEGER DEFAULT 499,
            caution_deposit_status TEXT DEFAULT 'VERIFIED',
            signature_name TEXT,
            accepted_at TEXT,
            pdf_unlocked INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_offer_letters_email ON intern_offer_letters(email);
        CREATE INDEX IF NOT EXISTS idx_offer_letters_offer_id ON intern_offer_letters(offer_letter_id);
        ALTER TABLE applications ADD COLUMN IF NOT EXISTS admin_note TEXT;
    """)
]


def run_all():
    print("=" * 70)
    print(" DBERT-LMS Production Migration Suite")
    print("=" * 70)

    db = get_db_adapter()
    engine_type = "postgres" if isinstance(db, PostgreSQLAdapter) else "sqlite"
    print(f"Connected engine: {engine_type.upper()}")

    # Run Phase 1 repairs first if PostgreSQL
    if engine_type == "postgres":
        print("\n--> Checking Phase 1 PostgreSQL repairs...")
        try:
            from scripts.phase1_postgres_repair import run as run_phase1
            run_phase1()
        except Exception as e:
            print(f"    Notice on Phase 1 repair: {e}")

    # Run phases 6 through 12
    with db as conn:
        cur = conn.cursor()
        for title, sql in MIGRATIONS[1:]:
            print(f"\n--> Applying {title}...")
            try:
                # If engine is SQLite, adapt SERIAL to INTEGER AUTOINCREMENT
                statements = [s.strip() for s in sql.strip().split(";") if s.strip()]
                for stmt in statements:
                    if engine_type == "sqlite":
                        stmt = stmt.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
                        stmt = stmt.replace("ADD COLUMN IF NOT EXISTS", "ADD COLUMN")
                    cur.execute(stmt)
                if hasattr(conn, "commit"):
                    conn.commit()
                print(f"    [SUCCESS] {title}")
            except Exception as e:
                # If column already exists on SQLite, ignore
                if "duplicate column name" in str(e).lower():
                    print(f"    [OK] Column already exists: {title}")
                else:
                    print(f"    [ERROR] Failed {title}: {e}")
                    raise

    print("\n" + "=" * 70)
    print(" All production migrations completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    run_all()
