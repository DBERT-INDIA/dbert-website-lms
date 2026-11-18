#!/usr/bin/env python3
"""
Fast fetch of UNSEEN candidate inquiries across all 5 accounts.
"""

import os
import sys
import email
from email.header import decode_header
from email.utils import parseaddr
import imaplib
from pathlib import Path
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

# Load .env
env_file = PORTAL_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k not in os.environ:
                    os.environ[k] = v

from services.delivery_service import EmailDeliveryService

SUPPRESSED_SENDERS = [
    "mailer-daemon", "postmaster", "no-reply", "noreply",
    "google.com", "accounts.google.com", "googlemail.com",
    "dbert.in", "ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com",
    "indeed.com", "dmarcreport", "dmarc", "claude.com", "github.com",
    "calendar-notification@google.com"
]

def decode_mime_header(header_val: str) -> str:
    if not header_val:
        return ""
    decoded_parts = decode_header(header_val)
    res = []
    for part, enc in decoded_parts:
        if isinstance(part, bytes):
            res.append(part.decode(enc or "utf-8", errors="ignore"))
        else:
            res.append(str(part))
    return "".join(res)

def extract_body(msg) -> str:
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdisp = str(part.get("Content-Disposition", ""))
            if ctype == "text/plain" and "attachment" not in cdisp:
                payload = part.get_payload(decode=True)
                if payload:
                    body += payload.decode("utf-8", errors="ignore") + "\n"
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode("utf-8", errors="ignore")
    return body

def strip_quoted_reply(body: str) -> str:
    lines = body.splitlines()
    clean = []
    for line in lines:
        l_str = line.strip()
        if l_str.startswith(">"):
            continue
        if l_str.startswith("On ") and ("wrote:" in l_str or "wrote :" in l_str):
            break
        if "---------- Forwarded message ---------" in l_str:
            break
        if "________________________________" in l_str:
            break
        clean.append(line)
    return "\n".join(clean).strip()

def main():
    service = EmailDeliveryService()
    inquiries = []

    print("=" * 76)
    print("  SCANNING UNSEEN INBOX MESSAGES ACROSS 5 GOOGLE WORKSPACE ACCOUNTS")
    print("=" * 76)

    for idx, acc in enumerate(service.pool.accounts, 1):
        print(f"\n[{idx}/5] Checking {acc.from_name} <{acc.email}>...")
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=15)
            mail.login(acc.email, acc.app_password)
            mail.select("INBOX", readonly=True)

            status, search_res = mail.search(None, "UNSEEN")
            if status != "OK" or not search_res or not search_res[0]:
                print("  No unseen messages.")
                mail.logout()
                continue

            msg_ids = search_res[0].split()
            print(f"  Total unseen: {len(msg_ids)}")

            for mid in msg_ids:
                # Fetch headers only
                res, data = mail.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE MESSAGE-ID)])")
                if res != "OK" or not data or not data[0]:
                    continue
                header_data = data[0][1]
                hdr_msg = email.message_from_bytes(header_data)
                
                from_hdr = decode_mime_header(hdr_msg.get("From", ""))
                name, sender_email = parseaddr(from_hdr)
                sender_email = sender_email.strip().lower()
                subj = decode_mime_header(hdr_msg.get("Subject", ""))
                date_hdr = hdr_msg.get("Date", "")
                msg_id = hdr_msg.get("Message-ID", "").strip()

                if any(sup in sender_email for sup in SUPPRESSED_SENDERS):
                    continue

                # It is a real human/candidate! Fetch full body
                res_b, data_b = mail.fetch(mid, "(RFC822)")
                full_body = ""
                clean_body = ""
                if res_b == "OK" and data_b and data_b[0]:
                    full_msg = email.message_from_bytes(data_b[0][1])
                    full_body = extract_body(full_msg)
                    clean_body = strip_quoted_reply(full_body)

                inquiries.append({
                    "account": acc.email,
                    "account_from_name": acc.from_name,
                    "mid": mid.decode(),
                    "message_id": msg_id,
                    "sender_name": name,
                    "sender_email": sender_email,
                    "date": date_hdr,
                    "subject": subj,
                    "clean_body": clean_body,
                    "full_body_snippet": full_body[:300]
                })

            mail.logout()
        except Exception as e:
            print(f"  Error checking {acc.email}: {e}")

    with open("data/active_unseen_inquiries.json", "w", encoding="utf-8") as f:
        json.dump(inquiries, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE] Found {len(inquiries)} active human inquiries requiring response.")
    for i, inq in enumerate(inquiries, 1):
        print(f"\n--- Inquiry #{i} ---")
        print(f"To: {inq['account']}")
        print(f"From: {inq['sender_name']} <{inq['sender_email']}>")
        print(f"Date: {inq['date']}")
        print(f"Subject: {inq['subject']}")
        print(f"Body: {repr(inq['clean_body'])}")

if __name__ == "__main__":
    main()
