#!/usr/bin/env python3
"""
================================================================================
DBERT Multi-SMTP Dispatch Daemon: 2,585 Un-logged Profile Completion
================================================================================
Dispatches profile completion & enrollment notices across all 5 authenticated
Google Workspace SMTP accounts in parallel with anti-spam pacing (18s-35s).

Target Audience:
  - 2,585 Candidates from Google Sheet (gid=198139462) who have never logged on LMS.

Usage:
  # Check status:
  python scripts/dispatch_never_logged_2585_multi_smtp.py --status

  # Dry-run inspection (shows 5-way sharding without sending):
  python scripts/dispatch_never_logged_2585_multi_smtp.py --dry-run

  # Dispatch 5 test emails (one from each account) to review inbox delivery:
  python scripts/dispatch_never_logged_2585_multi_smtp.py --test-to ain.sharma.abhinav@gmail.com

  # Launch live multi-account parallel dispatch:
  python scripts/dispatch_never_logged_2585_multi_smtp.py --live
================================================================================
"""

import os
import sys
import json
import time
import ssl
import random
import smtplib
import csv
import argparse
import threading
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate, make_msgid
from pathlib import Path
from typing import Dict, List, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

COHORT_FILE = DATA_DIR / "never_logged_cohort_2585.json"
TRACKING_JSON = DATA_DIR / "dispatch_tracking_never_logged_2585.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_never_logged_2585.csv"
LOG_FILE = DATA_DIR / "dispatch_never_logged_2585.log"

TELEMETRY_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

# 5 Authenticated Google Workspace SMTP Accounts
SMTP_ACCOUNTS = [
    {
        "id": "acc_1",
        "user": "abhinav.sharma@dbert.in",
        "pass": "rsupmvvvvwrsuxuh",
        "name": "Abhinav Sharma",
        "role": "Program Head & Project Mentor"
    },
    {
        "id": "acc_2",
        "user": "manoj.kumar@dbert.in",
        "pass": "fnevtpseplwibckr",
        "name": "Manoj Kumar",
        "role": "Academic Lead & Admissions"
    },
    {
        "id": "acc_3",
        "user": "sandeep.bannu@dbert.in",
        "pass": "qtqzlmrynbcxvyjy",
        "name": "Sandeep Bannu",
        "role": "Technical Program Operations"
    },
    {
        "id": "acc_4",
        "user": "contactus@dbert.in",
        "pass": "llvmaajmrljpcwru",
        "name": "DBERT Admissions & Verification",
        "role": "Admissions & Verification Concierge"
    },
    {
        "id": "acc_5",
        "user": "pulkit.kunar@dbert.in",
        "pass": "vzefecwpggxuaztr",
        "name": "Pulkit Kumar",
        "role": "Technical Mentorship & Verification"
    }
]

tracking_lock = threading.Lock()
log_lock = threading.Lock()

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    with log_lock:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

def load_cohort() -> List[Dict[str, Any]]:
    if not COHORT_FILE.exists():
        log(f"ERROR: Cohort file not found: {COHORT_FILE}")
        sys.exit(1)
    with open(COHORT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_or_init_tracking(cohort: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    with tracking_lock:
        if TRACKING_JSON.exists():
            with open(TRACKING_JSON, "r", encoding="utf-8") as f:
                tracking = json.load(f)
        else:
            tracking = {}

        # Sync missing records
        updated = False
        for c in cohort:
            email = c["email"].lower()
            if email not in tracking:
                tracking[email] = {
                    "id": c["id"],
                    "email": email,
                    "name": c["name"],
                    "domain": c["domain"],
                    "college": c["college"],
                    "phone": c.get("phone", ""),
                    "status": "PENDING",
                    "sent_at": None,
                    "account_id": None,
                    "message_id": None,
                    "error": None
                }
                updated = True

        if updated or not TRACKING_JSON.exists():
            save_tracking_unlocked(tracking)

        return tracking

def save_tracking_unlocked(tracking: Dict[str, Dict[str, Any]]):
    with open(TRACKING_JSON, "w", encoding="utf-8") as f:
        json.dump(tracking, f, indent=2)

    with open(TRACKING_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "email", "name", "domain", "college", "status", "sent_at", "account_id", "message_id", "error"])
        for e, d in tracking.items():
            writer.writerow([
                d.get("id"), d.get("email"), d.get("name"), d.get("domain"), d.get("college"),
                d.get("status"), d.get("sent_at"), d.get("account_id"), d.get("message_id"), d.get("error")
            ])

def update_candidate_state(email: str, status: str, account_id: str, message_id: str = None, error: str = None):
    with tracking_lock:
        with open(TRACKING_JSON, "r", encoding="utf-8") as f:
            tracking = json.load(f)

        email_clean = email.lower()
        if email_clean in tracking:
            tracking[email_clean]["status"] = status
            tracking[email_clean]["sent_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == "SENT" else None
            tracking[email_clean]["account_id"] = account_id
            tracking[email_clean]["message_id"] = message_id
            tracking[email_clean]["error"] = error
            save_tracking_unlocked(tracking)

def build_profile_completion_email(candidate: Dict[str, Any], sender_account: Dict[str, str]) -> tuple:
    name = candidate.get("name", "Fellow").strip()
    first_name = candidate.get("first_name") or (name.split()[0].title() if name else "Candidate")
    domain = candidate.get("domain", "Technical Internship").strip()
    college = candidate.get("college", "").strip() or "Your College"
    email = candidate.get("email", "").strip().lower()

    sender_name = sender_account["name"]
    sender_user = sender_account["user"]
    sender_role = sender_account["role"]

    subject = f"Action Required: Complete your DBERT Internship Profile ({domain}) — {first_name}"

    plain_text = f"""DBERT TECHNICAL COUNCIL — ADMISSIONS & ONBOARDING NOTICE
Digital Blinc Education Research and Technology (https://dbert.in)

Dear {name},

We are contacting you regarding your application for the 2-Month Remote Applied Engineering Internship ({domain}).

Our admissions records indicate that your candidate application profile is currently incomplete, which is holding your batch incubation seat from being confirmed.

To finalize your enrollment and access your assigned development sandbox, please complete your profile details on the portal.

================================================================================
INTERNSHIP HIGHLIGHTS & COMPENSATION
================================================================================
• Role: Remote Applied Engineering Fellow ({domain})
• Work Model: 100% Remote (Applied Engineering Cloud Sandbox)
• Weekly Time Commitment: Flexible 10 hours/week logged engagement
• Fixed Milestone Stipend: ₹5,000 (Earned upon completing sprint milestones)
• Variable Performance Incentive: Up to ₹18,000 (Based on milestone excellence)
• Total Potential Compensation: Up to ₹23,000
• Caution Deposit: ₹499 (100% Refundable / Credited per Section 5 of Offer Letter)
• Official Credentials: Two Cryptographically Verifiable Certificates + Letter of Recommendation

================================================================================
3 SIMPLE STEPS TO COMPLETE YOUR PROFILE & ENROLLMENT:
================================================================================
Step 1: Open Your Candidate Profile Portal
Direct Link: https://dbert.in/enroll/1999?email={email}
(Or log in directly at: https://lms.dbert.in/#signin)

Step 2: Confirm Academic & Specialization Track
Verify your college name ({college}), degree course, and select your preferred batch start date.

Step 3: Review Your Appointment Terms & Seat Reservation
Review your official letter of offer and confirm your incubation sandbox seat with the ₹499 caution deposit reconciliation.

================================================================================
NEED ASSISTANCE? CONNECT WITH ADMISSIONS CONCIERGE
================================================================================
If you have questions about your track, batch timing, or onboarding:
• WhatsApp Admissions Desk: +91 81929 11360
• Direct WhatsApp Link: https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20am%20{name}%20completing%20my%20DBERT%20internship%20profile.
• Email: support@dbert.in

Sincerely,

{sender_name}
{sender_role}
DBERT Technical Council
Sovereign Portal: https://dbert.in · LMS: https://lms.dbert.in
New Delhi, India • MSME Registered: UDYAM-UP-29-0109046
"""

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DBERT Internship Profile Completion</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0B0F17; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #E2E8F0; -webkit-font-smoothing: antialiased;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #0B0F17; padding: 30px 15px;">
    <tr>
      <td align="center">
        <!-- Main Card Container -->
        <table role="presentation" width="100%" style="max-width: 620px; background-color: #111827; border: 1px solid rgba(200, 153, 69, 0.35); border-radius: 12px; overflow: hidden; box-shadow: 0 14px 40px rgba(0,0,0,0.6);" cellspacing="0" cellpadding="0" border="0">
          
          <!-- Top Accent Banner -->
          <tr>
            <td style="background: linear-gradient(135deg, #92400E 0%, #B45309 50%, #D97706 100%); padding: 12px 24px; text-align: center; border-bottom: 1px solid rgba(245, 158, 11, 0.4);">
              <span style="font-size: 11.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.12em; color: #FEF3C7;">
                ⚡ ADMISSIONS NOTICE: PROFILE COMPLETION REQUIRED
              </span>
            </td>
          </tr>

          <!-- Brand Letterhead -->
          <tr>
            <td style="padding: 26px 32px 18px 32px; text-align: center; border-bottom: 1px solid #1F2937;">
              <span style="font-size: 26px; font-weight: 900; letter-spacing: 0.1em; color: #F8FAFC;">D B E R T</span>
              <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.16em; color: #C89945; font-weight: 700; margin-top: 4px;">
                Digital Blinc Education Research & Technology
              </div>
              <div style="font-size: 10px; color: #64748B; margin-top: 2px;">Govt. of India MSME Registered: UDYAM-UP-29-0109046</div>
            </td>
          </tr>

          <!-- Hero Greeting -->
          <tr>
            <td style="padding: 30px 32px 16px 32px;">
              <div style="display: inline-block; padding: 4px 12px; background: rgba(200, 153, 69, 0.12); border: 1px solid rgba(200, 153, 69, 0.3); border-radius: 9999px; color: #F59E0B; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 14px;">
                ● Track: {domain}
              </div>
              <h2 style="margin: 0 0 12px 0; font-size: 21px; font-weight: 700; color: #FFFFFF; line-height: 1.35;">
                Hi {first_name}, Complete Your Candidate Profile
              </h2>
              <p style="margin: 0 0 14px 0; font-size: 14px; line-height: 1.65; color: #CBD5E1;">
                Thank you for applying to the <strong>2-Month Remote Applied Engineering Internship & Incubation Fellowship</strong> at DBERT.
              </p>
              <p style="margin: 0 0 18px 0; font-size: 14px; line-height: 1.65; color: #CBD5E1;">
                Our admissions portal indicates that your academic application profile is currently pending completion. Completing your profile verifies your seat reservation and provisions your dedicated cloud developer sandbox.
              </p>
            </td>
          </tr>

          <!-- Appointment Terms Overview Table -->
          <tr>
            <td style="padding: 0 32px 24px 32px;">
              <div style="background-color: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 18px 20px;">
                <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #C89945; margin-bottom: 12px;">
                  Appointment Terms at a Glance
                </div>
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="font-size: 13px; color: #E2E8F0; line-height: 1.7;">
                  <tr>
                    <td style="padding: 4px 0; color: #94A3B8; width: 44%;">Work Arrangement:</td>
                    <td style="padding: 4px 0; font-weight: 600; color: #F8FAFC;">100% Remote Cloud Sandbox</td>
                  </tr>
                  <tr>
                    <td style="padding: 4px 0; color: #94A3B8;">Weekly Commitment:</td>
                    <td style="padding: 4px 0; font-weight: 600; color: #F8FAFC;">Flexible 10 Hours / Week</td>
                  </tr>
                  <tr>
                    <td style="padding: 4px 0; color: #94A3B8;">Fixed Milestone Stipend:</td>
                    <td style="padding: 4px 0; font-weight: 700; color: #10B981;">₹5,000 (Milestone-based)</td>
                  </tr>
                  <tr>
                    <td style="padding: 4px 0; color: #94A3B8;">Performance Incentive:</td>
                    <td style="padding: 4px 0; font-weight: 700; color: #F59E0B;">Up to ₹18,000</td>
                  </tr>
                  <tr>
                    <td style="padding: 4px 0; color: #94A3B8;">Refundable Caution Deposit:</td>
                    <td style="padding: 4px 0; font-weight: 600; color: #F8FAFC;">₹499 (100% Refundable / Credited)</td>
                  </tr>
                </table>
              </div>
            </td>
          </tr>

          <!-- 3 Steps Section -->
          <tr>
            <td style="padding: 0 32px 28px 32px;">
              <div style="font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #FFFFFF; margin-bottom: 12px;">
                3 Steps to Finalize Your Enrollment
              </div>
              
              <div style="margin-bottom: 12px; padding: 12px 16px; background-color: rgba(255,255,255,0.02); border-left: 3px solid #C89945; border-radius: 4px;">
                <strong style="color: #F8FAFC; font-size: 13.5px;">1. Open Your Profile Portal</strong><br>
                <span style="font-size: 12.5px; color: #94A3B8;">Click the secure link below to open your pre-filled candidate dossier on the DBERT platform.</span>
              </div>

              <div style="margin-bottom: 12px; padding: 12px 16px; background-color: rgba(255,255,255,0.02); border-left: 3px solid #C89945; border-radius: 4px;">
                <strong style="color: #F8FAFC; font-size: 13.5px;">2. Verify Academic & Degree Details</strong><br>
                <span style="font-size: 12.5px; color: #94A3B8;">Confirm your college ({college}), semester, and choose your preferred batch start date.</span>
              </div>

              <div style="padding: 12px 16px; background-color: rgba(255,255,255,0.02); border-left: 3px solid #C89945; border-radius: 4px;">
                <strong style="color: #F8FAFC; font-size: 13.5px;">3. Review Terms & Reserve Seat</strong><br>
                <span style="font-size: 12.5px; color: #94A3B8;">Inspect your appointment letter and unlock LMS platform access.</span>
              </div>
            </td>
          </tr>

          <!-- Primary CTA Button -->
          <tr>
            <td style="padding: 0 32px 30px 32px; text-align: center;">
              <a href="https://dbert.in/enroll/1999?email={email}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #D97706 0%, #B45309 100%); color: #FFFFFF; font-size: 14.5px; font-weight: 700; text-decoration: none; padding: 14px 34px; border-radius: 8px; box-shadow: 0 4px 15px rgba(217, 119, 6, 0.4); text-transform: uppercase; letter-spacing: 0.05em;">
                Complete Candidate Profile & Confirm Seat →
              </a>
              <div style="font-size: 11.5px; color: #64748B; margin-top: 10px;">
                Or access LMS login directly: <a href="https://lms.dbert.in/#signin" style="color: #94A3B8; text-decoration: underline;">https://lms.dbert.in/#signin</a>
              </div>
            </td>
          </tr>

          <!-- Support Concierge -->
          <tr>
            <td style="padding: 0 32px 28px 32px;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 16px; text-align: center;">
                <tr>
                  <td>
                    <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #10B981; font-weight: 700;">
                      💬 Admissions & Student Support Desk
                    </div>
                    <div style="font-size: 13px; color: #E2E8F0; margin: 6px 0 10px 0;">
                      Have questions regarding track selection, stipend, or timing?
                    </div>
                    <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20am%20{name}%20completing%20my%20DBERT%20internship%20profile." target="_blank" style="display: inline-block; background-color: #059669; color: #FFFFFF; font-size: 12px; font-weight: 700; text-decoration: none; padding: 8px 20px; border-radius: 6px;">
                      Chat on WhatsApp (+91 81929 11360) →
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Signatory Footer -->
          <tr>
            <td style="padding: 24px 32px 28px 32px; border-top: 1px solid #1E293B; background-color: #0B0F17; text-align: center;">
              <p style="margin: 0 0 4px 0; font-size: 13.5px; font-weight: 700; color: #F1F5F9;">{sender_name}</p>
              <p style="margin: 0 0 12px 0; font-size: 12px; color: #64748B;">{sender_role} · DBERT Technical Council</p>
              <div style="font-size: 11px; color: #475569; line-height: 1.6;">
                Digital Blinc Education Research and Technology · New Delhi, India<br>
                Official Sovereign Portal: <a href="https://dbert.in" style="color: #64748B; text-decoration: underline;">https://dbert.in</a> · LMS: <a href="https://lms.dbert.in" style="color: #64748B; text-decoration: underline;">https://lms.dbert.in</a><br>
                <span style="font-size: 10px; color: #334155; margin-top: 6px; display: inline-block;">You received this notification regarding your active internship application on record.</span>
              </div>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    return subject, plain_text, html_body

def send_smtp_message(sender_account: Dict[str, str], recipient_email: str, subject: str, plain_text: str, html_body: str) -> str:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr((sender_account["name"], sender_account["user"]))
    msg["To"] = recipient_email
    msg["Reply-To"] = sender_account["user"]
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")

    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx, timeout=25) as server:
        server.login(sender_account["user"], sender_account["pass"])
        server.sendmail(sender_account["user"], [recipient_email], msg.as_string())

    return msg["Message-ID"]

def send_telemetry_report(delivered_count: int, total_count: int, sender_stats: Dict[str, int]):
    subject = f"[TELEMETRY] DBERT Never-Logged Dispatch: {delivered_count}/{total_count} Delivered"
    stats_lines = "\n".join([f"  • {acc_id}: {cnt} delivered" for acc_id, cnt in sender_stats.items()])
    
    body = f"""DBERT MULTI-SMTP DISPATCH TELEMETRY REPORT
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total Campaign Target: {total_count}
Delivered so far: {delivered_count} ({delivered_count/total_count*100:.1f}%)

Account Breakdown:
{stats_lines}

Tracking State: data/dispatch_tracking_never_logged_2585.json
Live Log: data/dispatch_never_logged_2585.log
"""
    # Send via sender 1
    admin_sender = SMTP_ACCOUNTS[0]
    for tel_email in TELEMETRY_EMAILS:
        try:
            send_smtp_message(
                admin_sender, tel_email, subject, body,
                f"<pre style='font-family: monospace; font-size: 13px;'>{body}</pre>"
            )
            log(f"[TELEMETRY] Report dispatched to {tel_email}")
        except Exception as e:
            log(f"[TELEMETRY ERROR] Failed sending telemetry to {tel_email}: {e}")

def worker_thread(sender_account: Dict[str, str], assigned_candidates: List[Dict[str, Any]], stats_dict: Dict[str, int]):
    acc_id = sender_account["id"]
    acc_user = sender_account["user"]
    log(f"[{acc_id}] Worker thread started for {acc_user} with {len(assigned_candidates)} candidates.")

    consecutive_errors = 0
    for idx, c in enumerate(assigned_candidates):
        email = c["email"].lower()
        
        # Check current tracking state
        with tracking_lock:
            with open(TRACKING_JSON, "r", encoding="utf-8") as f:
                tracking = json.load(f)
            if tracking.get(email, {}).get("status") == "SENT":
                continue

        subject, plain_text, html_body = build_profile_completion_email(c, sender_account)

        try:
            msg_id = send_smtp_message(sender_account, email, subject, plain_text, html_body)
            update_candidate_state(email, "SENT", acc_id, message_id=msg_id)
            consecutive_errors = 0
            stats_dict[acc_id] = stats_dict.get(acc_id, 0) + 1
            total_sent = sum(stats_dict.values())

            log(f"[{acc_id}] ({idx+1}/{len(assigned_candidates)}) SENT -> {email} ({c.get('name')}) | Total Sent: {total_sent}")

            # Telemetry check every 250 sent emails
            if total_sent > 0 and total_sent % 250 == 0:
                threading.Thread(
                    target=send_telemetry_report,
                    args=(total_sent, 2585, stats_dict.copy()),
                    daemon=True
                ).start()

        except Exception as e:
            err_msg = str(e)
            consecutive_errors += 1
            update_candidate_state(email, "FAILED", acc_id, error=err_msg)
            log(f"[{acc_id}] ERROR sending to {email}: {err_msg}")

            if "daily user sending limit" in err_msg.lower() or "550 5.4.5" in err_msg:
                log(f"[{acc_id}] CRITICAL: Google daily sending limit reached for {acc_user}. Halting thread.")
                break

            if consecutive_errors >= 3:
                log(f"[{acc_id}] Circuit breaker triggered (3 consecutive errors). Pausing 90s...")
                time.sleep(90)
                consecutive_errors = 0

        # Anti-spam natural human pacing (18s to 35s)
        delay = random.uniform(18.0, 35.0)
        time.sleep(delay)

    log(f"[{acc_id}] Worker thread finished for {acc_user}.")

def run_dry_run(cohort: List[Dict[str, Any]]):
    log("=" * 70)
    log(" DRY-RUN INSPECTION: 5-WAY MULTI-SMTP SHARDING")
    log("=" * 70)
    log(f"Total Cohort Size: {len(cohort)} candidates")
    
    shards = {acc["id"]: [] for acc in SMTP_ACCOUNTS}
    for i, c in enumerate(cohort):
        acc = SMTP_ACCOUNTS[i % len(SMTP_ACCOUNTS)]
        shards[acc["id"]].append(c)

    for acc in SMTP_ACCOUNTS:
        assigned = shards[acc["id"]]
        log(f"  Account {acc['id']} ({acc['user']}): {len(assigned)} candidates")
        if assigned:
            sample = assigned[0]
            log(f"    Sample 1: {sample['name']} | {sample['email']} | Track: {sample['domain']}")

    log("=" * 70)
    log("Dry run verified successfully. Use --live to launch parallel dispatch.")

def run_test_dispatch(test_email: str, cohort: List[Dict[str, Any]]):
    log("=" * 70)
    log(f" TEST DISPATCH: Sending 5 preview emails to {test_email}")
    log("=" * 70)

    sample_candidate = cohort[0] if cohort else {
        "name": "Abhinav Test Candidate",
        "first_name": "Abhinav",
        "domain": "Data Analyst",
        "college": "IIT Delhi",
        "email": test_email
    }

    for idx, acc in enumerate(SMTP_ACCOUNTS):
        test_c = sample_candidate.copy()
        test_c["email"] = test_email
        test_c["name"] = f"Test Recipient ({acc['name']})"
        test_c["first_name"] = "Abhinav"

        subject, plain_text, html_body = build_profile_completion_email(test_c, acc)
        subject = f"[PREVIEW #{idx+1}/5] {subject}"

        log(f"Sending test #{idx+1} from {acc['user']} -> {test_email} ...")
        try:
            msg_id = send_smtp_message(acc, test_email, subject, plain_text, html_body)
            log(f"  [SUCCESS] Sent via {acc['user']} | Message-ID: {msg_id}")
        except Exception as e:
            log(f"  [FAILED] Error sending via {acc['user']}: {e}")

        time.sleep(3)

    log("=" * 70)
    log("Test preview dispatch completed! Please check your inbox.")

def print_status(cohort: List[Dict[str, Any]]):
    tracking = load_or_init_tracking(cohort)
    total = len(cohort)
    sent = sum(1 for d in tracking.values() if d.get("status") == "SENT")
    failed = sum(1 for d in tracking.values() if d.get("status") == "FAILED")
    pending = total - sent - failed

    log("=" * 70)
    log(" DBERT NEVER-LOGGED DISPATCH STATUS")
    log("=" * 70)
    log(f"Total Cohort: {total}")
    log(f"Delivered:    {sent} ({(sent/total)*100:.1f}%)")
    log(f"Pending:      {pending}")
    log(f"Failed:       {failed}")
    log("=" * 70)

    # Per account breakdown
    acc_counts = {}
    for d in tracking.values():
        if d.get("status") == "SENT" and d.get("account_id"):
            acc_id = d["account_id"]
            acc_counts[acc_id] = acc_counts.get(acc_id, 0) + 1

    log("Sent by account:")
    for acc in SMTP_ACCOUNTS:
        log(f"  {acc['id']} ({acc['user']}): {acc_counts.get(acc['id'], 0)} sent")

def main():
    parser = argparse.ArgumentParser(description="DBERT Never-Logged 2,585 Profile Completion Multi-SMTP Dispatcher")
    parser.add_argument("--dry-run", action="store_true", help="Inspect 5-way sharding without sending")
    parser.add_argument("--test-to", type=str, help="Send 5 preview test emails to a specific email address")
    parser.add_argument("--live", action="store_true", help="Launch live multi-threaded dispatch across all 5 accounts")
    parser.add_argument("--status", action="store_true", help="Check current campaign progress")
    args = parser.parse_args()

    cohort = load_cohort()

    if args.status:
        print_status(cohort)
        return

    if args.dry_run:
        run_dry_run(cohort)
        return

    if args.test_to:
        run_test_dispatch(args.test_to, cohort)
        return

    if not args.live:
        parser.print_help()
        return

    log("=" * 70)
    log(" LAUNCHING LIVE 5-ACCOUNT MULTI-SMTP DISPATCH")
    log("=" * 70)

    tracking = load_or_init_tracking(cohort)
    already_sent = sum(1 for d in tracking.values() if d.get("status") == "SENT")
    log(f"Total cohort: {len(cohort)} | Already sent: {already_sent} | Remaining: {len(cohort) - already_sent}")

    # Partition cohort round-robin across all 5 accounts
    shards = {acc["id"]: [] for acc in SMTP_ACCOUNTS}
    for i, c in enumerate(cohort):
        acc = SMTP_ACCOUNTS[i % len(SMTP_ACCOUNTS)]
        shards[acc["id"]].append(c)

    stats_dict = {acc["id"]: 0 for acc in SMTP_ACCOUNTS}
    threads = []

    for acc in SMTP_ACCOUNTS:
        assigned = shards[acc["id"]]
        t = threading.Thread(
            target=worker_thread,
            args=(acc, assigned, stats_dict),
            name=f"worker-{acc['id']}"
        )
        threads.append(t)
        t.start()
        # Stagger startup to avoid simultaneous connection bursts
        time.sleep(3.5)

    log(f"All {len(threads)} worker threads active. Monitoring progress...")

    for t in threads:
        t.join()

    total_sent = sum(stats_dict.values())
    log("=" * 70)
    log(f"DISPATCH MISSION COMPLETE: {total_sent} messages delivered in this session.")
    log("=" * 70)

    # Final Telemetry Report
    send_telemetry_report(already_sent + total_sent, len(cohort), stats_dict)

if __name__ == "__main__":
    main()
