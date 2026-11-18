#!/usr/bin/env python3
"""
Phase 15: Intern Offer Letters Table & Applications Admin Note Migration
Creates intern_offer_letters and adds admin_note column to applications.
Safe and idempotent for both PostgreSQL and SQLite.
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

# Ensure portal path is available
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database.adapter import get_db_adapter, PostgreSQLAdapter

SQL_POSTGRES = """
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
"""

SQL_SQLITE = """
CREATE TABLE IF NOT EXISTS intern_offer_letters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    created_at TEXT DEFAULT (datetime('now','localtime')),
    updated_at TEXT DEFAULT (datetime('now','localtime'))
);

CREATE INDEX IF NOT EXISTS idx_offer_letters_email ON intern_offer_letters(email);
CREATE INDEX IF NOT EXISTS idx_offer_letters_offer_id ON intern_offer_letters(offer_letter_id);
"""

def run():
    print("=" * 70)
    print(" Phase 15 Migration: intern_offer_letters & admin_note")
    print("=" * 70)

    db = get_db_adapter()
    engine_type = "postgres" if isinstance(db, PostgreSQLAdapter) else "sqlite"
    print(f"Connected engine: {engine_type.upper()}")

    sql_to_run = SQL_POSTGRES if engine_type == "postgres" else SQL_SQLITE

    with db as conn:
        cur = conn.cursor()
        statements = [s.strip() for s in sql_to_run.strip().split(";") if s.strip()]
        for stmt in statements:
            try:
                cur.execute(stmt)
                print(f"  [SUCCESS] {stmt[:60].replace(chr(10), ' ')}...")
            except Exception as e:
                if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                    print(f"  [ALREADY EXISTS] {e}")
                else:
                    print(f"  [ERROR] {e}")
                    raise

        # Check SQLite applications column admin_note
        if engine_type == "sqlite":
            try:
                cur.execute("PRAGMA table_info(applications);")
                cols = [r[1] for r in cur.fetchall()]
                if "admin_note" not in cols:
                    cur.execute("ALTER TABLE applications ADD COLUMN admin_note TEXT;")
                    print("  [SUCCESS] Added admin_note to SQLite applications table.")
                else:
                    print("  [OK] admin_note already in SQLite applications table.")
            except Exception as ex:
                print(f"  [NOTICE SQLite admin_note] {ex}")

        if hasattr(conn, "commit"):
            conn.commit()

    print("\nPhase 15 migration completed successfully!")

if __name__ == "__main__":
    run()
