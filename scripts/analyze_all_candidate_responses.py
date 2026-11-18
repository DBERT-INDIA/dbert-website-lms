#!/usr/bin/env python3
"""
Comprehensive Candidate Reply & Inquiry Analyzer across all 5 Google Workspace inboxes.
"""

import os
import sys
import email
from email.header import decode_header
from email.utils import parseaddr
import imaplib
from pathlib import Path
import json
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

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
    "security-noreply@linkedin.com"
]

def decode_mime_header(header_val: str) -> str:
    if not header_val:
        return ""
    try:
        decoded_parts = decode_header(header_val)
        res = []
        for part, enc in decoded_parts:
            if isinstance(part, bytes):
                res.append(part.decode(enc or "utf-8", errors="ignore"))
            else:
                res.append(str(part))
        return "".join(res)
    except Exception:
        return str(header_val)

def extract_body(msg) -> str:
    body = ""
    try:
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
    except Exception:
        pass
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

def classify_intent(subject: str, body: str) -> str:
    combined = (subject + " " + body).lower()
    
    # Check for abusive/hostile
    if any(w in combined for w in ["fuck", "suck", "dick", "bitch", "scam", "fraud"]):
        return "Hostile / Abusive"
    
    # Check for not interested / decline
    if any(w in combined for w in ["not interested", "can't do this", "cannot do this", "cancel", "decline", "withdraw", "sorry for inconvenience", "remove me", "unsubscribe"]):
        return "Not Interested / Opt-Out"
    
    # Check for submission / links / done
    if any(w in combined for w in ["github.com", "completed the remaining", "unlocked all 4 milestone", "repo", "submission", "submitted"]):
        return "Milestone / Project Submission"
    
    # Check for payment / stipend questions
    if any(w in combined for w in ["payment", "pay", "stipend", "5000", "499", "offer", "deposit", "caution", "disbursement", "fee", "refund", "upi"]):
        return "Payment / Stipend Inquiry"
        
    # Check for general question / support
    if any(w in combined for w in ["info", "help", "how to", "query", "question", "details", "brief", "verify", "certificate"]):
        return "General Query / Support"
        
    return "Other Reply"

def main():
    service = EmailDeliveryService()
    print("=" * 80)
    print("  DBERT CANDIDATE RESPONSE & INBOX INQUIRY AUDIT")
    print(f"  Scanning across {len(service.pool.accounts)} Google Workspace Inboxes")
    print("=" * 80)

    all_inquiries = []
    account_stats = {}

    for idx, acc in enumerate(service.pool.accounts, 1):
        print(f"\n[{idx}/5] Connecting to {acc.from_name} <{acc.email}>...")
        account_stats[acc.email] = {"total_scanned": 0, "candidate_replies": 0}
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=30)
            mail.login(acc.email, acc.app_password)
            mail.select("INBOX", readonly=True)

            # Search messages from the last 7 days (or all messages if fewer)
            status, search_res = mail.search(None, "ALL")
            if status != "OK" or not search_res or not search_res[0]:
                print(f"  -> No messages in INBOX.")
                mail.logout()
                continue

            msg_ids = search_res[0].split()
            account_stats[acc.email]["total_scanned"] = len(msg_ids)
            print(f"  -> Found {len(msg_ids)} total messages in inbox. Scanning latest 100...")

            # Inspect latest 100 messages
            recent_ids = msg_ids[-100:]
            for mid in recent_ids:
                try:
                    res, data = mail.fetch(mid, "(RFC822)")
                    if res != "OK" or not data or not data[0]:
                        continue
                    raw_email = data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    from_hdr = decode_mime_header(msg.get("From", ""))
                    name, sender_email = parseaddr(from_hdr)
                    sender_email = sender_email.strip().lower()
                    
                    if not sender_email or any(sup in sender_email for sup in SUPPRESSED_SENDERS):
                        continue
                    
                    subj = decode_mime_header(msg.get("Subject", ""))
                    date_hdr = msg.get("Date", "")
                    message_id = msg.get("Message-ID", "").strip()
                    
                    raw_body = extract_body(msg)
                    clean_body = strip_quoted_reply(raw_body)
                    
                    if not clean_body and not subj:
                        continue
                    
                    intent = classify_intent(subj, clean_body)
                    
                    all_inquiries.append({
                        "account": acc.email,
                        "account_name": acc.from_name,
                        "mid": mid.decode(),
                        "message_id": message_id,
                        "sender_name": name,
                        "sender_email": sender_email,
                        "date": date_hdr,
                        "subject": subj,
                        "intent": intent,
                        "clean_body": clean_body,
                        "snippet": clean_body[:250].replace("\r", " ").replace("\n", " ").strip()
                    })
                    account_stats[acc.email]["candidate_replies"] += 1
                except Exception as ex:
                    continue

            mail.logout()
            print(f"  -> Discovered {account_stats[acc.email]['candidate_replies']} candidate replies in {acc.email}.")
        except Exception as e:
            print(f"  -> Error accessing {acc.email}: {e}")

    # Deduplicate by (sender_email, subject, date)
    unique_inquiries = []
    seen = set()
    for inq in all_inquiries:
        key = (inq["sender_email"], inq["subject"], inq["date"])
        if key not in seen:
            seen.add(key)
            unique_inquiries.append(inq)

    # Sort reverse chronologically if date parsable
    output_path = ROOT_DIR / "data" / "all_candidate_inbox_responses.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(unique_inquiries, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("  RESPONSE AUDIT SUMMARY")
    print("=" * 80)
    print(f"Total Unique Candidate Responses Received: {len(unique_inquiries)}")
    
    # Category Breakdown
    categories = {}
    for inq in unique_inquiries:
        cat = inq["intent"]
        categories[cat] = categories.get(cat, 0) + 1
        
    print("\n[Breakdown by Intent / Category]")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat:32s}: {count} candidate(s)")

    print("\n[Breakdown by Target Inbox]")
    for acc_email, stats in account_stats.items():
        print(f"  - {acc_email:32s}: {stats['candidate_replies']} responses (out of {stats['total_scanned']} msgs)")

    print("\n" + "=" * 80)
    print("  DETAILED LIST OF CANDIDATE RESPONSES")
    print("=" * 80)
    for idx, inq in enumerate(unique_inquiries, 1):
        print(f"\n#{idx} [{inq['intent']}]")
        print(f"  Candidate: {inq['sender_name']} <{inq['sender_email']}>")
        print(f"  To Inbox:  {inq['account']}")
        print(f"  Date:      {inq['date']}")
        print(f"  Subject:   {inq['subject']}")
        print(f"  Content:   {inq['snippet']}")

if __name__ == "__main__":
    main()
