import json
import sqlite3
import argparse
from pathlib import Path
from format_revenue_whatsapp import format_revenue_whatsapp_message, clean_phone_number

DB_PATH = Path("data/dbert_revenue_whatsapp.db")
TARGET_JSON = Path("data/balanced_revenue_target_100.json")

def init_revenue_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS whatsapp_revenue_dispatch (
            serial_no INTEGER PRIMARY KEY,
            account_group TEXT NOT NULL,
            account_num INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            clean_phone TEXT,
            amount INTEGER NOT NULL,
            domain TEXT,
            priority_tier INTEGER,
            whatsapp_message TEXT NOT NULL,
            whatsapp_status TEXT DEFAULT 'PENDING',
            sent_at TEXT,
            whatsapp_error TEXT
        );
    """)
    conn.commit()
    return conn

def load_revenue_cohort():
    with open(TARGET_JSON, "r", encoding="utf-8") as f:
        cohort = json.load(f)

    conn = init_revenue_db()
    c = conn.cursor()
    c.execute("DELETE FROM whatsapp_revenue_dispatch;")

    inserted = 0
    for idx, cand in enumerate(cohort, start=1):
        # Odd serials -> Account 1, Even serials -> Account 2
        acc_num = 1 if (idx % 2 != 0) else 2
        acc_group = f"account{acc_num}"
        raw_phone = cand.get("phone", "")
        clean_phone = clean_phone_number(raw_phone)
        msg = format_revenue_whatsapp_message(cand)

        c.execute("""
            INSERT INTO whatsapp_revenue_dispatch (
                serial_no, account_group, account_num, name, email, phone, clean_phone,
                amount, domain, priority_tier, whatsapp_message, whatsapp_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
        """, (
            idx, acc_group, acc_num, cand.get("name", ""), cand.get("email", ""),
            raw_phone, clean_phone, cand.get("amount", 499), cand.get("domain", ""),
            cand.get("priority_tier", 1), msg
        ))
        inserted += 1

    conn.commit()
    conn.close()
    print(f"Loaded {inserted} candidates into {DB_PATH}")

def status():
    if not DB_PATH.exists():
        print("Database not initialized yet.")
        return
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    total = conn.execute("SELECT count(*) as c FROM whatsapp_revenue_dispatch").fetchone()["c"]
    pending = conn.execute("SELECT count(*) as c FROM whatsapp_revenue_dispatch WHERE whatsapp_status = 'PENDING'").fetchone()["c"]
    sent = conn.execute("SELECT count(*) as c FROM whatsapp_revenue_dispatch WHERE whatsapp_status = 'SENT'").fetchone()["c"]
    failed = conn.execute("SELECT count(*) as c FROM whatsapp_revenue_dispatch WHERE whatsapp_status = 'FAILED'").fetchone()["c"]
    acc1 = conn.execute("SELECT count(*) as c FROM whatsapp_revenue_dispatch WHERE account_num = 1").fetchone()["c"]
    acc2 = conn.execute("SELECT count(*) as c FROM whatsapp_revenue_dispatch WHERE account_num = 2").fetchone()["c"]
    conn.close()

    print("="*60)
    print("  DBERT REVENUE WHATSAPP QUEUE STATUS (100 TARGETS)")
    print("="*60)
    print(f"  Total Targets  : {total}")
    print(f"  Pending        : {pending}")
    print(f"  Sent           : {sent}")
    print(f"  Failed         : {failed}")
    print(f"  Account 1 (Odd) : {acc1} candidates")
    print(f"  Account 2 (Even): {acc2} candidates")
    print("="*60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--load", action="store_true", help="Load balanced 100 targets into DB")
    parser.add_argument("--status", action="store_true", help="Check queue status")
    args = parser.parse_args()

    if args.load:
        load_revenue_cohort()
    elif args.status:
        status()
    else:
        status()
