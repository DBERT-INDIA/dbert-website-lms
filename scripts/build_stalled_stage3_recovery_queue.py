#!/usr/bin/env python3
"""
scripts/build_stalled_stage3_recovery_queue.py
Builds the targeted recovery queue for Stalled Stage 3 (Selected) candidates.
Targets candidates who have an issued digital offer letter but have not completed
seat confirmation (unpaid ₹499 caution deposit).

Sovereign Rules Enforced:
- Active origin strictly https://dbert.in and https://lms.dbert.in
- Verified deduplication against data/dbert_whatsapp_sent_today.json
- Formats queue with complete personalization tokens
"""

import os
import sys
import json
import re
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding="utf-8")

DATA_DIR = "data"
SENT_TODAY_FILE = os.path.join(DATA_DIR, "dbert_whatsapp_sent_today.json")
OUTPUT_QUEUE_FILE = os.path.join(DATA_DIR, "stalled_stage3_recovery_queue.json")

CANDIDATE_SOURCES = [
    os.path.join(DATA_DIR, "selected_under_review_cohort_125.json"),
    os.path.join(DATA_DIR, "selected_applications_last_48h.json"),
    os.path.join(DATA_DIR, "whatsapp_last_70_selected_unpaid.json"),
]

def clean_phone_number(raw):
    if not raw:
        return ""
    p = re.sub(r"[^\d]", "", str(raw))
    if p.startswith("91") and len(p) == 12:
        p = p[2:]
    elif p.startswith("0") and len(p) == 11:
        p = p[1:]
    if len(p) == 10 and p[0] in "6789":
        return f"+91{p}"
    return ""

def load_sent_today():
    if os.path.exists(SENT_TODAY_FILE):
        try:
            with open(SENT_TODAY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def main():
    dry_run = "--dry-run" in sys.argv
    print("=" * 80)
    print("BUILDING STALLED STAGE 3 CANDIDATE RECOVERY QUEUE")
    print(f"Mode: {'DRY RUN' if dry_run else 'PRODUCTION QUEUE GENERATION'}")
    print("=" * 80)

    sent_today = load_sent_today()
    print(f"Loaded {len(sent_today)} entries from sent-today audit log.")

    seen_phones = set()
    seen_emails = set()
    queue = []

    for src in CANDIDATE_SOURCES:
        if not os.path.exists(src):
            continue
        try:
            with open(src, "r", encoding="utf-8") as f:
                data = json.load(f)
                items = data if isinstance(data, list) else data.get("candidates", [])
                print(f"Scanning {src} ({len(items)} records)...")
                for c in items:
                    email = (c.get("email") or "").strip().lower()
                    phone = (c.get("phone") or "").strip()
                    clean_phone = clean_phone_number(phone)
                    name = (c.get("name") or "Candidate").strip()
                    first_name = name.split()[0].capitalize()
                    domain = c.get("domain") or "Applied Engineering"
                    offer_id = c.get("offer_letter_id") or f"DBERT-OFR-2026-{domain[:3].upper()}-AUTO"

                    if not clean_phone or not email:
                        continue
                    if email in seen_emails or clean_phone in seen_phones:
                        continue

                    # Check against 24h sent log
                    raw_digits = clean_phone[-10:]
                    if clean_phone in sent_today or raw_digits in sent_today or email in sent_today:
                        continue

                    seen_phones.add(clean_phone)
                    seen_emails.add(email)

                    queue.append({
                        "name": name,
                        "first_name": first_name,
                        "email": email,
                        "phone": clean_phone,
                        "raw_phone": raw_digits,
                        "domain": domain,
                        "offer_letter_id": offer_id,
                        "offer_url": "https://lms.dbert.in/portal/offer",
                        "verification_url": "https://dbert.in/verify",
                        "enrollment_url": f"https://dbert.in/enroll/1999?email={email}",
                        "stipend_amount": "₹5,000",
                        "incentive_amount": "Up to ₹18,000",
                        "caution_deposit": "₹499 (100% Credited)",
                        "exam_pause_clause": "14-Day University Examination Pause with Zero Academic Penalty",
                        "queued_at": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat()
                    })
        except Exception as e:
            print(f"Error reading {src}: {e}")

    print(f"\nDiscovered {len(queue)} qualified stalled candidates for recovery dispatch.")

    if not dry_run:
        with open(OUTPUT_QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        print(f"Queue successfully written to: {OUTPUT_QUEUE_FILE}")
    else:
        print("Dry run active: skipped writing queue to disk.")

    if queue:
        print("\nSample Preview of First Queued Candidate:")
        print(json.dumps(queue[0], indent=2))

if __name__ == "__main__":
    main()
