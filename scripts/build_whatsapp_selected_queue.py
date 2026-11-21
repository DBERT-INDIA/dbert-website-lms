#!/usr/bin/env python3
"""
================================================================================
DBERT — Build WhatsApp Selected Multi-Login Queue (9 Candidates)
================================================================================
"""

import json
import re
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COHORT_FILE = ROOT / "data" / "selected_multi_login_cohort.json"
SENT_TODAY_FILE = ROOT / "data" / "dbert_whatsapp_sent_today.json"
OUTPUT_QUEUE = ROOT / "data" / "whatsapp_selected_multi_login_queue.json"

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdFxi9bft4POk4b3eXmp4aH71LmeQrJ0WzXA1bsIm37MalSIw/viewform?usp=header"
PORTAL_OFFER_URL = "https://lms.dbert.in/portal/offer"

def clean_phone(raw_phone: str) -> str:
    if not raw_phone:
        return ""
    digits = re.sub(r"\D", "", str(raw_phone))
    if digits.startswith("91") and len(digits) == 12:
        return digits
    if len(digits) == 10:
        return f"91{digits}"
    if len(digits) > 10 and digits.startswith("0"):
        digits = digits.lstrip("0")
        if len(digits) == 10:
            return f"91{digits}"
    return digits

def format_message(name: str, domain: str) -> str:
    # First 15 lines constraint: Offer URL at Line 8, Form URL at Line 11
    lines = [
        f"Hello {name},",
        "",
        f"🎓 *Congratulations on your selection for the DBERT {domain} Fellowship!*",
        "",
        "Your admissions evaluation is complete and your official Letter of Offer has been approved.",
        "",
        "📄 *Review & Download Your Official Letter of Offer:*",
        PORTAL_OFFER_URL,
        "",
        "👉 *Confirm Seat & Reconcile Caution Deposit:*",
        GOOGLE_FORM_URL,
        "",
        "• Caution Deposit: ₹499 (100% refundable upon milestone completion as per institutional terms)",
        "• Merchant UPI VPA: Q652429146@ybl (DBERT Admissions)",
        "• Performance Stipend: Up to ₹5,000 upon successful sprint and task milestones",
        "",
        "If you have already transferred your deposit via UPI, reply directly to this message with your 12-digit UTR number or transaction screenshot for instant portal activation.",
        "",
        "Warm regards,",
        "DBERT Admissions Desk",
        "Digital Blinc Education Research and Technology (dbert.in)"
    ]
    return "\n".join(lines)

with open(COHORT_FILE, "r", encoding="utf-8") as f:
    cohort = json.load(f)

sent_phones = set()
if SENT_TODAY_FILE.exists():
    try:
        with open(SENT_TODAY_FILE, "r", encoding="utf-8") as f:
            sent_list = json.load(f)
            for s in sent_list:
                p = clean_phone(s.get("phone", ""))
                if p:
                    sent_phones.add(p)
    except Exception as e:
        print(f"Warning loading sent today file: {e}")

queue = []
for cand in cohort:
    name = (cand.get("name") or "").strip()
    email = (cand.get("email") or "").strip().lower()
    raw_phone = cand.get("phone", "")
    phone = clean_phone(raw_phone)
    domain = (cand.get("domain") or "Engineering").strip()
    app_id = cand.get("app_id")
    offer_id = cand.get("offer_letter_id")

    # Exclude Muguntharajan K (or any candidate already sent to today)
    if phone in sent_phones or "muguntharajan" in email:
        print(f"SKIPPING already contacted candidate: {name} ({email}, {phone})")
        continue

    msg = format_message(name, domain)
    lines = msg.split("\n")

    # Verify Line 8 and Line 11
    assert lines[7] == PORTAL_OFFER_URL, f"Line 8 must be offer url, got: {lines[7]}"
    assert lines[10] == GOOGLE_FORM_URL, f"Line 11 must be form url, got: {lines[10]}"

    queue.append({
        "app_id": app_id,
        "name": name,
        "email": email,
        "phone": phone,
        "domain": domain,
        "offer_letter_id": offer_id,
        "message": msg
    })

print(f"\nTotal Candidates in Selection Queue: {len(queue)}")
for i, q in enumerate(queue, 1):
    print(f"{i}. App ID {q['app_id']}: {q['name']} | {q['phone']} | {q['domain']} | {q['offer_letter_id']}")

with open(OUTPUT_QUEUE, "w", encoding="utf-8") as f:
    json.dump(queue, f, indent=2)

print(f"\nSaved queue to {OUTPUT_QUEUE}")
