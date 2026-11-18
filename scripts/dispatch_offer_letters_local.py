#!/usr/bin/env python3
"""
================================================================================
DBERT Local Offer Letter Email Dispatch Bot
================================================================================
Dispatches official appointment and offer letter notifications to candidates 
who have confirmed their seat with the ₹499 caution deposit.

Strict Local Execution:
  - Connects strictly from local terminal via Google Workspace SMTP (smtp.gmail.com:465).
  - Authenticated default sender: manoj.kumar@dbert.in (Academic Lead & Admissions).
  - RFC-compliant MIME multipart (HTML + plain text fallback).
  - Anti-spam pacing (configurable 15s-60s human delays).
  - Persistent JSON/CSV idempotency tracking (never double-sends).
  - Directs candidates to log into LMS (https://lms.dbert.in/portal) to sign and download PDF.

Usage Examples:
  # Check eligible queue counts and tracking status:
  python scripts/dispatch_offer_letters_local.py --stats

  # Dry-run inspection (previews candidate batch & HTML without sending):
  python scripts/dispatch_offer_letters_local.py --dry-run

  # Dispatch 1 sample test email to your personal inbox:
  python scripts/dispatch_offer_letters_local.py --test-to your_email@gmail.com

  # Dispatch next 5 candidates with 30s safety pauses:
  python scripts/dispatch_offer_letters_local.py --batch 5 --delay 30

  # Continuous dispatch loop for all pending candidates:
  python scripts/dispatch_offer_letters_local.py --all --delay 30
================================================================================
"""

import os
import sys
import json
import time
import uuid
import smtplib
import sqlite3
import argparse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, formataddr
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "apps" / "portal" / "internship.db"
TRACKING_JSON = PROJECT_ROOT / "data" / "dispatch_tracking_offers.json"
TRACKING_CSV = PROJECT_ROOT / "data" / "dispatch_tracking_offers.csv"
LOG_PATH = PROJECT_ROOT / "data" / "dispatch_offers.log"

DEFAULT_SENDER = "manoj.kumar@dbert.in"
DEFAULT_PASSWORD = os.environ.get("GOOGLE_SMTP_PASS", "fnevtpseplwibckr")
DEFAULT_SENDER_NAME = "Manoj Kumar | Admissions & Academic Council, DBERT"
DEFAULT_REPLY_TO = "manoj.kumar@dbert.in"

COMMUNITY_WHATSAPP_URL = "https://chat.whatsapp.com/Kn6o6hMoFfc7rIVx0wgZt3"
ADMISSIONS_WHATSAPP_URL = "https://wa.me/918192911360"


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {msg}"
    print(entry)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


def load_tracking() -> list:
    if TRACKING_JSON.exists():
        try:
            with open(TRACKING_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception as e:
            log(f"[WARN] Failed to load tracking JSON: {e}")
    return []


def save_tracking(records: list):
    TRACKING_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKING_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    # Export CSV mirror
    try:
        import csv
        with open(TRACKING_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "email", "name", "domain", "status", "sent_at", "message_id", "sender"])
            for r in records:
                writer.writerow([
                    r.get("id"), r.get("email"), r.get("name"), r.get("domain"),
                    r.get("status"), r.get("sent_at"), r.get("message_id"), r.get("sender")
                ])
    except Exception as e:
        log(f"[WARN] Failed to export tracking CSV: {e}")


def get_sent_emails_set() -> set:
    records = load_tracking()
    return set(r.get("email", "").strip().lower() for r in records if r.get("status") == "SENT")


def get_eligible_candidates() -> list:
    """Queries internship.db for candidates who paid/verified ₹499 caution deposit."""
    if not DB_PATH.exists():
        log(f"[ERROR] Database file not found at: {DB_PATH}")
        return []

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    query = """
        SELECT id, name, email, phone, college, domain, joining_date, payment_status, amount, product, utr
        FROM enrollments
        WHERE (amount = 499 OR payment_status IN ('Verified', 'Accepted', 'approved'))
          AND payment_status NOT IN ('Rejected', 'Pending Verification', 'pending')
          AND email IS NOT NULL AND TRIM(email) != ''
        ORDER BY 
          CASE WHEN payment_status IN ('Verified', 'Accepted', 'approved') THEN 0 ELSE 1 END,
          id ASC
    """
    rows = conn.execute(query).fetchall()
    conn.close()

    candidates = []
    seen = set()
    for r in rows:
        em = (r["email"] or "").strip().lower()
        if not em or em in seen:
            continue
        seen.add(em)
        candidates.append({
            "id": r["id"],
            "name": (r["name"] or "Fellow").strip(),
            "email": em,
            "phone": r["phone"] or "",
            "college": r["college"] or "Verified University",
            "domain": r["domain"] or "Applied Engineering",
            "joining_date": (r["joining_date"] or "2026-11-09").split()[0],
            "payment_status": r["payment_status"] or "Verified",
            "amount": r["amount"] or 499
        })
    return candidates


def build_offer_email(candidate: dict, sender_account: dict) -> tuple:
    name = candidate.get("name", "Fellow").strip()
    email = candidate.get("email", "").strip()
    domain = candidate.get("domain", "Applied Engineering").strip()
    college = candidate.get("college", "Verified University").strip()
    joining_date = candidate.get("joining_date", "Monday, 6:00 PM IST")

    subject = f"OFFICIAL OFFER LETTER & APPOINTMENT: DBERT Remote Fellowship (₹5,000 Stipend Track) — {name}"

    msg = MIMEMultipart("alternative")
    domain_part = sender_account["user"].split("@")[-1] if "@" in sender_account["user"] else "dbert.in"
    msg_id = f"<{uuid.uuid4()}@{domain_part}>"
    msg["Message-ID"] = msg_id
    msg["From"] = formataddr((sender_account["name"], sender_account["user"]))
    msg["To"] = formataddr((name, email))
    msg["Reply-To"] = sender_account.get("reply_to", sender_account["user"])
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg["X-Entity-Ref-ID"] = f"dbert-offer-{candidate.get('id', 'cand')}"
    msg["Auto-Submitted"] = "auto-generated"

    body_text = f"""DBERT TECHNICAL COUNCIL — OFFICIAL INTERNSHIP APPOINTMENT
MSME Udyam: UDYAM-UP-29-0109046 | National Technology Incubation Initiative

Dear {name},

Congratulations! Following the reconciliation and verification of your ₹499 caution deposit, the DBERT Technical Council is pleased to formally extend your Letter of Offer for the 2-Month Remote Internship in {domain}.

APPOINTMENT & TENURE HIGHLIGHTS:
- Candidate Name: {name} ({college})
- Domain Track: {domain}
- Tenure: Two (2) Months — Fully Remote
- Batch Commencement: {joining_date}
- Fixed Internship Stipend: ₹5,000 (Subject to milestone completion)
- Seat Caution Deposit: ₹499 Paid & Verified (100% Credited / Refundable)

STIPEND ELIGIBILITY CRITERIA (₹5,000):
1. Minimum 10 hours per week login attendance recorded on the LMS.
2. Complete at least 2 course certifications on the LMS platform.
3. Complete at least 75 bounty tasks reviewed and accepted by mentors.

HOW TO REVIEW & DIGITALLY SIGN YOUR OFFER LETTER:
1. Log into your LMS student dashboard at:
   https://lms.dbert.in/portal
2. Go to the "Offer Letter" tab in your navigation.
3. Review your complete 16-section appointment terms.
4. Type your full legal name to execute your digital signature.
5. Download and print your official signed A4 PDF document.

JOIN YOUR COHORT WHATSAPP COMMUNITY:
{COMMUNITY_WHATSAPP_URL}

For questions or admissions support, reply directly to this email or chat with our Admissions Desk at +91 81929 11360.

Warm regards,
{sender_account['name']}
DBERT Technical Council | https://dbert.in
"""

    body_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{subject}</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; color: #0f172a; margin: 0; padding: 24px 12px;">
  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 620px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #cbd5e1; box-shadow: 0 4px 12px rgba(0,0,0,0.06);">
    <!-- Header -->
    <tr>
      <td style="background-color: #0f172a; padding: 32px 28px; text-align: left; border-bottom: 3px solid #059669;">
        <div style="color: #34d399; font-size: 11px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">
          DBERT TECHNICAL COUNCIL &bull; MSME UDYAM-UP-29-0109046
        </div>
        <div style="display: inline-block; background-color: rgba(16, 185, 129, 0.2); border: 1px solid #10b981; color: #10b981; font-size: 10px; font-weight: 800; padding: 4px 12px; border-radius: 9999px; letter-spacing: 0.5px; margin-bottom: 12px; text-transform: uppercase;">
          ✓ OFFICIAL APPOINTMENT &bull; SEAT CONFIRMED
        </div>
        <h1 style="color: #ffffff; font-size: 21px; margin: 0; font-weight: 800; line-height: 1.35;">
          Official Offer of Internship ({domain})
        </h1>
      </td>
    </tr>

    <!-- Body Content -->
    <tr>
      <td style="padding: 28px 24px;">
        <p style="font-size: 15px; margin: 0 0 14px; color: #0f172a;">Dear <strong>{name}</strong>,</p>
        <p style="font-size: 13.5px; line-height: 1.6; color: #334155; margin: 0 0 18px;">
          Congratulations! Following the reconciliation and verification of your <strong>₹499 seat caution deposit</strong>, the Admissions Council of <strong>DBERT Technical Council</strong> is pleased to formally extend your official Letter of Offer for the <strong>{domain}</strong> remote incubation fellowship.
        </p>

        <!-- Terms Breakdown Card -->
        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #059669; border-radius: 6px; padding: 18px; margin: 20px 0;">
          <div style="font-size: 11px; font-weight: 800; color: #059669; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
            Official Appointment Details
          </div>
          <table width="100%" style="font-size: 12.5px; color: #1e293b; border-collapse: collapse;">
            <tr>
              <td style="padding: 5px 0; color: #64748b; width: 40%;">Candidate Name</td>
              <td style="padding: 5px 0; font-weight: 700; color: #0f172a;">{name}</td>
            </tr>
            <tr>
              <td style="padding: 5px 0; color: #64748b;">Academic Institution</td>
              <td style="padding: 5px 0; color: #334155;">{college}</td>
            </tr>
            <tr>
              <td style="padding: 5px 0; color: #64748b;">Domain Track</td>
              <td style="padding: 5px 0; font-weight: 700; color: #059669;">{domain}</td>
            </tr>
            <tr>
              <td style="padding: 5px 0; color: #64748b;">Tenure &amp; Mode</td>
              <td style="padding: 5px 0; color: #0f172a;"><strong>2 Months</strong> &bull; Fully Remote</td>
            </tr>
            <tr>
              <td style="padding: 5px 0; color: #64748b;">Batch Kickoff</td>
              <td style="padding: 5px 0; font-weight: 700; color: #0f172a;">{joining_date}</td>
            </tr>
            <tr>
              <td style="padding: 5px 0; color: #64748b;">Caution Deposit</td>
              <td style="padding: 5px 0; color: #059669; font-weight: 700;">₹499 (100% Credited / Refundable)</td>
            </tr>
            <tr>
              <td style="padding: 5px 0; color: #64748b;">Fixed Stipend</td>
              <td style="padding: 5px 0; font-weight: 800; color: #0f172a;">₹5,000 (Based on Milestone Criteria below)</td>
            </tr>
          </table>
        </div>

        <!-- 3 Milestone Criteria -->
        <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 16px 18px; margin: 18px 0;">
          <div style="font-size: 12px; font-weight: 800; color: #15803d; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
            🎯 ₹5,000 Stipend Qualification Milestones:
          </div>
          <ol style="margin: 0; padding-left: 20px; font-size: 12.5px; color: #166534; line-height: 1.6;">
            <li><strong>Weekly Login Attendance:</strong> Maintain at least 10 logged hours/week on the LMS portal.</li>
            <li><strong>Course Certifications:</strong> Successfully complete at least 2 course certifications on the platform.</li>
            <li><strong>Bounty Task Sprints:</strong> Complete at least 75 mentor-reviewed bounty tasks.</li>
          </ol>
        </div>

        <!-- CTA Button -->
        <div style="text-align: center; margin: 28px 0;">
          <a href="https://lms.dbert.in/portal" style="display: inline-block; background: linear-gradient(135deg, #059669, #047857); color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 700; padding: 14px 28px; border-radius: 8px; box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3);">
            Login to LMS &amp; Review Offer Letter &rarr;
          </a>
        </div>

        <p style="font-size: 12px; color: #64748b; line-height: 1.5; text-align: center; margin: 0 0 20px;">
          Log in with your registered email (<code>{email}</code>) to review your 16-section agreement, type your legal name to digitally sign, and download your official signed PDF document.
        </p>

        <!-- WhatsApp Community -->
        <div style="border-top: 1px solid #e2e8f0; padding-top: 18px; margin-top: 24px;">
          <div style="font-size: 12px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">
            👥 Official Cohort WhatsApp Community:
          </div>
          <p style="font-size: 12px; color: #475569; margin: 0 0 10px;">
            Connect with your fellow domain interns, mentors, and batch coordinators before kickoff:
          </p>
          <a href="{COMMUNITY_WHATSAPP_URL}" style="display: inline-block; background-color: #25d366; color: #ffffff; text-decoration: none; font-size: 12px; font-weight: 700; padding: 8px 16px; border-radius: 6px;">
            Join Cohort Community &rarr;
          </a>
        </div>
      </td>
    </tr>

    <!-- Footer -->
    <tr>
      <td style="background-color: #f8fafc; border-top: 1px solid #e2e8f0; padding: 20px 24px; text-align: left; font-size: 11px; color: #64748b; line-height: 1.6;">
        <strong>DBERT Technical Council &bull; Admissions &amp; Academic Board</strong><br>
        MSME Registered Entity (Udyam: UDYAM-UP-29-0109046)<br>
        Admissions Support: <a href="mailto:manoj.kumar@dbert.in" style="color: #059669; text-decoration: none;">manoj.kumar@dbert.in</a> &bull; WhatsApp: +91 81929 11360 &bull; <a href="https://dbert.in" style="color: #059669; text-decoration: none;">https://dbert.in</a>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    msg.attach(MIMEText(body_html, "html", "utf-8"))
    return msg, msg_id


def connect_smtp(user: str, password: str) -> smtplib.SMTP_SSL:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30)
    server.login(user, password)
    return server


def print_banner(sender_email: str):
    print("=" * 76)
    print("       DBERT LOCAL OFFER LETTER DISPATCH BOT (GOOGLE WORKSPACE SMTP)")
    print(f"  Sender Account   : {sender_email}")
    print(f"  Delivery Route   : smtp.gmail.com:465 (SSL)")
    print(f"  Document Terms   : 2 Months Remote | Fixed ₹5,000 Stipend | ₹499 Verified")
    print(f"  Destination      : https://lms.dbert.in/portal/offer")
    print("=" * 76)


def main():
    parser = argparse.ArgumentParser(description="DBERT Local Offer Letter Email Dispatch Bot")
    parser.add_argument("--stats", action="store_true", help="Display queue status and sent statistics")
    parser.add_argument("--dry-run", action="store_true", help="Preview eligible candidates without sending emails")
    parser.add_argument("--test-to", type=str, metavar="EMAIL", help="Dispatch 1 test sample to the specified inbox")
    parser.add_argument("--batch", type=int, default=0, help="Dispatch next N candidates (e.g. --batch 10)")
    parser.add_argument("--all", action="store_true", help="Dispatch to all pending eligible candidates")
    parser.add_argument("--delay", type=float, default=30.0, help="Delay in seconds between consecutive dispatches (default: 30.0)")
    parser.add_argument("--sender", type=str, default=DEFAULT_SENDER, help=f"Google Workspace sender email (default: {DEFAULT_SENDER})")
    parser.add_argument("--password", type=str, default=DEFAULT_PASSWORD, help="Google Workspace App Password")

    args = parser.parse_args()

    sender_account = {
        "user": args.sender,
        "pass": args.password,
        "name": DEFAULT_SENDER_NAME,
        "reply_to": DEFAULT_REPLY_TO
    }

    print_banner(sender_account["user"])

    # 1. Fetch eligible candidates & sent tracking
    eligible = get_eligible_candidates()
    sent_set = get_sent_emails_set()
    pending = [c for c in eligible if c["email"] not in sent_set]

    # Mode 1: Stats
    if args.stats or (not args.dry_run and not args.test_to and args.batch == 0 and not args.all):
        print("\nEligible Queue Status (Candidates with ₹499 Paid/Verified):")
        print(f"  * Total Eligible Candidates In DB : {len(eligible)}")
        print(f"  * Previously Dispatched (SENT)    : {len(sent_set)}")
        print(f"  * Pending Dispatches Remaining    : {len(pending)}\n")
        if pending:
            print("Next 5 Pending Candidates:")
            for idx, c in enumerate(pending[:5], 1):
                print(f"  {idx}. {c['name']:<24} | {c['email']:<28} | {c['domain']:<22} | ₹{c['amount']}")
            print()
        return

    # Mode 2: Dry Run
    if args.dry_run:
        print("\n[DRY RUN] Inspecting next candidate payload without dispatching...")
        sample_cand = pending[0] if pending else (eligible[0] if eligible else {
            "id": 9999,
            "name": "Candidate Preview",
            "email": "candidate@example.com",
            "college": "Delhi Technological University",
            "domain": "Full Stack Web Development",
            "joining_date": "2026-11-09",
            "amount": 499
        })
        msg, msg_id = build_offer_email(sample_cand, sender_account)
        print(f"  Recipient  : {msg['To']}")
        print(f"  Subject    : {msg['Subject']}")
        print(f"  Message-ID : {msg_id}")
        print(f"  Eligible Candidates in Queue: {len(eligible)} ({len(pending)} pending)")
        print("\n[OK] Dry run completed safely with zero emails dispatched.\n")
        return

    # Mode 3: Test Send
    if args.test_to:
        test_email = args.test_to.strip().lower()
        print(f"\n[TEST SEND] Dispatching live test offer letter email to: {test_email}...")
        sample_cand = {
            "id": 9999,
            "name": "Verification Reviewer",
            "email": test_email,
            "college": "National Institute of Technology",
            "domain": "Full Stack Web Development",
            "joining_date": "2026-11-09",
            "amount": 499
        }
        msg, msg_id = build_offer_email(sample_cand, sender_account)
        try:
            server = connect_smtp(sender_account["user"], sender_account["pass"])
            server.sendmail(sender_account["user"], [test_email], msg.as_string())
            server.quit()
            print(f"[SUCCESS] Test email dispatched via {sender_account['user']}!")
            print(f"  -> Message-ID: {msg_id}")
            print(f"  -> Recipient: {test_email}")
            print("-> Please check your inbox and spam folder to inspect formatting and links.\n")
        except Exception as e:
            print(f"[ERROR] Failed to dispatch test email: {e}")
        return

    # Mode 4: Batch / All Dispatch
    target_count = len(pending) if args.all else min(args.batch, len(pending))
    if target_count <= 0:
        print("\n[INFO] No pending candidates awaiting offer letter dispatch. Queue is clean!\n")
        return

    targets = pending[:target_count]
    print(f"\n[LIVE DISPATCH] Starting controlled dispatch to {len(targets)} candidates with {args.delay}s delay...\n")

    tracking_records = load_tracking()
    server = None
    sent_count = 0
    fail_count = 0

    try:
        server = connect_smtp(sender_account["user"], sender_account["pass"])
        log(f"Connected to Google Workspace SMTP as {sender_account['user']}")

        for idx, cand in enumerate(targets, 1):
            if idx > 1 and args.delay > 0:
                log(f"Pacing pause ({args.delay}s) to preserve deliverability...")
                time.sleep(args.delay)

            try:
                msg, msg_id = build_offer_email(cand, sender_account)
                server.sendmail(sender_account["user"], [cand["email"]], msg.as_string())
                now_str = datetime.now().isoformat()
                log(f"[{idx}/{len(targets)}] ✓ SENT to {cand['email']} ({cand['name']}) | MsgID: {msg_id}")

                tracking_records.append({
                    "id": cand["id"],
                    "email": cand["email"],
                    "name": cand["name"],
                    "domain": cand["domain"],
                    "status": "SENT",
                    "sent_at": now_str,
                    "message_id": msg_id,
                    "sender": sender_account["user"]
                })
                save_tracking(tracking_records)
                sent_count += 1

            except Exception as send_err:
                log(f"[{idx}/{len(targets)}] ❌ FAILED for {cand['email']}: {send_err}")
                fail_count += 1
                # Reconnect if connection was dropped
                try:
                    server.quit()
                except Exception:
                    pass
                try:
                    server = connect_smtp(sender_account["user"], sender_account["pass"])
                except Exception as reconnect_err:
                    log(f"[FATAL] SMTP Reconnection failed: {reconnect_err}")
                    break

    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass

    print("\n" + "=" * 76)
    print(f"  [DISPATCH SUMMARY] Sent: {sent_count} | Failed: {fail_count} | Remaining Pending: {len(pending) - sent_count}")
    print("=" * 76 + "\n")


if __name__ == "__main__":
    main()
