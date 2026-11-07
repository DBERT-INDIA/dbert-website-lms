"""
scripts/sync_verified_certificates_to_portal.py
Synchronizes all officially VERIFIED candidates from certificates_registry.json
into the LMS intern_certificates table (SQLite / PostgreSQL).
"""
import sys
import os
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "portal")))

from services.certificate_service import CertificateService

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sync_verified")

def sync_verified():
    path = CertificateService.resolve_registry_path()
    if not path or not os.path.isfile(path):
        logger.error(f"Cannot resolve certificates_registry.json at {path}")
        return False

    with open(path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    if isinstance(registry, dict):
        records = registry.values()
    else:
        records = registry

    logger.info(f"Loaded {len(records)} records from {path}")

    # Import get_db from app
    try:
        from app import get_db
    except ImportError:
        logger.error("Could not import get_db from app")
        return False

    verified_count = 0
    synced_count = 0
    skipped_count = 0

    with get_db() as conn:
        for rec in records:
            if not isinstance(rec, dict):
                continue

            cert_id = rec.get("certId", "")
            is_prov = bool(rec.get("isProvisional", False))
            is_ver = bool(rec.get("verified", False) and not is_prov)
            email = (rec.get("email") or "").strip().lower()
            domain = rec.get("domain", "Internship Certificate")
            issue_date = rec.get("issueDate", "2026-10-01")

            if not is_ver or not email:
                continue

            verified_count += 1

            # Check if intern account exists
            acct = conn.execute("SELECT id FROM intern_accounts WHERE LOWER(email) = LOWER(?)", (email,)).fetchone()
            intern_id = acct["id"] if acct else 0

            # Check existing cert
            existing = conn.execute(
                "SELECT id FROM intern_certificates WHERE LOWER(cert_id) = LOWER(?) OR (LOWER(email) = LOWER(?) AND tier = 'verified')",
                (cert_id, email)
            ).fetchone()

            if existing:
                skipped_count += 1
                continue

            conn.execute(
                """
                INSERT INTO intern_certificates 
                (intern_id, course_id, course_title, cert_id, issued_at, url, tier, email)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (intern_id, 0, domain, cert_id, issue_date, f"/verify/{cert_id}", "verified", email)
            )
            synced_count += 1

        conn.commit()

    logger.info(f"Sync complete. Verified candidates found: {verified_count}. Newly synced: {synced_count}. Already present: {skipped_count}.")
    return True

if __name__ == "__main__":
    success = sync_verified()
    sys.exit(0 if success else 1)
