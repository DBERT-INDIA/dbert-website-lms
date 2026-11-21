"""
scripts/migrate_coin_perks_catalog.py
================================================================================
Idempotent database migration script for LMS Coin Perks Catalog & Redemptions.
Works across both SQLite (local/dev) and PostgreSQL (production).
Creates:
  - coin_perks_catalog
  - coin_perk_redemptions
Seeds the initial catalog with user-specified pricing:
  1. ai_ats_scanner (100 coins)
  2. ai_mock_interview (100 coins)
  3. mentor_session_1on1 (500 coins)
  4. course_fee_discount (Dynamic, 1 coin = ₹1, up to 50% discount)
================================================================================
"""
import sys
import os
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "portal")))
os.environ.setdefault("TESTING", "true")

from services.database.adapter import get_db_adapter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("coin_perks_migration")

DEFAULT_PERKS = [
    {
        "slug": "ai_ats_scanner",
        "title": "AI ATS Resume Screener Pass",
        "description": "Unlock 1 comprehensive AI-powered ATS resume scan, detailed rubric evaluation, and keyword optimization report on /portal/cv/ats-check.",
        "coin_price": 100,
        "category": "career",
        "action_type": "instant_token",
        "badge_label": "Instant Access",
        "icon_class": "fa-solid fa-file-shield",
        "metadata_json": json.dumps({"target_url": "/portal/cv", "scan_credits": 1, "feature": "ats_screener"})
    },
    {
        "slug": "ai_mock_interview",
        "title": "1-on-1 AI Mock Interview Pass",
        "description": "Unlock 1 full-length interactive AI technical mock interview session with domain question generation, response analysis, and scoring rubric.",
        "coin_price": 100,
        "category": "career",
        "action_type": "instant_token",
        "badge_label": "AI Simulator",
        "icon_class": "fa-solid fa-robot",
        "metadata_json": json.dumps({"target_url": "/portal", "sessions": 1, "feature": "ai_mock_interview"})
    },
    {
        "slug": "mentor_session_1on1",
        "title": "1-on-1 Senior Mentor Strategy Session",
        "description": "Book a 30-minute private 1-on-1 strategy, portfolio evaluation, or technical code review session with a senior DBERT industry mentor on /mentors/slots.",
        "coin_price": 500,
        "category": "mentorship",
        "action_type": "slot_credit",
        "badge_label": "Live 1-on-1",
        "icon_class": "fa-solid fa-chalkboard-user",
        "metadata_json": json.dumps({"target_url": "/mentors/slots", "slot_duration_mins": 30, "feature": "mentor_session"})
    },
    {
        "slug": "course_fee_discount",
        "title": "Course Enrollment Fee Discount",
        "description": "Redeem your earned DBERT educational coins for up to a 50% discount on any advanced specialization course track (1 Coin = ₹1 INR direct credit).",
        "coin_price": 1,
        "category": "course",
        "action_type": "discount",
        "badge_label": "Up to 50% Off",
        "icon_class": "fa-solid fa-graduation-cap",
        "metadata_json": json.dumps({"max_discount_percent": 50, "rate_inr_per_coin": 1.0, "target_url": "/courses", "feature": "course_discount"})
    }
]


def run_migration():
    logger.info("Initializing Coin Perks Catalog & Redemptions Migration...")
    conn = get_db_adapter()
    dialect = getattr(conn, "dialect", "sqlite")
    logger.info(f"Connected to database using dialect: {dialect}")

    with conn:
        # 1. Create coin_perks_catalog table
        if dialect == "postgres":
            conn.execute("""
                CREATE TABLE IF NOT EXISTS coin_perks_catalog (
                    id SERIAL PRIMARY KEY,
                    slug VARCHAR(64) UNIQUE NOT NULL,
                    title VARCHAR(128) NOT NULL,
                    description TEXT NOT NULL,
                    coin_price INTEGER NOT NULL CHECK (coin_price > 0),
                    category VARCHAR(32) NOT NULL DEFAULT 'career',
                    action_type VARCHAR(32) NOT NULL DEFAULT 'instant_token',
                    badge_label VARCHAR(64),
                    icon_class VARCHAR(64) DEFAULT 'fa-solid fa-gift',
                    metadata_json TEXT DEFAULT '{}',
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        else:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS coin_perks_catalog (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    coin_price INTEGER NOT NULL CHECK (coin_price > 0),
                    category TEXT NOT NULL DEFAULT 'career',
                    action_type TEXT NOT NULL DEFAULT 'instant_token',
                    badge_label TEXT,
                    icon_class TEXT DEFAULT 'fa-solid fa-gift',
                    metadata_json TEXT DEFAULT '{}',
                    is_active INTEGER DEFAULT 1,
                    created_at TEXT DEFAULT (datetime('now','localtime'))
                );
            """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_coin_perks_active ON coin_perks_catalog(is_active, category);")
        logger.info("Ensured coin_perks_catalog table and indexes.")

        # 2. Create coin_perk_redemptions table
        if dialect == "postgres":
            conn.execute("""
                CREATE TABLE IF NOT EXISTS coin_perk_redemptions (
                    id SERIAL PRIMARY KEY,
                    redemption_code VARCHAR(32) UNIQUE NOT NULL,
                    intern_id INTEGER NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    perk_id INTEGER NOT NULL REFERENCES coin_perks_catalog(id),
                    perk_slug VARCHAR(64) NOT NULL,
                    coins_spent INTEGER NOT NULL,
                    status VARCHAR(32) NOT NULL DEFAULT 'active',
                    voucher_token VARCHAR(64) UNIQUE,
                    details_json TEXT DEFAULT '{}',
                    idem_key VARCHAR(128) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    used_at TIMESTAMP
                );
            """)
        else:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS coin_perk_redemptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    redemption_code TEXT UNIQUE NOT NULL,
                    intern_id INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    perk_id INTEGER NOT NULL REFERENCES coin_perks_catalog(id),
                    perk_slug TEXT NOT NULL,
                    coins_spent INTEGER NOT NULL,
                    status TEXT NOT NULL DEFAULT 'active',
                    voucher_token TEXT UNIQUE,
                    details_json TEXT DEFAULT '{}',
                    idem_key TEXT UNIQUE NOT NULL,
                    created_at TEXT DEFAULT (datetime('now','localtime')),
                    used_at TEXT
                );
            """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_perk_redemptions_intern ON coin_perk_redemptions(intern_id, status);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_perk_redemptions_email ON coin_perk_redemptions(email);")
        logger.info("Ensured coin_perk_redemptions table and indexes.")

        # 3. Seed / Update master perks catalog idempotently
        for perk in DEFAULT_PERKS:
            existing = conn.execute(
                "SELECT id, coin_price FROM coin_perks_catalog WHERE slug = ?",
                (perk["slug"],)
            ).fetchone()

            if existing:
                conn.execute(
                    """
                    UPDATE coin_perks_catalog SET
                        title = ?,
                        description = ?,
                        coin_price = ?,
                        category = ?,
                        action_type = ?,
                        badge_label = ?,
                        icon_class = ?,
                        metadata_json = ?,
                        is_active = 1
                    WHERE slug = ?
                    """,
                    (
                        perk["title"],
                        perk["description"],
                        perk["coin_price"],
                        perk["category"],
                        perk["action_type"],
                        perk["badge_label"],
                        perk["icon_class"],
                        perk["metadata_json"],
                        perk["slug"],
                    )
                )
                logger.info(f"Updated perk [{perk['slug']}] -> Price: {perk['coin_price']} coins")
            else:
                conn.execute(
                    """
                    INSERT INTO coin_perks_catalog (
                        slug, title, description, coin_price, category,
                        action_type, badge_label, icon_class, metadata_json, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """,
                    (
                        perk["slug"],
                        perk["title"],
                        perk["description"],
                        perk["coin_price"],
                        perk["category"],
                        perk["action_type"],
                        perk["badge_label"],
                        perk["icon_class"],
                        perk["metadata_json"],
                    )
                )
                logger.info(f"Inserted new perk [{perk['slug']}] -> Price: {perk['coin_price']} coins")

        conn.commit()

    logger.info("Coin Perks Catalog & Redemptions Migration completed successfully!")


if __name__ == "__main__":
    run_migration()
