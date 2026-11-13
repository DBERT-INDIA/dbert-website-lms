#!/usr/bin/env python3
"""
================================================================================
DBERT — Dual-Account WhatsApp Candidate Credential Dispatcher
================================================================================
Purpose:
  Dispatches official, personalized WhatsApp credential notices to candidates
  from the DBERT provisional registry (data/all_409_provisional_registry.json).

Dual-Account Architecture:
  - Account 1 (Odd Serials):  .chrome_session_account1 (46 candidates per batch)
  - Account 2 (Even Serials): .chrome_session_account2 (46 candidates per batch)
  - Anti-Ban Pacing: 18s–35s randomized human delay between messages.
  - Circuit Breaker: Pauses worker if 3 consecutive failures occur.
  - Session Persistence: Reuses authenticated profiles (default Desktop/aivara/aivara).
  - Permanent History: whatsapp_sent_log ensures candidates are never re-messaged.
  - Cross-Channel Sync: Merges email & WhatsApp tracking into unified CSV.
================================================================================
"""

import os
import sys
import re
import csv
import time
import json
import random
import sqlite3
import argparse
import urllib.parse
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Paths and Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

REGISTRY_PATH = DATA_DIR / "all_409_provisional_registry.json"
EMAIL_TRACKING_PATH = DATA_DIR / "dispatch_tracking_409.json"
DB_PATH = DATA_DIR / "dbert_whatsapp.db"

# Session directories from existing authenticated Chrome profiles
AIVARA_SESSIONS_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
LOCAL_SESSIONS_DIR = PROJECT_ROOT

SESSION_ACC1 = (
    AIVARA_SESSIONS_DIR / ".chrome_session_account1"
    if (AIVARA_SESSIONS_DIR / ".chrome_session_account1").exists()
    else LOCAL_SESSIONS_DIR / ".chrome_session_account1"
)

SESSION_ACC2 = (
    AIVARA_SESSIONS_DIR / ".chrome_session_account2"
    if (AIVARA_SESSIONS_DIR / ".chrome_session_account2").exists()
    else LOCAL_SESSIONS_DIR / ".chrome_session_account2"
)

MAX_MESSAGES_PER_ACCOUNT = 46
TOTAL_TARGET_CANDIDATES = MAX_MESSAGES_PER_ACCOUNT * 2  # 92
MAX_CONSECUTIVE_WA_FAILURES = 3

GOOGLE_FORM_URL = (
    "https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"
)


def clean_phone_number(raw_phone) -> str:
    """Normalize phone number to 12 digits with 91 country code for Indian numbers."""
    if not raw_phone:
        return ""
    digits = re.sub(r"\D", "", str(raw_phone))
    if digits.startswith("91") and len(digits) == 12:
        return digits
    if len(digits) == 10:
        return "91" + digits
    if digits.startswith("0") and len(digits) == 11:
        return "91" + digits[1:]
    return digits


def parse_timestamp_to_dt(ts_str: str) -> datetime:
    """Parses various date/time formats encountered across sheet exports."""
    if not ts_str:
        return datetime.min
    ts_str = str(ts_str).strip()
    formats = (
        "%m/%d/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
    )
    for fmt in formats:
        try:
            return datetime.strptime(ts_str, fmt)
        except ValueError:
            pass
    return datetime.min


def build_candidate_timestamp_map() -> dict[str, tuple[datetime, str]]:
    """
    Builds a lookup map: (clean_email, phone_10_digit) -> (datetime, raw_timestamp_str).
    Scans master enrollment and sheet CSVs so candidates can be sorted latest-first.
    """
    ts_map = {}

    # 1. Master enrolled interns detailed CSV
    master_csv = PROJECT_ROOT / "all_enrolled_interns_master_detailed.csv"
    if master_csv.exists():
        try:
            with open(master_csv, "r", encoding="utf-8-sig", errors="ignore") as f:
                for row in csv.DictReader(f):
                    raw_ts = (row.get("Latest_Registration_Timestamp") or row.get("Earliest_Registration_Timestamp") or "").strip()
                    if not raw_ts:
                        continue
                    dt = parse_timestamp_to_dt(raw_ts)
                    em = (row.get("Email") or "").strip().lower()
                    ph = re.sub(r"\D", "", row.get("WhatsApp_Number") or row.get("Mobile_10_Digit") or "")[-10:]
                    if em:
                        ts_map[f"em:{em}"] = (dt, raw_ts)
                    if ph:
                        ts_map[f"ph:{ph}"] = (dt, raw_ts)
        except Exception as e:
            print(f"[WARN] Failed indexing {master_csv}: {e}")

    # 2. Check grand total pending candidates CSV
    pending_csv = DATA_DIR / "grand_total_pending_candidates.csv"
    if pending_csv.exists():
        try:
            with open(pending_csv, "r", encoding="utf-8", errors="ignore") as f:
                for row in csv.DictReader(f):
                    raw_ts = (row.get("timestamp") or "").strip()
                    if not raw_ts:
                        continue
                    dt = parse_timestamp_to_dt(raw_ts)
                    em = (row.get("email") or "").strip().lower()
                    ph = re.sub(r"\D", "", row.get("phone") or "")[-10:]
                    if em and f"em:{em}" not in ts_map:
                        ts_map[f"em:{em}"] = (dt, raw_ts)
                    if ph and f"ph:{ph}" not in ts_map:
                        ts_map[f"ph:{ph}"] = (dt, raw_ts)
        except Exception as e:
            print(f"[WARN] Failed indexing {pending_csv}: {e}")

    # 3. Check Google Sheet CSVs in project root
    for s_name in ("sheet_data.csv", "second_sheet.csv", "aug_oct_sheet.csv"):
        s_path = PROJECT_ROOT / s_name
        if s_path.exists():
            try:
                with open(s_path, "r", encoding="utf-8", errors="ignore") as f:
                    for row in csv.DictReader(f):
                        raw_ts = (row.get("Timestamp") or row.get("timestamp") or "").strip()
                        if not raw_ts:
                            continue
                        dt = parse_timestamp_to_dt(raw_ts)
                        em = (row.get("Email Address") or row.get("Email") or row.get("email") or "").strip().lower()
                        ph = re.sub(r"\D", "", row.get("WhatsApp number ") or row.get("Phone") or row.get("phone") or "")[-10:]
                        if em and f"em:{em}" not in ts_map:
                            ts_map[f"em:{em}"] = (dt, raw_ts)
                        if ph and f"ph:{ph}" not in ts_map:
                            ts_map[f"ph:{ph}"] = (dt, raw_ts)
            except Exception as e:
                print(f"[WARN] Failed indexing {s_path}: {e}")

    return ts_map


# ---------------------------------------------------------------------------
# Database & Queue Management
# ---------------------------------------------------------------------------
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def init_db():
    conn = get_db_connection()
    # Active queue table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS whatsapp_dispatch (
            serial_no        INTEGER PRIMARY KEY,
            candidate_id     TEXT NOT NULL,
            holder_name      TEXT NOT NULL,
            user_email       TEXT NOT NULL,
            clean_phone      TEXT NOT NULL,
            raw_phone        TEXT,
            domain_track     TEXT,
            core_project     TEXT,
            cert_id          TEXT NOT NULL,
            score            INTEGER,
            grade            TEXT,
            verification_url TEXT NOT NULL,
            signup_timestamp TEXT,
            account_group    TEXT NOT NULL,
            whatsapp_status  TEXT DEFAULT 'PENDING',
            whatsapp_sent_at TEXT,
            whatsapp_error   TEXT
        )
    """)
    # Migration if table already existed without signup_timestamp
    try:
        conn.execute("ALTER TABLE whatsapp_dispatch ADD COLUMN signup_timestamp TEXT")
        conn.commit()
    except Exception:
        pass

    # Permanent sent history log (persists across runs and batches)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS whatsapp_sent_log (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id     TEXT UNIQUE NOT NULL,
            holder_name      TEXT NOT NULL,
            user_email       TEXT NOT NULL,
            clean_phone      TEXT NOT NULL,
            cert_id          TEXT NOT NULL,
            domain_track     TEXT,
            account_group    TEXT NOT NULL,
            whatsapp_sent_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def load_registry_candidates() -> list[dict]:
    """Loads all candidates from all_409_provisional_registry.json."""
    if not REGISTRY_PATH.exists():
        print(f"[ERROR] Registry file not found: {REGISTRY_PATH}")
        return []
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_next_batch(batch_size: int = TOTAL_TARGET_CANDIDATES):
    """
    Loads the next batch of uncontacted candidates from the 409 registry.
    Preserves all previously SENT candidates in whatsapp_sent_log.
    Splits into odd (Account 1) and even (Account 2) queues.
    """
    init_db()
    conn = get_db_connection()

    # 1. Sync any existing SENT records in whatsapp_dispatch into whatsapp_sent_log
    sent_in_dispatch = conn.execute("""
        SELECT candidate_id, holder_name, user_email, clean_phone, cert_id, domain_track, account_group, whatsapp_sent_at
        FROM whatsapp_dispatch
        WHERE whatsapp_status = 'SENT'
    """).fetchall()

    for r in sent_in_dispatch:
        now_ts = r["whatsapp_sent_at"] or datetime.now().isoformat()
        conn.execute("""
            INSERT OR IGNORE INTO whatsapp_sent_log
            (candidate_id, holder_name, user_email, clean_phone, cert_id, domain_track, account_group, whatsapp_sent_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["candidate_id"], r["holder_name"], r["user_email"], r["clean_phone"], r["cert_id"], r["domain_track"], r["account_group"], now_ts))
    conn.commit()

    # 2. Get list of already sent candidate identifiers
    sent_rows = conn.execute("SELECT candidate_id, user_email, clean_phone, cert_id FROM whatsapp_sent_log").fetchall()
    sent_ids = set((r["candidate_id"] or "").strip() for r in sent_rows if r["candidate_id"])
    sent_emails = set((r["user_email"] or "").strip().lower() for r in sent_rows if r["user_email"])
    sent_phones = set((r["clean_phone"] or "").strip() for r in sent_rows if r["clean_phone"])
    sent_certs = set((r["cert_id"] or "").strip() for r in sent_rows if r["cert_id"])

    sent_phones_10 = set(p[-10:] for p in sent_phones if len(p) >= 10)

    # 3. Fetch all candidates from all_409_provisional_registry.json
    all_candidates = load_registry_candidates()
    ts_map = build_candidate_timestamp_map()

    # Annotate candidates with registration timestamp and datetime
    for cand in all_candidates:
        clean_email = (cand.get("email") or "").strip().lower()
        clean_phone = clean_phone_number(cand.get("phone", ""))
        p10 = clean_phone[-10:] if len(clean_phone) >= 10 else ""

        entry = ts_map.get(f"em:{clean_email}") or (ts_map.get(f"ph:{p10}") if p10 else None)
        if entry:
            cand["signup_dt"] = entry[0]
            cand["signup_timestamp"] = entry[1]
        else:
            cand_date = cand.get("startDate") or cand.get("issueDate") or ""
            cand["signup_dt"] = parse_timestamp_to_dt(cand_date)
            cand["signup_timestamp"] = cand_date

    # Sort all candidates descending: latest signups first
    all_candidates.sort(key=lambda c: c.get("signup_dt", datetime.min), reverse=True)

    # Filter uncontacted candidates (maintains reverse-chronological order)
    uncontacted = []
    seen_phones = set(sent_phones)
    seen_phones_10 = set(sent_phones_10)
    seen_emails = set(sent_emails)
    seen_certs = set(sent_certs)

    for cand in all_candidates:
        c_id = cand.get("internId") or cand.get("certId") or ""
        clean_phone = clean_phone_number(cand.get("phone", ""))
        clean_email = (cand.get("email") or "").strip().lower()
        cert_id = (cand.get("certId") or "").strip()
        p10 = clean_phone[-10:] if len(clean_phone) >= 10 else ""

        if c_id in sent_ids or cert_id in sent_certs or clean_email in sent_emails:
            continue
        if clean_phone in sent_phones or (p10 and p10 in sent_phones_10):
            continue
        if not clean_phone or len(clean_phone) < 10:
            continue
        if clean_phone in seen_phones or (p10 and p10 in seen_phones_10) or clean_email in seen_emails or cert_id in seen_certs:
            continue

        seen_phones.add(clean_phone)
        if p10:
            seen_phones_10.add(p10)
        seen_emails.add(clean_email)
        seen_certs.add(cert_id)
        uncontacted.append(cand)

    # Batch top N (default 92, capped at 46 per account)
    eligible_batch = uncontacted[:batch_size]

    # 4. Clear active dispatch queue and insert the new batch
    conn.execute("DELETE FROM whatsapp_dispatch")
    conn.commit()

    serial_no = 1
    for cand in eligible_batch:
        c_id = cand.get("internId") or cand.get("certId") or f"DBERT-INT-{serial_no}"
        name = (cand.get("holderName") or "Candidate").strip()
        email = (cand.get("email") or "").strip().lower()
        clean_phone = clean_phone_number(cand.get("phone", ""))
        domain = cand.get("domain") or "Applied AI Engineering"
        project = cand.get("project") or "Production Incubation System"
        cert_id = cand.get("certId") or ""
        score = cand.get("score") or 85
        grade = cand.get("grade") or "Grade A (Very Good)"
        verify_url = cand.get("verificationUrl") or f"https://dbert.in/verify?certid={cert_id}"
        signup_ts = cand.get("signup_timestamp") or ""

        account_group = "account1_odd" if (serial_no % 2 != 0) else "account2_even"

        conn.execute("""
            INSERT OR REPLACE INTO whatsapp_dispatch
            (serial_no, candidate_id, holder_name, user_email, clean_phone, raw_phone, domain_track, core_project, cert_id, score, grade, verification_url, signup_timestamp, account_group, whatsapp_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
        """, (serial_no, c_id, name, email, clean_phone, cand.get("phone"), domain, project, cert_id, score, grade, verify_url, signup_ts, account_group))
        serial_no += 1

    conn.commit()
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")

    acc1_count = conn.execute("SELECT count(*) as c FROM whatsapp_dispatch WHERE account_group = 'account1_odd'").fetchone()["c"]
    acc2_count = conn.execute("SELECT count(*) as c FROM whatsapp_dispatch WHERE account_group = 'account2_even'").fetchone()["c"]
    total_sent_so_far = len(sent_rows)
    total_candidates = len(all_candidates)
    remaining_uncontacted = max(0, len(uncontacted) - len(eligible_batch))

    conn.close()
    export_queues_csv()

    print("\n" + "=" * 76)
    print("  DBERT — NEXT BATCH LOADED INTO WHATSAPP DISPATCH QUEUE (LATEST FIRST)")
    print("=" * 76)
    print(f"  Total Candidates in Registry       : {total_candidates}")
    print(f"  Successfully Sent in Prior Runs    : {total_sent_so_far} candidates (Excluded)")
    print(f"  Queued for This Run (Latest First) : {len(eligible_batch)} candidates")
    print(f"    - Account 1 (Odd Serials)        : {acc1_count} candidates (Capped at {MAX_MESSAGES_PER_ACCOUNT})")
    print(f"    - Account 2 (Even Serials)       : {acc2_count} candidates (Capped at {MAX_MESSAGES_PER_ACCOUNT})")
    print(f"  Remaining After This Run           : {remaining_uncontacted} candidates")
    print("=" * 76)

    if eligible_batch:
        print("\nFirst 3 candidates in queue (Latest Signups):")
        for cand in eligible_batch[:3]:
            ts_display = cand.get("signup_timestamp") or "N/A"
            print(f"  - [{ts_display}] {cand.get('holderName')} | {cand.get('certId')} | +{clean_phone_number(cand.get('phone'))} | {cand.get('domain')}")
        print()


def load_sheet_1593_first_92(batch_size: int = 92):
    """
    Loads the first 92 uncontacted candidates from data/sheet_1593_provisional_registry.json.
    Splits them evenly:
      - Account 1 (Odd Serials): 46 candidates (account1_odd)
      - Account 2 (Even Serials): 46 candidates (account2_even)
    Populates whatsapp_dispatch in dbert_whatsapp.db and exports CSVs.
    """
    init_db()
    conn = get_db_connection()

    # 1. Sync any existing SENT records in whatsapp_dispatch into whatsapp_sent_log
    sent_in_dispatch = conn.execute("""
        SELECT candidate_id, holder_name, user_email, clean_phone, cert_id, domain_track, account_group, whatsapp_sent_at
        FROM whatsapp_dispatch
        WHERE whatsapp_status = 'SENT'
    """).fetchall()

    for r in sent_in_dispatch:
        now_ts = r["whatsapp_sent_at"] or datetime.now().isoformat()
        conn.execute("""
            INSERT OR IGNORE INTO whatsapp_sent_log
            (candidate_id, holder_name, user_email, clean_phone, cert_id, domain_track, account_group, whatsapp_sent_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["candidate_id"], r["holder_name"], r["user_email"], r["clean_phone"], r["cert_id"], r["domain_track"], r["account_group"], now_ts))
    conn.commit()

    # 2. Get list of already sent candidate identifiers
    sent_rows = conn.execute("SELECT candidate_id, user_email, clean_phone, cert_id FROM whatsapp_sent_log").fetchall()
    sent_ids = set((r["candidate_id"] or "").strip() for r in sent_rows if r["candidate_id"])
    sent_emails = set((r["user_email"] or "").strip().lower() for r in sent_rows if r["user_email"])
    sent_phones = set((r["clean_phone"] or "").strip() for r in sent_rows if r["clean_phone"])
    sent_certs = set((r["cert_id"] or "").strip() for r in sent_rows if r["cert_id"])
    sent_phones_10 = set(p[-10:] for p in sent_phones if len(p) >= 10)

    # 3. Load sheet 1593 registry
    sheet_path = DATA_DIR / "sheet_1593_provisional_registry.json"
    if not sheet_path.exists():
        print(f"[ERROR] Sheet registry not found: {sheet_path}")
        conn.close()
        return

    with open(sheet_path, "r", encoding="utf-8") as f:
        all_sheet = json.load(f)

    uncontacted = []
    seen_phones = set(sent_phones)
    seen_phones_10 = set(sent_phones_10)
    seen_emails = set(sent_emails)
    seen_certs = set(sent_certs)

    for cand in all_sheet:
        c_id = cand.get("internId") or cand.get("certId") or ""
        clean_phone = clean_phone_number(cand.get("phone", ""))
        clean_email = (cand.get("email") or "").strip().lower()
        cert_id = (cand.get("certId") or "").strip()
        p10 = clean_phone[-10:] if len(clean_phone) >= 10 else ""

        if c_id in sent_ids or cert_id in sent_certs or clean_email in sent_emails:
            continue
        if clean_phone in sent_phones or (p10 and p10 in sent_phones_10):
            continue
        if not clean_phone or len(clean_phone) < 10:
            continue
        if clean_phone in seen_phones or (p10 and p10 in seen_phones_10) or clean_email in seen_emails or cert_id in seen_certs:
            continue

        seen_phones.add(clean_phone)
        if p10:
            seen_phones_10.add(p10)
        seen_emails.add(clean_email)
        seen_certs.add(cert_id)
        uncontacted.append(cand)

        if len(uncontacted) >= batch_size:
            break

    eligible_batch = uncontacted[:batch_size]

    # 4. Clear active dispatch queue and insert the new batch
    conn.execute("DELETE FROM whatsapp_dispatch")
    conn.commit()

    serial_no = 1
    for cand in eligible_batch:
        c_id = cand.get("internId") or cand.get("certId") or f"DBERT-INT-{serial_no}"
        name = (cand.get("holderName") or "Candidate").strip()
        email = (cand.get("email") or "").strip().lower()
        clean_phone = clean_phone_number(cand.get("phone", ""))
        domain = cand.get("domain") or "Technical Track"
        project = cand.get("project") or "Capstone Incubation Development"
        cert_id = cand.get("certId") or ""
        score = cand.get("score") or 88
        grade = cand.get("grade") or "Grade A (Very Good)"
        verify_url = cand.get("verificationUrl") or f"https://dbert.in/verify?certid={cert_id}"
        signup_ts = cand.get("signup_timestamp") or cand.get("batch") or ""

        account_group = "account1_odd" if (serial_no % 2 != 0) else "account2_even"

        conn.execute("""
            INSERT OR REPLACE INTO whatsapp_dispatch
            (serial_no, candidate_id, holder_name, user_email, clean_phone, raw_phone, domain_track, core_project, cert_id, score, grade, verification_url, signup_timestamp, account_group, whatsapp_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
        """, (serial_no, c_id, name, email, clean_phone, cand.get("phone"), domain, project, cert_id, score, grade, verify_url, signup_ts, account_group))
        serial_no += 1

    conn.commit()
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")

    acc1_count = conn.execute("SELECT count(*) as c FROM whatsapp_dispatch WHERE account_group = 'account1_odd'").fetchone()["c"]
    acc2_count = conn.execute("SELECT count(*) as c FROM whatsapp_dispatch WHERE account_group = 'account2_even'").fetchone()["c"]
    total_sent_so_far = len(sent_rows)

    conn.close()
    export_queues_csv()

    print("\n" + "=" * 76)
    print("  DBERT — SHEET 1593: FIRST 92 CANDIDATES LOADED FOR DUAL WHATSAPP DISPATCH")
    print("=" * 76)
    print(f"  Queued for This Run                : {len(eligible_batch)} candidates")
    print(f"    - Account 1 (Odd Serials)        : {acc1_count} candidates (Capped at {MAX_MESSAGES_PER_ACCOUNT})")
    print(f"    - Account 2 (Even Serials)       : {acc2_count} candidates (Capped at {MAX_MESSAGES_PER_ACCOUNT})")
    print(f"  Total Sent in Prior Runs           : {total_sent_so_far} candidates (Excluded)")
    print("=" * 76)

    if eligible_batch:
        print("\nFirst 3 candidates in queue:")
        for cand in eligible_batch[:3]:
            print(f"  - {cand.get('holderName')} | {cand.get('certId')} | +{clean_phone_number(cand.get('phone'))} | {cand.get('domain')}")
        print()


def export_queues_csv():
    """Exports master and per-account dispatch CSVs for operator tracking."""
    conn = get_db_connection()
    rows = [dict(r) for r in conn.execute("SELECT * FROM whatsapp_dispatch ORDER BY serial_no ASC").fetchall()]
    conn.close()

    master_csv = DATA_DIR / "dbert_whatsapp_master.csv"
    acc1_csv = DATA_DIR / "dbert_whatsapp_acc1.csv"
    acc2_csv = DATA_DIR / "dbert_whatsapp_acc2.csv"

    headers = [
        "serial_no", "candidate_id", "holder_name", "user_email", "clean_phone", "raw_phone",
        "domain_track", "core_project", "cert_id", "score", "grade", "verification_url",
        "signup_timestamp", "account_group", "whatsapp_status", "whatsapp_sent_at", "whatsapp_error"
    ]

    with open(master_csv, "w", newline="", encoding="utf-8-sig") as fm, \
         open(acc1_csv, "w", newline="", encoding="utf-8-sig") as f1, \
         open(acc2_csv, "w", newline="", encoding="utf-8-sig") as f2:

        wm = csv.DictWriter(fm, fieldnames=headers)
        w1 = csv.DictWriter(f1, fieldnames=headers)
        w2 = csv.DictWriter(f2, fieldnames=headers)

        wm.writeheader(); w1.writeheader(); w2.writeheader()

        for r in rows:
            wm.writerow(r)
            if r["account_group"] == "account1_odd":
                w1.writerow(r)
            else:
                w2.writerow(r)


def reset_failed_to_pending():
    """Resets all FAILED records in the active queue back to PENDING."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE whatsapp_dispatch SET whatsapp_status = 'PENDING', whatsapp_error = NULL WHERE whatsapp_status = 'FAILED'")
    count = c.rowcount
    conn.commit()
    conn.close()
    print(f"\n[OK] Reset {count} FAILED records back to PENDING.")
    export_queues_csv()


def print_overall_status():
    """Prints comprehensive campaign telemetry and uncontacted pool status."""
    init_db()
    conn = get_db_connection()

    all_candidates = load_registry_candidates()
    total_candidates = len(all_candidates)

    total_sent_log = conn.execute("SELECT count(*) as c FROM whatsapp_sent_log").fetchone()["c"]
    dispatch_pending = conn.execute("SELECT count(*) as c FROM whatsapp_dispatch WHERE whatsapp_status = 'PENDING'").fetchone()["c"]
    dispatch_sent = conn.execute("SELECT count(*) as c FROM whatsapp_dispatch WHERE whatsapp_status = 'SENT'").fetchone()["c"]
    dispatch_failed = conn.execute("SELECT count(*) as c FROM whatsapp_dispatch WHERE whatsapp_status = 'FAILED'").fetchone()["c"]

    sent_certs = set(r[0] for r in conn.execute("SELECT cert_id FROM whatsapp_sent_log").fetchall() if r[0])
    sent_phones = set(r[0] for r in conn.execute("SELECT clean_phone FROM whatsapp_sent_log").fetchall() if r[0])

    uncontacted_count = 0
    for cand in all_candidates:
        cid = cand.get("certId", "")
        ph = clean_phone_number(cand.get("phone", ""))
        if cid in sent_certs or ph in sent_phones:
            continue
        uncontacted_count += 1

    conn.close()

    print("\n" + "=" * 76)
    print("  DBERT — WHATSAPP DISPATCH OVERALL PROGRESS STATUS")
    print("=" * 76)
    print(f"  Total Candidates in Registry       : {total_candidates}")
    print(f"  Total Messages Sent So Far         : {total_sent_log} (Logged in permanent record)")
    print(f"  Current Active Queue               : {dispatch_pending + dispatch_sent + dispatch_failed} candidates")
    print(f"    - Pending in current queue       : {dispatch_pending}")
    print(f"    - Sent in current queue          : {dispatch_sent}")
    print(f"    - Failed in current queue        : {dispatch_failed}")
    print(f"  Total Uncontacted Candidates Left  : {uncontacted_count}")
    print("=" * 76 + "\n")


# ---------------------------------------------------------------------------
# Message Formatting
# ---------------------------------------------------------------------------
_EMAIL_TRACKING_MAP = None


def get_email_tracking_map() -> dict:
    """Loads email tracking state from data/dispatch_tracking_sheet_1593.json and data/dispatch_tracking_409.json."""
    global _EMAIL_TRACKING_MAP
    if _EMAIL_TRACKING_MAP is not None:
        return _EMAIL_TRACKING_MAP
    _EMAIL_TRACKING_MAP = {}
    
    # 1. Check Sheet 1593 tracking first
    tracking_1593 = DATA_DIR / "dispatch_tracking_sheet_1593.json"
    if tracking_1593.exists():
        try:
            with open(tracking_1593, "r", encoding="utf-8") as f:
                for r in json.load(f):
                    cid = (r.get("certId") or "").strip()
                    em = (r.get("email") or "").strip().lower()
                    if cid:
                        _EMAIL_TRACKING_MAP[cid] = r
                    if em:
                        _EMAIL_TRACKING_MAP[f"em:{em}"] = r
        except Exception as e:
            print(f"[WARN] Failed loading sheet 1593 tracking map: {e}")

    # 2. Check 409 tracking
    tracking_file = DATA_DIR / "dispatch_tracking_409.json"
    if tracking_file.exists():
        try:
            with open(tracking_file, "r", encoding="utf-8") as f:
                for r in json.load(f):
                    cid = (r.get("certId") or "").strip()
                    em = (r.get("email") or "").strip().lower()
                    if cid and cid not in _EMAIL_TRACKING_MAP:
                        _EMAIL_TRACKING_MAP[cid] = r
                    if em and f"em:{em}" not in _EMAIL_TRACKING_MAP:
                        _EMAIL_TRACKING_MAP[f"em:{em}"] = r
        except Exception as e:
            print(f"[WARN] Failed loading email tracking map: {e}")
    return _EMAIL_TRACKING_MAP


def format_email_dispatch_notice(cand: dict) -> str:
    """
    Builds the official email notice citing sending account and dispatch timestamp.
    """
    cert_id = cand.get("cert_id") or cand.get("certId") or ""
    em = (cand.get("user_email") or cand.get("email") or "").strip().lower()

    email_map = get_email_tracking_map()
    e_info = email_map.get(cert_id) or email_map.get(f"em:{em}") or {}
    status = e_info.get("status")
    sent_at_raw = e_info.get("sent_at")
    sent_from = e_info.get("sent_from") or "abhinav.sharma@dbert.in"

    if status == "SENT" and sent_at_raw:
        try:
            dt = datetime.fromisoformat(sent_at_raw.split(".")[0])
            ts_display = dt.strftime("%d %b %Y at %I:%M %p IST")
        except Exception:
            ts_display = sent_at_raw
        return f"An official credential email was sent to your inbox from *{sent_from}* on *{ts_display}*. Please check your inbox & spam folder."
    else:
        return f"An official credential email from *DBERT Directorate* is registered and queued for delivery to your inbox today. Please check your inbox & spam folder."


def format_whatsapp_message(cand: dict) -> str:
    """
    Formats the official DBERT credential notification message.
    CRITICAL CONSTRAINTS (Strictly in lines 1-15):
    - Verification URL (Line 8)
    - Google Form URL (Line 11)
    - Email Notice with Timestamp from abhinav.sharma@dbert.in (Line 14)
    """
    name = (cand.get("holder_name") or cand.get("holderName") or "Candidate").strip()
    domain = cand.get("domain_track") or cand.get("domain") or "Applied AI Engineering"
    project = cand.get("core_project") or cand.get("project") or "Production Incubation System"
    score = cand.get("score") or 85
    grade = cand.get("grade") or "Grade A (Very Good)"
    cert_id = cand.get("cert_id") or cand.get("certId") or ""
    verify_url = cand.get("verification_url") or cand.get("verificationUrl") or f"https://dbert.in/verify?certid={cert_id}"
    email_notice = format_email_dispatch_notice(cand)

    return (
        f"🎓 *Official Credential Release – DBERT Incubation*\n"
        f"\n"
        f"Dear {name},\n"
        f"\n"
        f"Congratulations! Your official internship credential has been verified & recorded.\n"
        f"\n"
        f"🔗 *Direct Verification Link & Dossier:*\n"
        f"👉 {verify_url}\n"
        f"\n"
        f"📝 *Claim & Verification Form (Mandatory):*\n"
        f"👉 {GOOGLE_FORM_URL}\n"
        f"\n"
        f"📧 *Official Email Notice:*\n"
        f"{email_notice}\n"
        f"\n"
        f"📌 *Credential Summary:*\n"
        f"• *Candidate:* {name}\n"
        f"• *Certificate ID:* {cert_id}\n"
        f"• *Track:* {domain}\n"
        f"• *Project:* {project}\n"
        f"• *Score:* {score}/100 ({grade})\n"
        f"\n"
        f"📜 *Next Steps:*\n"
        f"1️⃣ Tap your verification link to view your tamper-proof credential dossier.\n"
        f"2️⃣ Fill out the Google Form above to confirm your dispatch details.\n"
        f"3️⃣ Check your email from abhinav.sharma@dbert.in for your official credential dossier.\n"
        f"4️⃣ Share your verified credential directly to LinkedIn or download your records.\n"
        f"\n"
        f"⚠️ *Note:* All official DBERT credentials operate under our sovereign domain *dbert.in*. Legacy links referencing dbert.online redirect securely.\n"
        f"\n"
        f"📩 *Queries?* Reply directly to this WhatsApp message or email contactus@dbert.in.\n"
        f"\n"
        f"Best regards,\n"
        f"*Abhinav Sharma*\n"
        f"Program Head & Project Mentor\n"
        f"*DBERT — Digital Blinc Education Research And Technology*\n"
        f"🌐 https://dbert.in"
    )


# ---------------------------------------------------------------------------
# WhatsApp Dispatch (Playwright Persistent Context)
# ---------------------------------------------------------------------------
def send_whatsapp_single(page, cand: dict) -> tuple[bool, str]:
    """Automates sending a single WhatsApp message via WhatsApp Web."""
    if page.is_closed():
        return False, "BROWSER_CLOSED"

    phone = cand.get("clean_phone") or clean_phone_number(cand.get("phone", ""))
    if not phone or len(phone) < 10:
        return False, "INVALID_PHONE"

    msg = format_whatsapp_message(cand)
    encoded_msg = urllib.parse.quote(msg)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"

    try:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=35000)
        except Exception as e_nav:
            err_msg = str(e_nav).lower()
            if "closed" in err_msg:
                return False, f"BROWSER_CLOSED: {str(e_nav)}"

        t_start = time.time()
        sent = False
        while time.time() - t_start < 35:
            if page.is_closed():
                return False, "BROWSER_CLOSED"

            dialogs = page.query_selector_all("[role='dialog']")
            starting_chat = False
            for d in dialogs:
                try:
                    txt = d.inner_text().lower()
                    if any(term in txt for term in ["invalid", "not on whatsapp", "url is invalid", "couldn't find"]):
                        btn = d.query_selector("button")
                        if btn:
                            btn.click()
                        return False, "NOT_ON_WHATSAPP"
                    elif "starting chat" in txt:
                        starting_chat = True
                except Exception:
                    pass

            if starting_chat:
                time.sleep(1)
                continue

            # 1. Look for Send button
            send_btn = page.query_selector('button[aria-label="Send"], button[data-testid="send"], button[data-testid="compose-btn-send"], span[data-icon="send"]')
            if send_btn:
                try:
                    time.sleep(0.5)
                    tag = page.evaluate("(el) => el.tagName.toLowerCase()", send_btn)
                    if tag != "button":
                        btn_parent = page.evaluate_handle("(el) => el.closest('button') || el", send_btn)
                        btn_parent.click()
                    else:
                        send_btn.click()
                    time.sleep(2)
                    sent = True
                    break
                except Exception:
                    pass

            # 2. Look for message input and send Enter
            chat_input = page.query_selector('footer div[contenteditable="true"], div[role="textbox"], div[contenteditable="true"][data-tab="10"]')
            if chat_input:
                try:
                    text_content = chat_input.inner_text().strip()
                    if text_content:
                        chat_input.focus()
                        time.sleep(0.5)
                        page.keyboard.press("Enter")
                        time.sleep(2)
                        sent = True
                        break
                except Exception:
                    pass

            time.sleep(1)

        if not sent:
            return False, "TIMEOUT_SEND_NOT_COMPLETED"

        return True, "SENT"
    except Exception as e:
        return False, f"ERROR: {str(e)}"


# ---------------------------------------------------------------------------
# Account Worker Process
# ---------------------------------------------------------------------------
def run_worker(account_group: str, delay_min: float = 18.0, delay_max: float = 35.0, auto_start: bool = True):
    """Runs a dedicated worker process for account1_odd or account2_even."""
    init_db()

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM whatsapp_dispatch
        WHERE account_group = ? AND whatsapp_status = 'PENDING'
        ORDER BY serial_no ASC
        LIMIT ?
    """, (account_group, MAX_MESSAGES_PER_ACCOUNT))
    candidates = [dict(r) for r in c.fetchall()]
    conn.close()

    acc_num = 1 if account_group == "account1_odd" else 2
    session_dir = str(SESSION_ACC1 if acc_num == 1 else SESSION_ACC2)

    print("\n" + "=" * 76)
    print(f"  DBERT — WHATSAPP WORKER ACCOUNT {acc_num} ({account_group.upper()})")
    print(f"  Session Folder     : {session_dir}")
    print(f"  Queue Size         : {len(candidates)} candidates (Capped at {MAX_MESSAGES_PER_ACCOUNT})")
    print(f"  Pacing Delay       : {delay_min}s – {delay_max}s randomized human breaks")
    print("=" * 76)

    if not candidates:
        print(f"[OK] No pending candidates for {account_group}. Queue complete!")
        return

    from playwright.sync_api import sync_playwright

    consecutive_wa_failures = 0
    delivered_count = 0

    try:
        with sync_playwright() as p:
            launch_args = [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars",
                "--remote-debugging-port=0",
            ]

            browser = None
            try:
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=session_dir,
                    channel="chrome",
                    headless=False,
                    ignore_default_args=["--enable-automation"],
                    args=launch_args,
                )
            except Exception as e_chrome:
                print(f"[*] System Chrome failed ({e_chrome}). Launching bundled Chromium...")
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=session_dir,
                    headless=False,
                    ignore_default_args=["--enable-automation"],
                    args=launch_args,
                )

            browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.on("dialog", lambda d: d.accept())

            print(f"\n[*] Opening WhatsApp Web for Account {acc_num}...")
            page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)

            print(f"[*] Checking session status for Account {acc_num}...")
            logged_in = False
            for _ in range(25):
                if page.is_closed():
                    break
                if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header"):
                    logged_in = True
                    break
                time.sleep(1)

            if logged_in:
                print(f"[OK] Account {acc_num} WhatsApp session is active! Auto-starting in 3 seconds...")
                time.sleep(3)
            elif auto_start:
                print("\n" + "!" * 76)
                print(f"  [ACTION REQUIRED] Account {acc_num} is not logged in.")
                print(f"  >>> Please scan the QR code in the opened Chrome window using WhatsApp.")
                print(f"  (Auto-start enabled: Dispatch will begin automatically once scanned)")
                print("!" * 76 + "\n")
                for _ in range(120):  # wait up to 4 minutes
                    if page.is_closed():
                        print(f"[!] Browser window was closed for Account {acc_num}.")
                        return
                    if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header"):
                        logged_in = True
                        break
                    time.sleep(2)
                if not logged_in:
                    print(f"[ERROR] Account {acc_num} login timed out. Halting worker.")
                    return
                print(f"\n[OK] Account {acc_num} logged in! Starting dispatch in 3 seconds...")
                time.sleep(3)
            else:
                input(f"\n>>> Verify Account {acc_num} is logged into WhatsApp Web (scan QR code in Chrome if needed), then press [ENTER] to start: ")

            total = len(candidates)
            for idx, cand in enumerate(candidates, 1):
                s_no = cand["serial_no"]
                name = cand["holder_name"]
                phone = cand["clean_phone"]
                email = cand["user_email"]
                cert_id = cand["cert_id"]

                # Refresh status from DB
                conn = get_db_connection()
                cur = conn.execute("SELECT whatsapp_status FROM whatsapp_dispatch WHERE serial_no = ?", (s_no,)).fetchone()
                conn.close()

                wa_status = cur["whatsapp_status"] if cur else "PENDING"
                if wa_status == "SENT":
                    print(f"  [{idx:2d}/{total}] SKIPPED: Serial #{s_no} ({name}) already sent.")
                    continue

                print(f"\n----------------------------------------------------------------------")
                print(f"  [{idx:2d}/{total}] Processing #{s_no}: {name} | Phone: +{phone} | Cert: {cert_id}")
                print(f"----------------------------------------------------------------------")

                wa_ok, wa_detail = send_whatsapp_single(page, cand)
                conn = get_db_connection()
                if wa_ok:
                    consecutive_wa_failures = 0
                    delivered_count += 1
                    print(f"  [WA SUCCESS] Delivered to {name} (+{phone}) | Total Sent: {delivered_count}/{total}")
                    now_iso = datetime.now().isoformat()
                    conn.execute("""
                        UPDATE whatsapp_dispatch 
                        SET whatsapp_status = 'SENT', whatsapp_sent_at = ?, whatsapp_error = NULL
                        WHERE serial_no = ?
                    """, (now_iso, s_no))
                    # Record to permanent history log
                    conn.execute("""
                        INSERT OR REPLACE INTO whatsapp_sent_log
                        (candidate_id, holder_name, user_email, clean_phone, cert_id, domain_track, account_group, whatsapp_sent_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (cand["candidate_id"], name, email, phone, cert_id, cand.get("domain_track"), account_group, now_iso))
                else:
                    consecutive_wa_failures += 1
                    print(f"  [WA FAILED] Detail: {wa_detail} | Consecutive Failures: {consecutive_wa_failures}/{MAX_CONSECUTIVE_WA_FAILURES}")
                    conn.execute("""
                        UPDATE whatsapp_dispatch 
                        SET whatsapp_status = 'FAILED', whatsapp_error = ?
                        WHERE serial_no = ?
                    """, (wa_detail, s_no))

                conn.commit()
                conn.close()

                if "BROWSER_CLOSED" in wa_detail:
                    print(f"\n[ALERT] Chrome browser for Account {acc_num} was closed! Halting worker to preserve remaining queue.")
                    break

                if consecutive_wa_failures >= MAX_CONSECUTIVE_WA_FAILURES:
                    print(f"\n[ALERT] Reached {MAX_CONSECUTIVE_WA_FAILURES} consecutive WhatsApp failures! Pausing worker for inspection.")
                    input(">>> Press [ENTER] when ready to resume: ")
                    consecutive_wa_failures = 0

                # Randomized safety pacing
                if idx < total:
                    sleep_time = random.uniform(delay_min, delay_max)
                    print(f"  [Pacing Delay] Sleeping {sleep_time:.1f}s before next contact...")
                    time.sleep(sleep_time)

            print(f"\n[OK] Worker for Account {acc_num} completed dispatch! ({delivered_count} messages sent)")
            export_queues_csv()

    except Exception as e_worker:
        print(f"\n[ERROR] Worker failed: {e_worker}")
        export_queues_csv()


# ---------------------------------------------------------------------------
# Dry Run & Test Send
# ---------------------------------------------------------------------------
def dry_run():
    """Previews the current dispatch queue, account split, and sample message."""
    init_db()
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM whatsapp_dispatch ORDER BY serial_no ASC").fetchall()
    sent_count = conn.execute("SELECT count(*) as c FROM whatsapp_sent_log").fetchone()["c"]
    conn.close()

    total = len(rows)
    acc1_rows = [dict(r) for r in rows if r["account_group"] == "account1_odd"]
    acc2_rows = [dict(r) for r in rows if r["account_group"] == "account2_even"]

    print("\n" + "=" * 76)
    print("  DBERT — DUAL WHATSAPP DISPATCH QUEUE SUMMARY (DRY RUN)")
    print("=" * 76)
    print(f"  Total Candidates in Active Queue : {total}")
    print(f"  Account 1 (Odd Serials)          : {len(acc1_rows)} candidates (Capped at {MAX_MESSAGES_PER_ACCOUNT})")
    print(f"  Account 2 (Even Serials)         : {len(acc2_rows)} candidates (Capped at {MAX_MESSAGES_PER_ACCOUNT})")
    print(f"  Permanent Sent History Log       : {sent_count} candidates already delivered")
    print("=" * 76)

    print("\n--- FIRST 5 CANDIDATES FOR ACCOUNT 1 (ODD - LATEST SIGNUPS) ---")
    for r in acc1_rows[:5]:
        ts = r.get("signup_timestamp") or "N/A"
        print(f"  #{r['serial_no']:2d} | [{ts:<19}] | {r['holder_name']:<22} | {r['cert_id']:<24} | +{r['clean_phone']}")

    print("\n--- FIRST 5 CANDIDATES FOR ACCOUNT 2 (EVEN - LATEST SIGNUPS) ---")
    for r in acc2_rows[:5]:
        ts = r.get("signup_timestamp") or "N/A"
        print(f"  #{r['serial_no']:2d} | [{ts:<19}] | {r['holder_name']:<22} | {r['cert_id']:<24} | +{r['clean_phone']}")

    if rows:
        print("\n" + "=" * 76)
        print("  SAMPLE FORMATTED MESSAGE PREVIEW (CANDIDATE #1):")
        print("=" * 76)
        cand1 = dict(rows[0])
        print(f"Recipient: {cand1['holder_name']} (+{cand1['clean_phone']})")
        print(f"Cert ID  : {cand1['cert_id']}")
        print(f"Account  : {cand1['account_group']}")
        print(f"Signup TS: {cand1.get('signup_timestamp') or 'N/A'}\n")
        msg = format_whatsapp_message(cand1)
        for i, line in enumerate(msg.split("\n"), 1):
            tag = ""
            if cand1.get("verification_url", "") in line:
                tag = "  <-- [VERIFICATION URL in first 15 lines]"
            elif GOOGLE_FORM_URL in line:
                tag = "  <-- [GOOGLE FORM URL in first 15 lines]"
            elif "abhinav.sharma@dbert.in" in line:
                tag = "  <-- [EMAIL DISPATCH NOTICE in first 15 lines]"
            print(f"Line {i:2d}: {line}{tag}")
        print("=" * 76 + "\n")


def send_test_message(phone: str, account_num: int = 1):
    """Sends 1 test message to the specified phone number."""
    clean_phone = clean_phone_number(phone)
    if not clean_phone or len(clean_phone) < 10:
        print(f"[ERROR] Invalid phone number: {phone}")
        return

    sample_cand = {
        "holder_name": "Test Candidate",
        "domain_track": "Data Analyst Track",
        "core_project": "Cognitive Solutions",
        "score": 88,
        "grade": "Grade A (Very Good)",
        "cert_id": "CERT-DBERT-2026-TEST-001",
        "clean_phone": clean_phone,
        "verification_url": "https://dbert.in/verify?certid=CERT-DBERT-2026-TEST-001"
    }

    session_dir = str(SESSION_ACC1 if account_num == 1 else SESSION_ACC2)

    print("\n" + "=" * 76)
    print(f"  SENDING TEST WHATSAPP MESSAGE VIA ACCOUNT {account_num}")
    print(f"  Recipient Phone: +{clean_phone}")
    print(f"  Session Dir    : {session_dir}")
    print("=" * 76)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        ok, detail = send_whatsapp_single(page, sample_cand)
        time.sleep(3)
        browser.close()

        if ok:
            print(f"\n[OK] Test message successfully delivered to +{clean_phone} via Account {account_num}!")
        else:
            print(f"\n[FAILED] Test delivery failed: {detail}")


# ---------------------------------------------------------------------------
# Cross-Channel Sync (Email + WhatsApp Unified Tracking)
# ---------------------------------------------------------------------------
def sync_email_and_whatsapp_tracking():
    """
    Cross-references email delivery records (dispatch_tracking_409.json) with
    WhatsApp delivery status (dbert_whatsapp.db) and exports a unified report.
    """
    init_db()
    conn = get_db_connection()

    # WhatsApp sent map
    wa_sent_rows = conn.execute("SELECT cert_id, clean_phone, whatsapp_sent_at FROM whatsapp_sent_log").fetchall()
    wa_sent_map = {r["cert_id"]: r["whatsapp_sent_at"] for r in wa_sent_rows if r["cert_id"]}
    wa_phone_map = {r["clean_phone"]: r["whatsapp_sent_at"] for r in wa_sent_rows if r["clean_phone"]}

    # Active queue map
    wa_dispatch_rows = conn.execute("SELECT cert_id, clean_phone, whatsapp_status, whatsapp_error FROM whatsapp_dispatch").fetchall()
    wa_dispatch_map = {r["cert_id"]: r for r in wa_dispatch_rows if r["cert_id"]}

    conn.close()

    # Load email tracking records
    email_records = []
    if EMAIL_TRACKING_PATH.exists():
        try:
            with open(EMAIL_TRACKING_PATH, "r", encoding="utf-8") as ef:
                email_records = json.load(ef)
        except Exception as e:
            print(f"[!] Warning reading email tracking file: {e}")

    registry = load_registry_candidates()
    email_map = {r.get("certId"): r for r in email_records if r.get("certId")}

    unified_output = DATA_DIR / "dbert_unified_omnichannel_tracking.csv"
    headers = [
        "cert_id", "intern_id", "holder_name", "email", "phone", "domain",
        "email_status", "email_sent_at", "email_message_id",
        "whatsapp_status", "whatsapp_sent_at", "whatsapp_error"
    ]

    count_both_sent = 0
    count_email_only = 0
    count_wa_only = 0
    count_pending = 0

    with open(unified_output, "w", newline="", encoding="utf-8-sig") as uf:
        writer = csv.DictWriter(uf, fieldnames=headers)
        writer.writeheader()

        for cand in registry:
            cert_id = cand.get("certId", "")
            phone = clean_phone_number(cand.get("phone", ""))
            em_info = email_map.get(cert_id, {})
            email_status = em_info.get("status", "PENDING")
            email_sent_at = em_info.get("sent_at", "")
            email_msg_id = em_info.get("message_id", "")

            # WhatsApp Status resolution
            if cert_id in wa_sent_map or phone in wa_phone_map:
                wa_status = "SENT"
                wa_sent_at = wa_sent_map.get(cert_id) or wa_phone_map.get(phone, "")
                wa_error = ""
            elif cert_id in wa_dispatch_map:
                dq = wa_dispatch_map[cert_id]
                wa_status = dq["whatsapp_status"]
                wa_sent_at = ""
                wa_error = dq["whatsapp_error"] or ""
            else:
                wa_status = "PENDING"
                wa_sent_at = ""
                wa_error = ""

            if email_status == "SENT" and wa_status == "SENT":
                count_both_sent += 1
            elif email_status == "SENT":
                count_email_only += 1
            elif wa_status == "SENT":
                count_wa_only += 1
            else:
                count_pending += 1

            writer.writerow({
                "cert_id": cert_id,
                "intern_id": cand.get("internId", ""),
                "holder_name": cand.get("holderName", ""),
                "email": cand.get("email", ""),
                "phone": phone,
                "domain": cand.get("domain", ""),
                "email_status": email_status,
                "email_sent_at": email_sent_at,
                "email_message_id": email_msg_id,
                "whatsapp_status": wa_status,
                "whatsapp_sent_at": wa_sent_at,
                "whatsapp_error": wa_error
            })

    print("\n" + "=" * 76)
    print("  DBERT — UNIFIED OMNICHANNEL (EMAIL + WHATSAPP) TRACKING EXPORT")
    print("=" * 76)
    print(f"  Total Candidates in Registry : {len(registry)}")
    print(f"  Delivered via BOTH Channels  : {count_both_sent}")
    print(f"  Delivered via EMAIL ONLY     : {count_email_only}")
    print(f"  Delivered via WHATSAPP ONLY  : {count_wa_only}")
    print(f"  Pending on BOTH Channels     : {count_pending}")
    print(f"  Export File Generated        : {unified_output}")
    print("=" * 76 + "\n")


# ---------------------------------------------------------------------------
# CLI Argument Router
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="DBERT Dual-Account WhatsApp Candidate Dispatcher")
    parser.add_argument("--init-db", action="store_true", help="Initialize database tables")
    parser.add_argument("--next-batch", action="store_true", help="Load next batch of remaining uncontacted candidates")
    parser.add_argument("--load-sheet-92", "--load-sheet-1593", dest="load_sheet_92", action="store_true", help="Load first 92 candidates from sheet 1593 partitioned for Account 1 & 2")
    parser.add_argument("--status", action="store_true", help="Display overall campaign progress and counts")
    parser.add_argument("--dry-run", action="store_true", help="Display queue counts and sample message preview")
    parser.add_argument("--reset-failed", action="store_true", help="Reset FAILED records back to PENDING")
    parser.add_argument("--worker", choices=["account1", "account2"], help="Run dispatch worker for account1 or account2")
    parser.add_argument("--test-to", "--test-phone", dest="test_to", type=str, help="Send 1 test message to the specified phone number")
    parser.add_argument("--account", type=int, choices=[1, 2], default=1, help="Account number for test send (default: 1)")
    parser.add_argument("--sync-email", action="store_true", help="Cross-reference with email tracking and export unified CSV")
    parser.add_argument("--auto-start", action="store_true", default=True, help="Auto-start dispatch without prompt once WhatsApp is active")
    parser.add_argument("--delay-min", type=float, default=18.0, help="Minimum delay between messages in seconds")
    parser.add_argument("--delay-max", type=float, default=35.0, help="Maximum delay between messages in seconds")

    args = parser.parse_args()

    if args.init_db:
        init_db()
        print(f"[OK] Initialized database at {DB_PATH}")
    elif args.next_batch:
        load_next_batch()
    elif args.load_sheet_92:
        load_sheet_1593_first_92()
    elif args.status:
        print_overall_status()
    elif args.reset_failed:
        reset_failed_to_pending()
    elif args.dry_run:
        dry_run()
    elif args.test_to:
        send_test_message(args.test_to, account_num=args.account)
    elif args.sync_email:
        sync_email_and_whatsapp_tracking()
    elif args.worker:
        account_group = "account1_odd" if args.worker == "account1" else "account2_even"
        run_worker(account_group, delay_min=args.delay_min, delay_max=args.delay_max, auto_start=args.auto_start)
    else:
        dry_run()


if __name__ == "__main__":
    main()
