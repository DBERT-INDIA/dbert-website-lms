#!/usr/bin/env python3
"""
================================================================================
DBERT — ₹299 Credential Verification & ₹5,000 Stipend Queue Generator
================================================================================
Extracts all provisional candidates who:
  1. Have NOT paid the ₹299 project verification fee.
  2. Have NOT received their ₹5,000 release stipend / ₹299 notice message.
  3. Possess a valid 10-digit Indian mobile number (starting with 6/7/8/9).

Ranks candidates by:
  - Evaluation Score descending (88 -> 70)
  - Recency and domain

Shards into:
  - data/whatsapp_299_uncontacted_master_220.json (All 220 clean candidates)
  - data/whatsapp_299_queue_batch35_acc1.json (35 candidates for Account 1)
  - data/whatsapp_299_queue_batch35_acc2.json (35 candidates for Account 2)
  - data/whatsapp_299_queue_batch70_dual.json (Combined 70 candidates)
================================================================================
"""

import sys
import json
import sqlite3
import csv
import re
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(r"C:\Users\user\Desktop\dbert-website-lms")
DATA_DIR = PROJECT_ROOT / "data"

def clean_phone(p):
    if not p:
        return ""
    d = re.sub(r"\D", "", str(p))
    if len(d) > 10 and d.startswith("91"):
        d = d[2:]
    elif len(d) > 10 and d.startswith("0"):
        d = d[1:]
    return d[-10:] if len(d) >= 10 else d

def clean_name(name_str):
    if not name_str:
        return "Fellow"
    n = name_str.strip()
    if "@" in n:
        parts = n.split("@")[0]
        # clean email-like names like jaiswalaryanxyz
        cleaned = re.sub(r"[^a-zA-Z\s]", "", parts)
        return cleaned.title() if cleaned else "Fellow"
    return n

def build_message(name: str, domain: str, cert_id: str, email: str) -> str:
    first_name = name.split()[0] if name else "Fellow"
    if first_name.lower() in ["fellow", "candidate"]:
        first_name = name

    # Adheres strictly to the First-15-Lines rule
    return (
        f"Hello {first_name},\n"
        f"\n"
        f"Regarding your {domain} Internship at DBERT:\n"
        f"Your milestone progress has been verified. To clear Gate 3 (Credential Verification) and unlock your ₹5,000 Milestone Stipend, please complete your official verification (₹299).\n"
        f"\n"
        f"🌐 View Pre-Vetted Engineers Directory:\n"
        f"https://dbert.in/verify/directory\n"
        f"\n"
        f"👉 Instant Verification & Stipend Unlock:\n"
        f"https://dbert.in/verify/unlock?certid={cert_id}&email={email}\n"
        f"\n"
        f"Admissions & Verification Concierge (https://dbert.in)"
    )

def main():
    print("=" * 70)
    print("  DBERT: BUILDING ₹299 & ₹5,000 STIPEND UNCONTACTED QUEUES")
    print("=" * 70)

    # 1. Gather all exclusions (already contacted across all campaigns)
    contacted_phones = set()
    contacted_emails = set()
    contacted_certs = set()

    # SQLite
    db_path = DATA_DIR / "dbert_whatsapp.db"
    if db_path.exists():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT clean_phone, user_email, cert_id FROM whatsapp_sent_log")
        for p, e, c in cur.fetchall():
            if p: contacted_phones.add(clean_phone(p))
            if e: contacted_emails.add(e.strip().lower())
            if c: contacted_certs.add(c.strip())

        cur.execute("SELECT phone, email, cert_id, status FROM stipend_dispatch_log")
        for p, e, c, s in cur.fetchall():
            if s == "SENT" or s is None:
                if p: contacted_phones.add(clean_phone(p))
                if e: contacted_emails.add(e.strip().lower())
                if c: contacted_certs.add(c.strip())
        conn.close()

    # Sent Today JSON
    sent_today_path = DATA_DIR / "dbert_whatsapp_sent_today.json"
    if sent_today_path.exists():
        try:
            sent_today = json.load(open(sent_today_path, encoding="utf-8"))
            if isinstance(sent_today, list):
                for r in sent_today:
                    if r.get("status") == "SENT" or "status" not in r:
                        p = clean_phone(r.get("phone"))
                        if p: contacted_phones.add(p)
                        e = (r.get("email") or "").strip().lower()
                        if e: contacted_emails.add(e)
                        c = (r.get("cert_id") or "").strip()
                        if c: contacted_certs.add(c)
            elif isinstance(sent_today, dict):
                for k in sent_today.keys():
                    contacted_phones.add(clean_phone(k))
        except Exception:
            pass

    # Tracking CSVs
    for f in [
        DATA_DIR / "dispatch_tracking_stipend_299.csv",
        DATA_DIR / "dispatch_tracking_batch35_acc2.csv",
        DATA_DIR / "dispatch_tracking_resubmit_27.csv",
        DATA_DIR / "dispatch_tracking_selected_multi_login.csv"
    ]:
        if f.exists():
            with open(f, encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    if r.get("status") == "SENT" or "status" not in r:
                        phone = clean_phone(r.get("clean_phone") or r.get("phone"))
                        if phone: contacted_phones.add(phone)
                        email = (r.get("email") or "").strip().lower()
                        if email: contacted_emails.add(email)
                        cert = (r.get("cert_id") or "").strip()
                        if cert: contacted_certs.add(cert)

    # 2. Gather verified / paid 299 exclusions
    paid_299_certs = set()
    sub_path = DATA_DIR / "verification_submissions_299.json"
    if sub_path.exists():
        for sub in json.load(open(sub_path, encoding="utf-8")):
            c = sub.get("certId")
            if c: paid_299_certs.add(c)

    # 3. Build phone & email lookups from auxiliary registries
    phone_lookup = {}
    email_lookup = {}

    p409 = DATA_DIR / "all_409_provisional_registry.json"
    if p409.exists():
        for r in json.load(open(p409, encoding="utf-8")):
            c = r.get("cert_id") or r.get("certId")
            if c:
                if r.get("phone"): phone_lookup[c] = clean_phone(r.get("phone"))
                if r.get("email"): email_lookup[c] = r.get("email").strip().lower()

    sw_path = DATA_DIR / "second_wave_299_pending_queue.json"
    if sw_path.exists():
        for r in json.load(open(sw_path, encoding="utf-8")):
            c = r.get("certId") or r.get("cert_id")
            if c:
                if r.get("phone"): phone_lookup[c] = clean_phone(r.get("phone"))
                if r.get("email"): email_lookup[c] = r.get("email").strip().lower()

    # 4. Filter directory candidates
    dir_path = PROJECT_ROOT / "apps" / "website" / "src" / "data" / "directory_candidates.json"
    dir_cands = json.load(open(dir_path, encoding="utf-8"))
    provisional_cands = [c for c in dir_cands if c.get("status") == "PROVISIONAL" or c.get("isProvisional") is True]

    uncontacted = []
    for c in provisional_cands:
        cid = c.get("certId")
        p = phone_lookup.get(cid) or clean_phone(c.get("phone"))
        e = email_lookup.get(cid) or (c.get("email") or "").strip().lower()

        if cid in paid_299_certs:
            continue
        if (p and p in contacted_phones) or (e and e in contacted_emails) or (cid and cid in contacted_certs):
            continue
        if p and len(p) == 10 and p[0] in "6789":
            raw_name = c.get("holderName") or "Fellow"
            name = clean_name(raw_name)
            domain = c.get("domain") or "Engineering"
            score = c.get("score", 0)
            msg = build_message(name, domain, cid, e)

            uncontacted.append({
                "cert_id": cid,
                "name": name,
                "first_name": name.split()[0],
                "phone": f"91{p}",
                "clean_phone": p,
                "email": e,
                "domain": domain,
                "score": score,
                "duration": c.get("duration", ""),
                "message": msg
            })

    # Sort descending by score, then cert_id
    uncontacted.sort(key=lambda x: (x["score"], x["cert_id"]), reverse=True)

    print(f"[*] Found {len(uncontacted)} qualified uncontacted candidates pending ₹299.")

    # Save master uncontacted queue (all 220)
    master_file = DATA_DIR / "whatsapp_299_uncontacted_master_220.json"
    with open(master_file, "w", encoding="utf-8") as f:
        json.dump(uncontacted, f, indent=2)
    print(f"[✓] Saved master queue ({len(uncontacted)} items) -> {master_file.name}")

    # Top 70 candidates sharded:
    # Account 1 gets odd indices of top 70 (35 candidates)
    # Account 2 gets even indices of top 70 (35 candidates)
    top_70 = uncontacted[:70]
    acc1_queue = []
    acc2_queue = []

    for idx, cand in enumerate(top_70, 1):
        cand_copy = dict(cand)
        cand_copy["serial_no"] = idx
        if idx % 2 == 1:
            cand_copy["assigned_account"] = "ACCOUNT_1"
            acc1_queue.append(cand_copy)
        else:
            cand_copy["assigned_account"] = "ACCOUNT_2"
            acc2_queue.append(cand_copy)

    acc1_file = DATA_DIR / "whatsapp_299_queue_batch35_acc1.json"
    acc2_file = DATA_DIR / "whatsapp_299_queue_batch35_acc2.json"
    dual_file = DATA_DIR / "whatsapp_299_queue_batch70_dual.json"

    with open(acc1_file, "w", encoding="utf-8") as f:
        json.dump(acc1_queue, f, indent=2)
    print(f"[✓] Saved Account 1 queue ({len(acc1_queue)} items) -> {acc1_file.name}")

    with open(acc2_file, "w", encoding="utf-8") as f:
        json.dump(acc2_queue, f, indent=2)
    print(f"[✓] Saved Account 2 queue ({len(acc2_queue)} items) -> {acc2_file.name}")

    with open(dual_file, "w", encoding="utf-8") as f:
        json.dump(top_70, f, indent=2)
    print(f"[✓] Saved Dual 70 queue ({len(top_70)} items) -> {dual_file.name}")

if __name__ == "__main__":
    main()
