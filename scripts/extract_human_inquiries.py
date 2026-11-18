#!/usr/bin/env python3
"""
Filter and extract all real human incoming messages from candidates across all 5 accounts.
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
    "indeed.com", "dmarcreport", "dmarc", "claude.com", "github.com"
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
    human_inquiries = []

    for acc in service.pool.accounts:
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=15)
            mail.login(acc.email, acc.app_password)
            mail.select("INBOX", readonly=True)

            status, search_res = mail.search(None, "ALL")
            if status != "OK" or not search_res or not search_res[0]:
                mail.logout()
                continue

            msg_ids = search_res[0].split()
            # Check last 50 messages per account
            for mid in msg_ids[-50:]:
                res, data = mail.fetch(mid, "(RFC822)")
                if res != "OK" or not data or not data[0]:
                    continue
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                subj = decode_mime_header(msg.get("Subject", ""))
                from_hdr = decode_mime_header(msg.get("From", ""))
                name, sender_email = parseaddr(from_hdr)
                sender_email = sender_email.strip().lower()
                date_hdr = msg.get("Date", "")
                message_id = msg.get("Message-ID", "").strip()

                if any(sup in sender_email for sup in SUPPRESSED_SENDERS):
                    continue

                raw_body = extract_body(msg)
                clean_body = strip_quoted_reply(raw_body)
                if not clean_body:
                    continue

                human_inquiries.append({
                    "account": acc.email,
                    "account_from_name": acc.from_name,
                    "mid": mid.decode(),
                    "message_id": message_id,
                    "sender_name": name,
                    "sender_email": sender_email,
                    "date": date_hdr,
                    "subject": subj,
                    "clean_body": clean_body
                })

            mail.logout()
        except Exception as e:
            print(f"Error checking {acc.email}: {e}")

    with open("data/detected_human_inquiries.json", "w", encoding="utf-8") as f:
        json.dump(human_inquiries, f, indent=2, ensure_ascii=False)

    print(f"Found {len(human_inquiries)} candidate/human messages.")
    for idx, item in enumerate(human_inquiries, 1):
        print(f"\n[{idx}] To: {item['account']} | From: {item['sender_name']} <{item['sender_email']}>")
        print(f"    Date: {item['date']}")
        print(f"    Subject: {item['subject']}")
        print(f"    Body: {repr(item['clean_body'][:150])}")

if __name__ == "__main__":
    main()
