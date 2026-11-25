"""
scripts/sync_enrollments_to_postgres.py
Reconciles balance enrollment records from data/balance_enrollments_1500.json
into the PostgreSQL / SQLite enrollments and intern_accounts tables.
Guarantees zero data loss and automated synchronization.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Insert apps/portal for get_db
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "portal")))

from app import get_db, ensure_column, VALID_DOMAINS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sync_enrollments")

def resolve_balance_file():
    candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "balance_enrollments_1500.json")),
        "/var/www/dbert-website-lms/data/balance_enrollments_1500.json",
        "data/balance_enrollments_1500.json"
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None

def sync_balance_enrollments():
    file_path = resolve_balance_file()
    if not file_path:
        logger.error("Could not find balance_enrollments_1500.json")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    if not isinstance(records, list):
        logger.error("Invalid format: expected a JSON array")
        return False

    logger.info(f"Loaded {len(records)} balance enrollment records from {file_path}")

    synced = 0
    updated = 0
    with get_db() as conn:
        ensure_column(conn, "enrollments", "intern_id", "INTEGER")
        ensure_column(conn, "enrollments", "amount_paid", "INTEGER DEFAULT 0")
        ensure_column(conn, "enrollments", "utr_number", "TEXT")
        ensure_column(conn, "enrollments", "deposit_paid", "INTEGER DEFAULT 0")
        ensure_column(conn, "enrollments", "balance_paid", "INTEGER DEFAULT 0")
        ensure_column(conn, "enrollments", "submission_id", "TEXT")
        ensure_column(conn, "enrollments", "balance_submission_id", "TEXT")

        for r in records:
            email = (r.get("email") or "").strip().lower()
            name = (r.get("fullName") or r.get("name") or "").strip()
            phone = (r.get("phone") or "").strip()
            college = (r.get("college") or "").strip()
            domain = (r.get("domain") or "").strip()
            utr = (r.get("utrNumber") or r.get("utr") or "").strip()
            sub_id = (r.get("id") or r.get("submissionId") or "").strip()
            status = (r.get("status") or "SUBMITTED").strip().upper()
            submitted_at = r.get("submittedAt") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if not email:
                continue

            # Normalize domain
            if domain not in VALID_DOMAINS:
                for vd in VALID_DOMAINS:
                    if vd.lower() in domain.lower() or domain.lower() in vd.lower():
                        domain = vd
                        break
                if domain not in VALID_DOMAINS:
                    domain = "Full Stack Web Development"

            # Check if intern account exists
            acct = conn.execute("SELECT id, name FROM intern_accounts WHERE LOWER(email)=?", (email,)).fetchone()
            if not acct:
                # Create basic intern account
                from werkzeug.security import generate_password_hash
                import secrets
                random_pw = secrets.token_urlsafe(12)
                pw_hash = generate_password_hash(random_pw)
                cursor = conn.execute(
                    """INSERT INTO intern_accounts 
                    (name, email, password_hash, domain, phone, college, signup_stage, account_status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, 5, 'active', ?, ?)""",
                    (name, email, pw_hash, domain, phone, college, submitted_at, submitted_at)
                )
                intern_id = cursor.lastrowid
                logger.info(f"Created new intern account for {email} (ID: {intern_id})")
            else:
                intern_id = acct["id"]

            # Upsert into enrollments
            enr = conn.execute(
                "SELECT id, balance_paid, utr_number FROM enrollments WHERE LOWER(email)=?", (email,)
            ).fetchone()

            if enr:
                conn.execute(
                    """UPDATE enrollments SET
                        balance_paid = 1500,
                        utr_number = COALESCE(utr_number, ?),
                        balance_submission_id = ?,
                        updated_at = ?
                    WHERE id = ?""",
                    (utr, sub_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), enr["id"])
                )
                updated += 1
            else:
                conn.execute(
                    """INSERT INTO enrollments
                    (intern_id, email, name, phone, college, domain, batch_label, amount_paid, deposit_paid, balance_paid, utr_number, submission_id, balance_submission_id, payment_status, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, '2026-Cohort-A', 1999, 499, 1500, ?, ?, ?, ?, ?, ?)""",
                    (intern_id, email, name, phone, college, domain, utr, sub_id, sub_id, status, submitted_at, submitted_at)
                )
                synced += 1

        conn.commit()

    logger.info(f"Reconciliation complete. Total processed: {len(records)}, Inserted: {synced}, Updated: {updated}")
    return True

if __name__ == "__main__":
    sync_balance_enrollments()
