#!/usr/bin/env python3
"""
Inspect all 5 Google Workspace inboxes via IMAP and print all unread/recent emails.
"""

import os
import sys
import email
from email.header import decode_header
from email.utils import parseaddr
import imaplib
from pathlib import Path

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

def main():
    service = EmailDeliveryService()
    print("=" * 76)
    print(f"  INSPECTING INBOXES ACROSS {len(service.pool.accounts)} GOOGLE WORKSPACE ACCOUNTS")
    print("=" * 76)

    for idx, acc in enumerate(service.pool.accounts, 1):
        print(f"\n[{idx}/5] Account: {acc.from_name} <{acc.email}>")
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=15)
            mail.login(acc.email, acc.app_password)
            mail.select("INBOX", readonly=True)

            status, search_res = mail.search(None, "UNSEEN")
            if status != "OK" or not search_res or not search_res[0]:
                print("  Status: Connected | Unread messages: 0")
                mail.logout()
                continue

            msg_ids = search_res[0].split()
            print(f"  Status: Connected | Unread messages: {len(msg_ids)}")

            for mid in msg_ids[-10:]:  # Check up to 10 latest unread
                res, data = mail.fetch(mid, "(RFC822)")
                if res != "OK" or not data or not data[0]:
                    continue
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)
                subj = decode_mime_header(msg.get("Subject", ""))
                from_hdr = decode_mime_header(msg.get("From", ""))
                name, sender_email = parseaddr(from_hdr)
                date_hdr = msg.get("Date", "")
                body = extract_body(msg).strip()
                preview = body[:200].replace("\n", " ")
                print(f"    - Mid {mid.decode()}: From: {name} <{sender_email}>")
                print(f"      Date: {date_hdr}")
                print(f"      Subj: {subj}")
                print(f"      Body Preview: {preview}...")

            mail.logout()
        except Exception as e:
            print(f"  Error accessing inbox: {e}")

if __name__ == "__main__":
    main()
