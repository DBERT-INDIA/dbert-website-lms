"""
scripts/migrate_mentor_group_capacity.py
========================================
Migrates mentor availability slots and session bookings to support
Group Mentorship sessions with up to 30 interns per slot.

Safe for both SQLite (local development) and PostgreSQL (production EC2).
"""
import os
import sys

# Ensure apps/portal is on path
portal_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "portal"))
if portal_dir not in sys.path:
    sys.path.insert(0, portal_dir)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(portal_dir, ".env"))
except ImportError:
    pass

# Ensure local test compatibility if not on production postgres
if "DATABASE_URL" not in os.environ:
    os.environ.setdefault("FLASK_DEBUG", "true")

from services.database.adapter import get_db_adapter

def run_migration():
    print(">>> Starting Mentor Group Mentorship capacity migration...")
    db = get_db_adapter()
    dialect = getattr(db, "dialect", "sqlite")
    print(f"[*] Detected database dialect: {dialect}")

    with db as conn:
        # 1. Ensure columns on mentor_availability_slots
        cols_to_add = [
            ("capacity", "INTEGER DEFAULT 30"),
            ("seats_booked", "INTEGER DEFAULT 0"),
            ("domain", "TEXT DEFAULT 'All Tracks'"),
            ("topic", "TEXT DEFAULT 'Technical Mentorship & Capstone Review'"),
        ]

        if dialect == "postgres":
            for col, defn in cols_to_add:
                try:
                    conn.execute(f"ALTER TABLE mentor_availability_slots ADD COLUMN IF NOT EXISTS {col} {defn}")
                    print(f" [+] Postgres column ensured: mentor_availability_slots.{col}")
                except Exception as e:
                    print(f" [!] Postgres add column notice: {e}")

            # Remove unique constraint on slot_id in mentor_session_bookings if exists
            try:
                conn.execute("ALTER TABLE mentor_session_bookings DROP CONSTRAINT IF EXISTS mentor_session_bookings_slot_id_key")
                print(" [+] Postgres dropped unique constraint on slot_id")
            except Exception as e:
                print(f" [!] Postgres drop constraint notice: {e}")

            try:
                conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_mentor_booking_slot_intern ON mentor_session_bookings(slot_id, intern_id)")
                print(" [+] Postgres created compound unique index on (slot_id, intern_id)")
            except Exception as e:
                print(f" [!] Postgres compound index notice: {e}")

        else:
            # SQLite
            existing_cols = [r["name"] for r in conn.execute("PRAGMA table_info(mentor_availability_slots)").fetchall()]
            for col, defn in cols_to_add:
                if col not in existing_cols:
                    conn.execute(f"ALTER TABLE mentor_availability_slots ADD COLUMN {col} {defn}")
                    print(f" [+] SQLite column added: mentor_availability_slots.{col}")
                else:
                    print(f" [=] SQLite column already exists: mentor_availability_slots.{col}")

            # For SQLite mentor_session_bookings, check if table definition contains UNIQUE on slot_id
            create_sql = conn.execute("SELECT sql FROM sqlite_master WHERE name='mentor_session_bookings' AND type='table'").fetchone()
            if create_sql and "slot_id INTEGER NOT NULL UNIQUE" in create_sql[0]:
                print(" [*] SQLite table mentor_session_bookings has UNIQUE constraint on slot_id. Recreating safely...")
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS mentor_session_bookings_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        slot_id INTEGER NOT NULL,
                        intern_id INTEGER NOT NULL,
                        meeting_link TEXT,
                        status TEXT DEFAULT 'booked',
                        created_at TEXT DEFAULT (datetime('now','localtime')),
                        FOREIGN KEY(slot_id) REFERENCES mentor_availability_slots(id),
                        FOREIGN KEY(intern_id) REFERENCES intern_accounts(id),
                        UNIQUE(slot_id, intern_id)
                    )
                """)
                conn.execute("INSERT OR IGNORE INTO mentor_session_bookings_new SELECT id, slot_id, intern_id, meeting_link, status, created_at FROM mentor_session_bookings")
                conn.execute("DROP TABLE mentor_session_bookings")
                conn.execute("ALTER TABLE mentor_session_bookings_new RENAME TO mentor_session_bookings")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_mentor_bookings ON mentor_session_bookings(intern_id, status)")
                print(" [+] SQLite mentor_session_bookings migrated with compound UNIQUE(slot_id, intern_id)")
            else:
                conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_mentor_booking_slot_intern ON mentor_session_bookings(slot_id, intern_id)")
                print(" [=] SQLite mentor_session_bookings already supports multi-intern slots")

        # 2. Backfill seats_booked and is_booked
        print(" [*] Recalculating seats_booked and is_booked status across all slots...")
        if dialect == "postgres":
            conn.execute("""
                UPDATE mentor_availability_slots s
                SET seats_booked = COALESCE((
                    SELECT COUNT(*) FROM mentor_session_bookings b WHERE b.slot_id = s.id AND b.status = 'booked'
                ), 0)
            """)
            conn.execute("""
                UPDATE mentor_availability_slots
                SET is_booked = CASE WHEN seats_booked >= COALESCE(capacity, 30) THEN 1 ELSE 0 END
            """)
        else:
            conn.execute("""
                UPDATE mentor_availability_slots
                SET seats_booked = COALESCE((
                    SELECT COUNT(*) FROM mentor_session_bookings WHERE slot_id = mentor_availability_slots.id AND status = 'booked'
                ), 0)
            """)
            conn.execute("""
                UPDATE mentor_availability_slots
                SET is_booked = CASE WHEN seats_booked >= COALESCE(capacity, 30) THEN 1 ELSE 0 END
            """)

        conn.commit()
    print(">>> Migration completed successfully!")

if __name__ == "__main__":
    run_migration()
