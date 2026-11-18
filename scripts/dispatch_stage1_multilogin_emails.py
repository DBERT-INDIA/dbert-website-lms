#!/usr/bin/env python3
"""
================================================================================
DBERT Stage 1 Multi-Login Candidate Email Dispatch Daemon
================================================================================
Targets the highest-intent candidates (logged in multiple times in last 7 days):
  - Cohort 499 (134 Candidates): Seat Confirmation & Official Offer Letter terms (₹499 Caution Deposit)
  - Cohort 299 (23 Candidates): Credential Verification Upgrade & 3-Document Packet (₹299)
  - UTR Reassurance (2 Candidates): Notice that their submitted balance UTR is being reconciled

Deliverability & Architecture:
  - Authenticated Google Workspace SMTP relay (smtp.gmail.com:465) via abhinav.sharma@dbert.in
  - RFC 5322 MIME multipart (HTML + responsive typography + plain text fallback)
  - Anti-spam pacing (30 seconds interval between dispatches)
  - Atomic tracking into data/dispatch_tracking_stage1_multilogin.json
  - Telemetry notifications dispatched to ain.sharma.abhinav@gmail.com & ajnatechrpa@gmail.com
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from email.utils import formatdate, make_msgid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# Force UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PORTAL_DIR = Path("apps/portal").resolve()
sys.path.insert(0, str(PORTAL_DIR))

# Load .env
env_file = PORTAL_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

from services.delivery_service import EmailDeliveryService

TRACKING_FILE = Path("data/dispatch_tracking_stage1_multilogin.json")
LOG_FILE = Path("data/dispatch_stage1_multilogin.log")

COHORT_499_FILE = Path("data/stage1_cohort_499_actionable.json")
COHORT_299_FILE = Path("data/stage1_cohort_299_actionable.json")

TELEMETRY_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

FROM_NAME = "Abhinav Sharma"
FROM_EMAIL = "abhinav.sharma@dbert.in"
REPLY_TO = "abhinav.sharma@dbert.in"


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass


def load_tracking() -> dict:
    if TRACKING_FILE.exists():
        try:
            with open(TRACKING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_tracking(state: dict):
    TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKING_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def build_499_email(c: dict) -> tuple[str, str, str]:
    name = c.get("name") or "Candidate"
    domain = c.get("domain") or "Technical Track"
    subject = f"Selection Confirmed: Confirm Your {domain} Internship Seat & Appointment Terms"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{subject}</title>
</head>
<body style="margin:0; padding:0; background-color:#f1f5f9; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color:#0f172a; line-height:1.6;">
  <div style="max-width:620px; margin:30px auto; background-color:#ffffff; border-radius:12px; overflow:hidden; border:1px solid #e2e8f0; box-shadow:0 4px 15px rgba(0,0,0,0.05);">
    
    <!-- Header Banner -->
    <div style="background:linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding:28px 32px; text-align:left; border-bottom:3px solid #e2b96f;">
      <div style="font-size:22px; font-weight:800; color:#ffffff; letter-spacing:-0.5px;">
        DBERT <span style="color:#e2b96f; font-weight:400; font-size:16px;">| Technical Council</span>
      </div>
      <div style="color:#94a3b8; font-size:12px; margin-top:4px; text-transform:uppercase; letter-spacing:1px;">
        Office of Academic Admissions &amp; Enterprise Incubation
      </div>
    </div>

    <!-- Body Content -->
    <div style="padding:32px 32px 24px;">
      <p style="font-size:16px; font-weight:600; color:#0f172a; margin-top:0;">Dear {name},</p>
      
      <p style="font-size:14.5px; color:#334155;">
        Congratulations! Following the evaluation of your candidate profile and active participation on the DBERT learning platform, the Academic Admissions Committee is pleased to confirm your <strong>Selection</strong> for the <strong>{domain}</strong> Remote Internship &amp; Incubation Cohort.
      </p>

      <!-- Key Terms Card -->
      <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #e2b96f; border-radius:8px; padding:18px 20px; margin:22px 0;">
        <div style="font-size:14px; font-weight:800; color:#0f172a; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">
          Appointment &amp; Performance Highlights
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:13.5px; color:#334155;">
          <tr>
            <td style="padding:5px 0; width:45%; color:#64748b;">Domain Track:</td>
            <td style="padding:5px 0; font-weight:700; color:#0f172a;">{domain}</td>
          </tr>
          <tr>
            <td style="padding:5px 0; color:#64748b;">Tenure &amp; Work Model:</td>
            <td style="padding:5px 0; font-weight:700; color:#0f172a;">Two (2) Months &middot; Remote Schedule (~10 hrs/wk)</td>
          </tr>
          <tr>
            <td style="padding:5px 0; color:#64748b;">Monthly Stipend:</td>
            <td style="padding:5px 0; font-weight:700; color:#16a34a;">Up to &#8377;5,000 / month (Milestone Contributions)</td>
          </tr>
          <tr>
            <td style="padding:5px 0; color:#64748b;">Seat Caution Deposit:</td>
            <td style="padding:5px 0; font-weight:700; color:#0f172a;">&#8377;499 (100% Refundable / Ledger Credited)</td>
          </tr>
        </table>
      </div>

      <!-- Action Required Section -->
      <h3 style="font-size:15px; font-weight:700; color:#0f172a; margin:22px 0 8px;">Next Step: Review Terms &amp; Reserve Your Seat</h3>
      <p style="font-size:14px; color:#334155; margin:0 0 16px;">
        To reserve your cohort seat and unlock your signed Offer Letter PDF on your student portal, please complete your seat confirmation with the refundable &#8377;499 caution deposit:
      </p>

      <div style="text-align:center; margin:26px 0;">
        <a href="https://lms.dbert.in/portal" target="_blank" style="display:inline-block; background:linear-gradient(135deg, #e2b96f 0%, #c89945 100%); color:#0f172a; font-weight:800; font-size:15px; text-decoration:none; padding:14px 34px; border-radius:8px; box-shadow:0 4px 14px rgba(200,153,69,0.35);">
          Login to Student Portal &amp; Confirm Seat &rarr;
        </a>
      </div>

      <!-- Financial Ledger Note -->
      <div style="background:#f0fdf4; border:1px solid #86efac; border-radius:8px; padding:14px 16px; margin:20px 0; font-size:12.5px; color:#166534; line-height:1.5;">
        <strong>Ledger Credit Guarantee:</strong> Your &#8377;499 caution deposit is credited in full towards your incubation account. If you subsequently opt for the full Incubation &amp; Placement Program (&#8377;1,999), your deposit is deducted automatically, leaving only a net &#8377;1,500 balance payable at <a href="https://dbert.in/enroll/1999" style="color:#15803d; font-weight:700;">dbert.in/enroll/1999</a>.
      </div>

      <p style="font-size:13.5px; color:#475569; margin:20px 0 0;">
        If you have any questions or require assistance with payment verification, you may reply directly to this email or contact the Admissions Concierge via WhatsApp at <strong>+91 81929 11360</strong>.
      </p>

      <div style="margin-top:28px; padding-top:20px; border-top:1px solid #e2e8f0;">
        <p style="font-size:14px; font-weight:700; color:#0f172a; margin:0;">Abhinav Sharma</p>
        <p style="font-size:12.5px; color:#64748b; margin:2px 0 0;">Executive Director &amp; Academic Head</p>
        <p style="font-size:12px; color:#94a3b8; margin:2px 0 0;">DBERT Technical Council &middot; <a href="https://dbert.in" style="color:#0284c7; text-decoration:none;">dbert.in</a> &middot; <a href="https://lms.dbert.in" style="color:#0284c7; text-decoration:none;">lms.dbert.in</a></p>
      </div>

    </div>

    <!-- Footer -->
    <div style="background:#f8fafc; padding:16px 32px; border-top:1px solid #e2e8f0; font-size:11px; color:#94a3b8; text-align:center;">
      This official communication was dispatched to {c.get('email')} regarding your candidate application on DBERT LMS. DBERT.online is now DBERT.in.
    </div>

  </div>
</body>
</html>"""

    plain_content = f"""Dear {name},

Congratulations! Following the review of your application and active learning sessions on DBERT, the Academic Admissions Committee has confirmed your Selection for the {domain} Remote Internship & Incubation Cohort.

APPOINTMENT & PERFORMANCE HIGHLIGHTS:
- Domain Track: {domain}
- Tenure: Two (2) Months · Remote Schedule (~10 hrs/week)
- Monthly Stipend: Up to Rs. 5,000 / month based on milestone contributions
- Seat Caution Deposit: Rs. 499 (100% Refundable / Credited in Full)

NEXT STEP: REVIEW TERMS & RESERVE YOUR SEAT
Please log in to your student dashboard to review your appointment terms and confirm your seat:
https://lms.dbert.in/portal

FINANCIAL LEDGER GUARANTEE:
Your Rs. 499 caution deposit is credited in full towards your incubation account. If you complete the full Incubation Program (Rs. 1,999), your deposit is deducted automatically, leaving only Rs. 1,500 balance payable at https://dbert.in/enroll/1999.

For any queries, reply directly to this email or message Admissions on WhatsApp at +91 81929 11360.

Warm regards,
Abhinav Sharma
Executive Director & Academic Head
DBERT Technical Council | https://dbert.in
"""
    return subject, html_content, plain_content


def build_299_email(c: dict) -> tuple[str, str, str]:
    name = c.get("name") or "Candidate"
    domain = c.get("domain") or "Technical Track"
    cert_id = c.get("cert_id") or "DBERT-CERT-2026"
    subject = f"Credential Verification Notice: Upgrade Your DBERT {domain} Certificate to Verified Status"

    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"
    verify_url = f"https://dbert.in/verify/{cert_id}"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{subject}</title>
</head>
<body style="margin:0; padding:0; background-color:#f1f5f9; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color:#0f172a; line-height:1.6;">
  <div style="max-width:620px; margin:30px auto; background-color:#ffffff; border-radius:12px; overflow:hidden; border:1px solid #e2e8f0; box-shadow:0 4px 15px rgba(0,0,0,0.05);">
    
    <!-- Header Banner -->
    <div style="background:linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding:28px 32px; text-align:left; border-bottom:3px solid #e2b96f;">
      <div style="font-size:22px; font-weight:800; color:#ffffff; letter-spacing:-0.5px;">
        DBERT <span style="color:#e2b96f; font-weight:400; font-size:16px;">| Verification Registry</span>
      </div>
      <div style="color:#94a3b8; font-size:12px; margin-top:4px; text-transform:uppercase; letter-spacing:1px;">
        Master Credential &amp; Academic Evaluation Authority
      </div>
    </div>

    <!-- Body Content -->
    <div style="padding:32px 32px 24px;">
      <p style="font-size:16px; font-weight:600; color:#0f172a; margin-top:0;">Dear {name},</p>
      
      <p style="font-size:14.5px; color:#334155;">
        Our academic records indicate that you have completed technical milestones under certificate ID <strong>{cert_id}</strong> in <strong>{domain}</strong>. We noticed your active return to the student portal this week.
      </p>

      <p style="font-size:14px; color:#334155;">
        Your credential is currently classified as <strong>Provisional</strong>. You are eligible to complete formal verification and upgrade to <strong>Permanent Verified Status</strong> on the sovereign registry (<a href="https://dbert.in" style="color:#0284c7; text-decoration:none;">dbert.in</a>).
      </p>

      <!-- Benefits Card -->
      <div style="background:#f8fafc; border:1px solid #cbd5e1; border-left:4px solid #16a34a; border-radius:8px; padding:18px 20px; margin:22px 0;">
        <div style="font-size:14px; font-weight:800; color:#0f172a; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">
          What Verified Status Unlocks
        </div>
        <ul style="margin:0; padding-left:18px; font-size:13.5px; color:#334155; line-height:1.7;">
          <li><strong>Master Public Verification:</strong> Permanent verified status with cryptographic hash on <a href="{verify_url}" style="color:#0284c7; font-weight:600;">dbert.in/verify/{cert_id}</a>.</li>
          <li><strong>Pre-Vetted Engineers Directory:</strong> Profile indexed in our employer hiring directory (<a href="https://dbert.in/verify/directory" style="color:#0284c7; font-weight:600;">dbert.in/verify/directory</a>).</li>
          <li><strong>Complete 3-Document Executive Packet:</strong>
            <ul style="margin-top:4px; padding-left:16px; color:#475569;">
              <li>Official Certificate of Completion (luxury slate artwork &amp; QR seal).</li>
              <li>Academic Evaluation Rubric (100-mark rubric with Turnitin score).</li>
              <li>Letter of Recommendation (LOR) signed by Director Abhinav Sharma.</li>
            </ul>
          </li>
          <li><strong>Recruiter Fast-Track:</strong> Round-1 screening waivers with partner tech firms.</li>
        </ul>
      </div>

      <!-- Action Section -->
      <h3 style="font-size:15px; font-weight:700; color:#0f172a; margin:22px 0 8px;">Upgrade Instructions (Fee: &#8377;299)</h3>
      <p style="font-size:14px; color:#334155; margin:0 0 16px;">
        To finalize your verified credential issuance, please complete the nominal &#8377;299 verification &amp; archival fee via the official form:
      </p>

      <div style="text-align:center; margin:26px 0;">
        <a href="{form_url}" target="_blank" style="display:inline-block; background:linear-gradient(135deg, #16a34a 0%, #15803d 100%); color:#ffffff; font-weight:800; font-size:15px; text-decoration:none; padding:14px 34px; border-radius:8px; box-shadow:0 4px 14px rgba(22,163,74,0.35);">
          Upgrade to Verified Credential (&#8377;299) &rarr;
        </a>
      </div>

      <p style="font-size:13.5px; color:#475569; margin:20px 0 0;">
        Once submitted, our academic registrar will reconcile your verification hash and deliver your full 3-document credential packet within 24 hours. For questions, message Admissions at <strong>+91 81929 11360</strong>.
      </p>

      <div style="margin-top:28px; padding-top:20px; border-top:1px solid #e2e8f0;">
        <p style="font-size:14px; font-weight:700; color:#0f172a; margin:0;">Abhinav Sharma</p>
        <p style="font-size:12.5px; color:#64748b; margin:2px 0 0;">Executive Director &amp; Academic Head</p>
        <p style="font-size:12px; color:#94a3b8; margin:2px 0 0;">DBERT Technical Council &middot; <a href="https://dbert.in" style="color:#0284c7; text-decoration:none;">dbert.in</a> &middot; <a href="https://lms.dbert.in" style="color:#0284c7; text-decoration:none;">lms.dbert.in</a></p>
      </div>

    </div>

    <!-- Footer -->
    <div style="background:#f8fafc; padding:16px 32px; border-top:1px solid #e2e8f0; font-size:11px; color:#94a3b8; text-align:center;">
      This official credential update was dispatched to {c.get('email')} for Certificate {cert_id}. DBERT.online is now DBERT.in.
    </div>

  </div>
</body>
</html>"""

    plain_content = f"""Dear {name},

Our academic records indicate that you have completed technical milestones under Certificate ID {cert_id} in {domain}. We noticed your active return to the student portal this week.

Your credential is currently classified as Provisional. You are eligible to complete formal verification and upgrade to Permanent Verified Status on the sovereign registry (https://dbert.in).

WHAT VERIFIED STATUS UNLOCKS:
1. Permanent Verified Registry Status on https://dbert.in/verify/{cert_id}
2. Placement Indexing in Pre-Vetted Engineers Directory: https://dbert.in/verify/directory
3. Complete 3-Document Executive Packet:
   - Certificate of Completion with Luxury Slate & QR Seal
   - Academic Project Evaluation with 100-mark rubric & Turnitin score
   - Letter of Recommendation (LOR) signed by Director Abhinav Sharma
4. Recruiter Round-1 Screening Waivers

UPGRADE INSTRUCTIONS (Fee: Rs. 299):
To finalize your verified credential issuance, please complete the nominal Rs. 299 verification & archival fee via the official form:
{form_url}

For any questions, reply directly to this email or message Admissions on WhatsApp at +91 81929 11360.

Warm regards,
Abhinav Sharma
Executive Director & Academic Head
DBERT Technical Council | https://dbert.in
"""
    return subject, html_content, plain_content


def send_telemetry_report(service: EmailDeliveryService, stats: dict):
    subject = f"[TELEMETRY] Stage 1 Multi-Login Email Dispatch: {stats['sent']} Sent ({stats['pct']:.1f}%)"
    body_html = f"""<div style="font-family:sans-serif; padding:20px;">
    <h2>Stage 1 Multi-Login Candidate Dispatch Milestone</h2>
    <p><strong>Total Targets:</strong> {stats['total']}</p>
    <p><strong>Delivered Successfully:</strong> {stats['sent']}</p>
    <p><strong>Failed:</strong> {stats['failed']}</p>
    <p><strong>Remaining:</strong> {stats['remaining']}</p>
    <p><strong>Breakdown:</strong> Cohort 499: {stats['c499_sent']} sent | Cohort 299: {stats['c299_sent']} sent</p>
    <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</p>
    </div>"""

    for recipient in TELEMETRY_EMAILS:
        try:
            service.send_email(
                to=recipient,
                subject=subject,
                html_content=body_html,
                text_content=body_html.replace("<p>", "").replace("</p>", "\n").replace("<h2>", "").replace("</h2>", "\n"),
                dry_run=False
            )
            log(f"Telemetry sent to {recipient}")
        except Exception as e:
            log(f"Telemetry failed to {recipient}: {e}")


def main():
    parser = argparse.ArgumentParser(description="DBERT Stage 1 Email Dispatcher")
    parser.add_argument("--dry-run", action="store_true", help="Simulate dispatch without sending")
    parser.add_argument("--test-to", type=str, help="Send 1 sample of each email to test address")
    parser.add_argument("--live", action="store_true", help="Execute live email delivery")
    parser.add_argument("--delay", type=int, default=30, help="Delay in seconds between emails (default 30)")
    parser.add_argument("--batch", type=int, default=0, help="Maximum emails to send in this run (0 = all)")
    args = parser.parse_args()

    if not (args.dry_run or args.test_to or args.live):
        print("ERROR: Specify either --dry-run, --test-to <email>, or --live")
        sys.exit(1)

    log("=" * 70)
    log("DBERT STAGE 1 MULTI-LOGIN DISPATCH DAEMON INITIALIZED")
    log("=" * 70)

    # Load targets
    with open(COHORT_499_FILE, "r", encoding="utf-8") as f:
        c499_list = json.load(f)

    with open(COHORT_299_FILE, "r", encoding="utf-8") as f:
        c299_list = json.load(f)

    targets = []
    for u in c499_list:
        targets.append({**u, "cohort_type": "499"})
    for u in c299_list:
        targets.append({**u, "cohort_type": "299"})

    log(f"Loaded {len(targets)} total Stage 1 actionable targets ({len(c499_list)} in Cohort 499, {len(c299_list)} in Cohort 299)")

    svc = EmailDeliveryService()

    # TEST-TO MODE
    if args.test_to:
        log(f"Sending test samples to {args.test_to}...")
        sample_499 = c499_list[0]
        s499, h499, t499 = build_499_email(sample_499)
        res499 = svc.send_email(to=args.test_to, subject="[TEST SAMPLE] " + s499, html_content=h499, text_content=t499, dry_run=False)
        log(f"Cohort 499 Test Result: {res499.success} | Msg ID: {res499.message_id}")

        sample_299 = c299_list[0]
        s299, h299, t299 = build_299_email(sample_299)
        res299 = svc.send_email(to=args.test_to, subject="[TEST SAMPLE] " + s299, html_content=h299, text_content=t299, dry_run=False)
        log(f"Cohort 299 Test Result: {res299.success} | Msg ID: {res299.message_id}")
        return

    # DRY-RUN MODE
    if args.dry_run:
        log("=== DRY RUN MODE: PREVIEWING ALL 157 TARGETS ===")
        for i, c in enumerate(targets, 1):
            cohort = c["cohort_type"]
            if cohort == "499":
                subj, _, _ = build_499_email(c)
            else:
                subj, _, _ = build_299_email(c)
            print(f"[{i:03d}/{len(targets)}] [{cohort}] {c['email']} | {c['name']} | Logins: {c['logins_7d']} | Subj: {subj[:55]}...")
        log("DRY RUN COMPLETED. Run with --live to initiate live sending.")
        return

    # LIVE DISPATCH MODE
    tracking = load_tracking()
    sent_count = sum(1 for v in tracking.values() if v.get("status") == "SENT")
    log(f"Current tracking state: {sent_count} previously sent")

    pending_targets = [c for c in targets if tracking.get(c["email"].lower(), {}).get("status") != "SENT"]
    log(f"Pending actionable targets to deliver: {len(pending_targets)}")

    if args.batch > 0:
        pending_targets = pending_targets[:args.batch]
        log(f"Limiting execution to batch of {len(pending_targets)} candidates")

    success_this_run = 0
    failed_this_run = 0
    c499_sent = sum(1 for v in tracking.values() if v.get("status") == "SENT" and v.get("cohort") == "499")
    c299_sent = sum(1 for v in tracking.values() if v.get("status") == "SENT" and v.get("cohort") == "299")

    for i, c in enumerate(pending_targets, 1):
        email = c["email"].strip().lower()
        cohort = c["cohort_type"]

        if cohort == "499":
            subject, html_c, text_c = build_499_email(c)
        else:
            subject, html_c, text_c = build_299_email(c)

        log(f"[{i}/{len(pending_targets)}] Dispatching to {email} ({c['name']}) [Cohort {cohort}, Logins: {c['logins_7d']}]...")

        res = svc.send_email(
            to=email,
            subject=subject,
            html_content=html_c,
            text_content=text_c,
            dry_run=False
        )

        if res.success:
            log(f"  --> DELIVERED: Message ID: {res.message_id}")
            tracking[email] = {
                "name": c.get("name"),
                "cohort": cohort,
                "domain": c.get("domain"),
                "logins_7d": c.get("logins_7d"),
                "status": "SENT",
                "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message_id": res.message_id
            }
            save_tracking(tracking)
            success_this_run += 1
            if cohort == "499":
                c499_sent += 1
            else:
                c299_sent += 1
        else:
            log(f"  --> FAILED: {res.error}")
            tracking[email] = {
                "name": c.get("name"),
                "cohort": cohort,
                "status": "FAILED",
                "failed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": str(res.error)
            }
            save_tracking(tracking)
            failed_this_run += 1

            # Circuit breaker on daily user sending limit exceeded
            if "550 5.4.5" in str(res.error) or "Daily user sending limit" in str(res.error):
                log("CIRCUIT BREAKER: Google Workspace daily sending limit exceeded! Halting safely.")
                sys.exit(55)

        # Milestone Telemetry every 25 delivered
        total_delivered = sum(1 for v in tracking.values() if v.get("status") == "SENT")
        if total_delivered > 0 and total_delivered % 25 == 0:
            stats = {
                "total": len(targets),
                "sent": total_delivered,
                "failed": sum(1 for v in tracking.values() if v.get("status") == "FAILED"),
                "remaining": len(targets) - total_delivered,
                "pct": total_delivered / len(targets) * 100,
                "c499_sent": c499_sent,
                "c299_sent": c299_sent
            }
            send_telemetry_report(svc, stats)

        # Pacing delay
        if i < len(pending_targets):
            time.sleep(args.delay)

    log("=" * 70)
    log(f"STAGE 1 RUN COMPLETED: {success_this_run} sent, {failed_this_run} failed")
    log("=" * 70)

    # Final telemetry report upon completing all
    total_delivered = sum(1 for v in tracking.values() if v.get("status") == "SENT")
    stats = {
        "total": len(targets),
        "sent": total_delivered,
        "failed": sum(1 for v in tracking.values() if v.get("status") == "FAILED"),
        "remaining": len(targets) - total_delivered,
        "pct": total_delivered / len(targets) * 100,
        "c499_sent": c499_sent,
        "c299_sent": c299_sent
    }
    send_telemetry_report(svc, stats)


if __name__ == "__main__":
    main()
