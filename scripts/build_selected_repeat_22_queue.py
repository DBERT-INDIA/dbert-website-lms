#!/usr/bin/env python3
"""
================================================================================
DBERT — Build WhatsApp Selected Repeat 22 Queue
================================================================================
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

COHORT_FILE = DATA_DIR / "selected_under_review_cohort_125.json"
OUTPUT_QUEUE = DATA_DIR / "whatsapp_selected_repeat_22_queue.json"

TARGET_APP_IDS = [
    5314, 5301, 5330, 5195, 5196, 5266, 5221, 5203, 5146, 5351,
    5335, 5324, 5320, 5319, 5310, 5309, 5254, 5239, 5230, 5222,
    5220, 5325
]

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
    # Strict 15 lines rule: Offer URL at Line 8, Form URL at Line 11
    first_name = name.split()[0] if name else "Candidate"
    lines = [
        f"Hello {first_name},",
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

def main():
    print(f"Loading {COHORT_FILE.name}...")
    with open(COHORT_FILE, "r", encoding="utf-8") as f:
        all_cands = json.load(f)

    cand_map = {c["app_id"]: c for c in all_cands}

    queue = []
    for idx, app_id in enumerate(TARGET_APP_IDS, 1):
        cand = cand_map.get(app_id)
        if not cand:
            print(f"[WARN] App ID {app_id} not found in cohort!")
            continue

        raw_name = cand.get("name") or "Fellow"
        name = raw_name.strip()
        email = (cand.get("email") or "").strip().lower()
        raw_phone = cand.get("phone", "")
        phone = clean_phone(raw_phone)
        domain = cand.get("domain") or "Engineering"
        offer_id = cand.get("offer_letter_id")

        msg = format_message(name, domain)
        lines = msg.split("\n")

        # Verify line positions
        assert lines[7] == PORTAL_OFFER_URL, f"Line 8 must be offer url, got: {lines[7]}"
        assert lines[10] == GOOGLE_FORM_URL, f"Line 11 must be form url, got: {lines[10]}"

        queue.append({
            "serial_no": idx,
            "app_id": app_id,
            "name": name,
            "first_name": name.split()[0],
            "email": email,
            "phone": phone,
            "clean_phone": phone[-10:] if len(phone) >= 10 else phone,
            "domain": domain,
            "offer_letter_id": offer_id,
            "message": msg
        })

    with open(OUTPUT_QUEUE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)

    print(f"[✓] Generated {len(queue)} messages in {OUTPUT_QUEUE.name}")
    print("\nSample Message Snippet:")
    print("\n".join(queue[0]["message"].split("\n")[:14]))

if __name__ == "__main__":
    main()
