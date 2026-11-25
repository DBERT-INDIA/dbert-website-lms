#!/usr/bin/env python3
"""
Extracts 90-100 active enrolled interns from EC2 PostgreSQL who:
  1. Have NOT completed the ₹299 Gate 1 deposit (stipend_verified = 0).
  2. Are NOT on the Pre-Vetted / Verified Directory (directory_candidates.json / certificates_registry.json).
  3. Have logged in recently (within LAST_LOGIN_DAYS, ordered most recent first).
  4. Have NOT been messaged in recent WhatsApp campaigns (fresh first; if < 90, report exact breakdown).

Splits 50/50 into Account 1 and Account 2 queues.
"""

import csv
import json
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
WEBSITE_DATA = PROJECT_ROOT / "apps" / "website" / "src" / "data"
SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
SSH_HOST = "ubuntu@3.26.237.171"

ACC1_QUEUE = DATA_DIR / "whatsapp_gate1_299_acc1.json"
ACC2_QUEUE = DATA_DIR / "whatsapp_gate1_299_acc2.json"
TARGET_TOTAL = 100
RECENT_LOGIN_DAYS = 14


def normalize_phone(raw: str) -> str:
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) == 10 and digits[0] in "6789":
        return "91" + digits
    if len(digits) == 11 and digits.startswith("0") and digits[1] in "6789":
        return "91" + digits[1:]
    if len(digits) == 12 and digits.startswith("91") and digits[2] in "6789":
        return digits
    if len(digits) >= 10:
        return digits[-10:] if len(digits) > 12 else digits
    return ""


def load_prevetted_exclusions() -> tuple[set[str], set[str], set[str]]:
    emails: set[str] = set()
    certs: set[str] = set()
    names: set[str] = set()

    dir_path = WEBSITE_DATA / "directory_candidates.json"
    if dir_path.exists():
        for c in json.loads(dir_path.read_text(encoding="utf-8")):
            if not c.get("isProvisional") or c.get("verified") or (c.get("status") or "").lower() == "verified":
                if c.get("email"):
                    emails.add(c["email"].strip().lower())
                if c.get("certId"):
                    certs.add(c["certId"].strip().upper())
                if c.get("holderName"):
                    names.add(c["holderName"].strip().lower())

    cert_reg = WEBSITE_DATA / "certificates_registry.json"
    if cert_reg.exists():
        reg = json.loads(cert_reg.read_text(encoding="utf-8"))
        for cid, c in reg.items():
            if c.get("verified") is True or not c.get("isProvisional", True):
                certs.add(cid.strip().upper())
                if c.get("email"):
                    emails.add(c["email"].strip().lower())

    return emails, certs, names


def load_previously_contacted() -> tuple[set[str], set[str]]:
    contacted_phones: set[str] = set()
    contacted_emails: set[str] = set()

    db_path = DATA_DIR / "dbert_whatsapp.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(db_path)
            for phone, email in conn.execute("SELECT clean_phone, user_email FROM whatsapp_sent_log"):
                p = normalize_phone(phone or "")
                if p:
                    contacted_phones.add(p)
                if email:
                    contacted_emails.add(email.strip().lower())
            conn.close()
        except Exception as e:
            print(f"[WARN] Could not read whatsapp_sent_log: {e}")

    for json_name in (
        "dbert_whatsapp_sent_today.json",
        "whatsapp_299_queue_acc1.json",
        "whatsapp_299_queue_acc2.json",
        "whatsapp_299_queue_batch35_acc2.json",
    ):
        jp = DATA_DIR / json_name
        if jp.exists():
            try:
                for item in json.loads(jp.read_text(encoding="utf-8")):
                    p = normalize_phone(item.get("phone") or item.get("clean_phone") or "")
                    if p:
                        contacted_phones.add(p)
                    em = (item.get("email") or "").strip().lower()
                    if em:
                        contacted_emails.add(em)
            except Exception as e:
                print(f"[WARN] Could not read {json_name}: {e}")

    for csv_name in (
        "dispatch_tracking_batch35_acc2.csv",
        "dispatch_tracking_stipend_299.csv",
        "dispatch_tracking_resubmit_27.csv",
        "dispatch_tracking_selected_multi_login.csv",
        "dispatch_tracking_gate1_299_nov25.csv",
    ):
        cp = DATA_DIR / csv_name
        if cp.exists():
            try:
                with open(cp, encoding="utf-8", newline="") as f:
                    for row in csv.DictReader(f):
                        if (row.get("status") or "").upper() in ("SENT", "DELIVERED", ""):
                            p = normalize_phone(row.get("clean_phone") or row.get("phone") or "")
                            if p:
                                contacted_phones.add(p)
                            em = (row.get("email") or "").strip().lower()
                            if em:
                                contacted_emails.add(em)
            except Exception as e:
                print(f"[WARN] Could not read {csv_name}: {e}")

    return contacted_phones, contacted_emails


def fetch_ec2_enrolled_unverified() -> list[dict]:
    sql = """
    SET search_path TO dbert_internship, public;
    WITH latest_sessions AS (
        SELECT LOWER(email) AS em, MAX(created_at) AS last_login
        FROM user_sessions
        GROUP BY LOWER(email)
    ),
    latest_certs AS (
        SELECT DISTINCT ON (LOWER(email)) LOWER(email) AS em, cert_id, COALESCE(tier, '') AS tier
        FROM intern_certificates
        WHERE cert_id IS NOT NULL AND TRIM(cert_id) != ''
        ORDER BY LOWER(email), id DESC
    ),
    latest_enrollments AS (
        SELECT DISTINCT ON (LOWER(email)) LOWER(email) AS em, id AS enrollment_id, created_at AS enrolled_at
        FROM enrollments
        ORDER BY LOWER(email), id DESC
    )
    SELECT json_agg(row_to_json(t))
    FROM (
        SELECT
            ia.id AS candidate_id,
            COALESCE(NULLIF(TRIM(ia.name), ''), 'Intern') AS name,
            LOWER(TRIM(ia.email)) AS email,
            TRIM(ia.phone) AS raw_phone,
            COALESCE(NULLIF(TRIM(ia.domain), ''), 'Engineering') AS domain,
            COALESCE(lc.cert_id, '') AS cert_id,
            COALESCE(lc.tier, '') AS cert_tier,
            COALESCE(ls.last_login, '') AS last_login,
            COALESCE(le.enrolled_at::text, '') AS enrolled_at
        FROM intern_accounts ia
        JOIN latest_enrollments le ON le.em = LOWER(ia.email)
        JOIN latest_sessions ls ON ls.em = LOWER(ia.email)
        LEFT JOIN latest_certs lc ON lc.em = LOWER(ia.email)
        WHERE ia.is_active = 1
          AND COALESCE(ia.stipend_verified, 0) = 0
          AND COALESCE(lc.tier, '') != 'verified'
          AND ia.phone IS NOT NULL
          AND length(trim(ia.phone)) >= 10
        ORDER BY ls.last_login DESC, le.enrolled_at DESC, ia.id DESC
    ) t;
    """
    cmd = [
        "ssh",
        "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        SSH_HOST,
        f"sudo -u postgres psql -d dbert_lms -t -A -c \"{sql.replace(chr(10), ' ')}\"",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if res.returncode != 0:
        raise RuntimeError(f"EC2 query failed: {res.stderr}")

    lines = [ln.strip() for ln in res.stdout.splitlines() if ln.strip() and ln.strip() != "SET"]
    if not lines:
        return []
    return json.loads(lines[-1]) or []


def main():
    rows = fetch_ec2_enrolled_unverified()
    pv_emails, pv_certs, pv_names = load_prevetted_exclusions()
    contacted_phones, contacted_emails = load_previously_contacted()

    cutoff_14d = (datetime.now() - timedelta(days=RECENT_LOGIN_DAYS)).strftime("%Y-%m-%d")

    seen_phones: set[str] = set()
    seen_emails: set[str] = set()
    excluded_prevetted = 0
    excluded_older_login = 0
    fresh_recent: list[dict] = []
    prior_recent: list[dict] = []

    for r in rows:
        clean_phone = normalize_phone(r.get("raw_phone") or "")
        email = (r.get("email") or "").strip().lower()
        cert_id = (r.get("cert_id") or "").strip().upper()
        name_l = (r.get("name") or "").strip().lower()
        last_login = r.get("last_login") or ""

        if not clean_phone or len(clean_phone) < 10:
            continue
        if clean_phone in seen_phones or (email and email in seen_emails):
            continue

        # Exclude Pre-Vetted / Verified directory members
        if email in pv_emails or (cert_id and cert_id in pv_certs) or name_l in pv_names:
            excluded_prevetted += 1
            continue

        # Enforce recent login window (last 14 days)
        if last_login[:10] < cutoff_14d:
            excluded_older_login += 1
            continue

        seen_phones.add(clean_phone)
        if email:
            seen_emails.add(email)

        entry = {
            "candidate_id": r["candidate_id"],
            "name": r["name"],
            "email": email,
            "clean_phone": clean_phone,
            "domain": r["domain"],
            "cert_id": r.get("cert_id") or "",
            "last_login": last_login,
            "enrolled_at": r["enrolled_at"],
        }

        if clean_phone in contacted_phones or email in contacted_emails:
            entry["tier"] = "TOPUP_RECENT"
            prior_recent.append(entry)
        else:
            entry["tier"] = "FRESH_RECENT"
            fresh_recent.append(entry)

    print(f"EC2 enrolled unverified with login sessions: {len(rows)}")
    print(f"Excluded Pre-Vetted / Verified: {excluded_prevetted}")
    print(f"Excluded login older than {RECENT_LOGIN_DAYS} days (< {cutoff_14d}): {excluded_older_login}")
    print(f"Eligible logged in >= {cutoff_14d}: Fresh={len(fresh_recent)}, PriorContacted={len(prior_recent)}")

    selected = fresh_recent[:TARGET_TOTAL]
    if len(selected) < TARGET_TOTAL:
        selected.extend(prior_recent[: TARGET_TOTAL - len(selected)])

    acc1: list[dict] = []
    acc2: list[dict] = []
    for idx, item in enumerate(selected, start=1):
        item["serial_no"] = idx
        if idx % 2 == 1:
            acc1.append(item)
        else:
            acc2.append(item)

    ACC1_QUEUE.write_text(json.dumps(acc1, indent=2, ensure_ascii=False), encoding="utf-8")
    ACC2_QUEUE.write_text(json.dumps(acc2, indent=2, ensure_ascii=False), encoding="utf-8")

    fresh_cnt = sum(1 for x in selected if x["tier"] == "FRESH_RECENT")
    topup_cnt = sum(1 for x in selected if x["tier"] == "TOPUP_RECENT")
    print(f"Final Queue Selected: {len(selected)} (Fresh={fresh_cnt}, TopUp={topup_cnt})")
    print(f"  Account 1: {len(acc1)} -> {ACC1_QUEUE}")
    print(f"  Account 2: {len(acc2)} -> {ACC2_QUEUE}")


if __name__ == "__main__":
    main()
