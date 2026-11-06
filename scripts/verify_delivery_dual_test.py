#!/usr/bin/env python3
"""
Post-Cooldown Dual-Verification Email Runner
Target recipients:
  1. ain.sharma.abhinav@gmail.com
  2. ajnatechrpa@gmail.com

Features:
- Built-in dry-run safety (--dry-run)
- Cooldown safety lock (--execute-after-cooldown required for live dispatch)
- 15-second pacing delay between recipients
- Clean MIME structure matching Test 5B (proven domain text formatting)
- Valid RFC 5322 headers (Date, Message-ID with @dbert.in domain)
"""

import sys
import time
import argparse
import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "rsupmvvvvwrsuxuh"
FROM_EMAIL = "abhinav.sharma@dbert.in"

TARGETS = [
    ("ain.sharma.abhinav@gmail.com", "Abhinav (AIN)"),
    ("ajnatechrpa@gmail.com", "AjnaTech RPA")
]

def build_email_body(name, cert_id, intern_id, domain, project, duration, score, grade):
    return f"""Dear {name},

Your official technical incubation and internship program record with DBERT has been recorded on the verification portal.

Credential Details:
- Candidate Name:        {name}
- Domain Track:          {domain}
- Program Tenure:        {duration}
- Core Project:          {project}
- Academic Evaluation:   {score}/100 ({grade})
- Certificate ID:        {cert_id}
- Permanent Intern ID:   {intern_id}

Direct Verification Portal Link:
dbert.in/verify/{cert_id}

Please visit the link above to view your complete credential dossier and review your verification status.

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
dbert.in/verify
"""

def main():
    parser = argparse.ArgumentParser(description="Deliverability Dual-Test Verification Runner")
    parser.add_argument("--dry-run", action="store_true", help="Validate message generation without SMTP dispatch")
    parser.add_argument("--execute-after-cooldown", action="store_true", help="Acknowledge cooldown has completed and proceed with live send")
    args = parser.parse_args()

    name = "Badugu venkata rajesh"
    cert_id = "CERT-DBERT-2026-DA-057"
    intern_id = "DBERT-2026-INT-1000"
    domain = "Data Analyst"
    project = "Cognitive Solutions"
    duration = "15 Aug 2026 - 15 Oct 2026"
    score = 88
    grade = "Grade A (Very Good)"

    body = build_email_body(name, cert_id, intern_id, domain, project, duration, score, grade)

    print("=================================================================")
    print("      DBERT DUAL-TEST EMAIL VERIFICATION RUNNER")
    print("=================================================================")
    print(f"SMTP Server: {SMTP_HOST}:{SMTP_PORT}")
    print(f"Sender:      Abhinav Sharma <{FROM_EMAIL}>")
    print(f"Targets:     {[t[0] for t in TARGETS]}")
    print("-----------------------------------------------------------------")

    if args.dry_run:
        print("[DRY-RUN MODE ACTIVE] Verifying payload generation only...")
        for email_addr, label in TARGETS:
            msg = MIMEText(body, "plain", "utf-8")
            msg["Subject"] = f"DBERT Internship Verification: {name} [{cert_id}]"
            msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
            msg["To"] = email_addr
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid(domain="dbert.in")
            print(f"  [OK] Payload generated for {label} <{email_addr}> ({len(msg.as_string())} bytes)")
        print("\n[SUCCESS] Dry-run verification complete. 0 network calls made.")
        return

    if not args.execute_after_cooldown:
        print("[COOLDOWN LOCK ACTIVE]")
        print("To protect domain reputation, live dispatch is locked during cooldown.")
        print("When cooldown is complete, re-run with:")
        print("    python scripts/verify_delivery_dual_test.py --execute-after-cooldown")
        return

    print("[LIVE DISPATCH COMMENCING] Connecting to SMTP server...")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(SMTP_USER, SMTP_PASS)
        print("  [OK] Authenticated successfully with Google Workspace SMTP.")

        for i, (email_addr, label) in enumerate(TARGETS):
            msg = MIMEText(body, "plain", "utf-8")
            msg["Subject"] = f"DBERT Internship Verification: {name} [{cert_id}]"
            msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
            msg["To"] = email_addr
            msg["Date"] = formatdate(localtime=True)
            msg_id = make_msgid(domain="dbert.in")
            msg["Message-ID"] = msg_id

            print(f"\n[{i+1}/{len(TARGETS)}] Dispatching to {label} ({email_addr})...")
            print(f"  Message-ID: {msg_id}")
            res = server.sendmail(FROM_EMAIL, [email_addr], msg.as_string())
            print(f"  SMTP Status: 250 Accepted (result={res})")

            if i < len(TARGETS) - 1:
                print("  Enforcing 15-second inter-recipient spacing delay...")
                time.sleep(15)

    print("\n=================================================================")
    print("[COMPLETED] Both test emails have been submitted to Google SMTP.")
    print("Please inspect Primary Inboxes for both accounts:")
    print("  1. ain.sharma.abhinav@gmail.com")
    print("  2. ajnatechrpa@gmail.com")
    print("=================================================================")

if __name__ == "__main__":
    main()
