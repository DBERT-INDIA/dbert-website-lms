#!/usr/bin/env python3
"""
scripts/dispatch_cohort_drive_nov2026.py
Multi-Account Google Workspace SMTP Dispatcher for DBERT Internship Cohort Drive (Nov 2026).

Notifies candidate registry (~1,590 candidates) about the upcoming remote internship
cohort starting Monday 16 Nov 2026 at 06:00 PM IST, driving LMS signups & activations.

Key Features:
- 5-account rotating Google Workspace SMTP pool
- Randomized human pacing: 14.0s - 26.0s (avg 20s) + micro-breaks every 20 emails
- Strict deduplication: records into data/dispatch_tracking_cohort_drive_nov2026.json
- High-converting email template with personalized domain track, certId, and direct deep-links
- Milestone telemetry every 100 sent emails to Ain and AjnaTech RPA
"""

import os
import sys
import time
import json
import csv
import random
import argparse
from urllib.parse import quote
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

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

REGISTRY_FILE = DATA_DIR / "sheet_1593_provisional_registry.json"
TRACKING_JSON = DATA_DIR / "dispatch_tracking_cohort_drive_nov2026.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_cohort_drive_nov2026.csv"
DISPATCH_LOG = DATA_DIR / "dispatch_cohort_drive_nov2026.log"
MILESTONES_FILE = DATA_DIR / "dispatch_cohort_drive_milestones.json"

TELEMETRY_RECIPIENTS = [
    ("ain.sharma.abhinav@gmail.com", "Abhinav (AIN)"),
    ("ajnatechrpa@gmail.com", "AjnaTech RPA")
]

DOMAIN_SLUGS = {
    "AI Agent Development": "ai-agent-development",
    "Data Analyst": "data-analyst",
    "Full Stack Development": "full-stack-development",
    "Python Automation": "python-automation",
    "UI/UX Design": "ui-ux-design",
    "DevOps & Cloud": "devops-cloud",
    "Mobile App Development": "mobile-app-development",
    "Cybersecurity": "cybersecurity",
    "Digital Marketing": "digital-marketing",
}

def log_message(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    try:
        with open(DISPATCH_LOG, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def load_or_init_tracking(registry: list[dict]) -> list[dict]:
    if TRACKING_JSON.exists():
        try:
            with open(TRACKING_JSON, "r", encoding="utf-8") as f:
                tracking = json.load(f)
            if len(tracking) == len(registry):
                log_message(f"Loaded existing tracking file with {len(tracking)} records.")
                return tracking
        except Exception as e:
            log_message(f"Warning: Failed to load tracking file: {e}. Reinitializing.")

    tracking = []
    for idx, cand in enumerate(registry, 1):
        email_clean = cand.get("email", "").strip().lower()
        domain = cand.get("domain", "Full Stack Development")
        tracking.append({
            "index": idx,
            "certId": cand.get("certId", ""),
            "internId": cand.get("internId", ""),
            "holderName": cand.get("holderName", "Candidate"),
            "email": email_clean,
            "phone": cand.get("phone", ""),
            "college": cand.get("college", ""),
            "domain": domain,
            "status": "PENDING",
            "sent_at": None,
            "sent_from": None,
            "message_id": None,
            "error": None
        })

    save_tracking(tracking)
    return tracking

def save_tracking(tracking: list[dict]):
    try:
        with open(TRACKING_JSON, "w", encoding="utf-8") as f:
            json.dump(tracking, f, indent=2, ensure_ascii=False)

        fieldnames = [
            "index", "certId", "internId", "holderName", "email", "phone", "college",
            "domain", "status", "sent_at", "sent_from", "message_id", "error"
        ]
        with open(TRACKING_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(tracking)
    except Exception as e:
        log_message(f"Error saving tracking state: {e}")

def build_cohort_drive_email(cand: dict, sender_name: str, sender_role: str, sender_email: str) -> tuple[str, str, str]:
    name = cand.get("holderName", "Candidate").strip()
    first_name = name.split()[0] if name else "Candidate"
    cert_id = cand.get("certId", "").strip()
    domain = cand.get("domain", "Full Stack Development").strip()
    email_clean = cand.get("email", "").strip()
    college = cand.get("college", "").strip() or "Registered Institution"

    ref_id = cert_id if cert_id else f"DBERT-APP-{cand.get('index', 1001):04d}"

    signup_url = f"https://lms.dbert.in/#signup?domain={quote(domain)}"
    verify_url = f"https://dbert.in/verify/{cert_id}" if cert_id else "https://dbert.in/verify"

    standup_date = "Monday, 16 November 2026 at 06:00 PM IST"
    deadline_date = "Sunday, 15 November 2026 at 11:59 PM IST"

    # Anti-spam administrative subject line: strictly status update and next required actions
    subject = f"URGENT: Application Status Update & Next Mandatory Steps [{ref_id}] — {name}"

    plain_text = f"""DBERT CENTRAL ADMISSIONS & COHORT OPERATIONS
Digital Blinc Education Research and Technology (dbert.in)
Official Communication Ref: {ref_id}
Notice Classification: HIGH PRIORITY / TIME-SENSITIVE

Dear {name},

This is an official administrative status notification regarding your technical internship application on file for the {domain} specialization track (Application Reference: {ref_id}).

Your candidate record has reached the Active Onboarding Verification stage for the upcoming sprint cycle scheduled to commence on {standup_date}.

CANDIDATE DOSSIER SUMMARY:
- Applicant Name:      {name}
- Registered Email:    {email_clean}
- College/University:  {college}
- Specialization:      {domain}
- Application Ref:     {ref_id}
- Current Status:      ACTION REQUIRED: VERIFICATION PENDING
- Cohort Sprint Start: {standup_date}
- Final Verification:  {deadline_date}

MANDATORY NEXT COURSE OF ACTIONS:
In order to validate your technical record, secure your mentor allocation, and access your project sprint briefing, you are required to complete your student profile verification prior to the specified deadline.

1. Access the Student Portal Verification Gateway:
   {signup_url}

2. Enter your registered email ({email_clean}) or phone number to link your application dossier.

3. Complete your technical profile reconciliation and confirm your preferred track ({domain}).

4. Your project repository, async sprint milestones, and mentor orientation details will be unlocked upon verification.

IMPORTANT REALLOCATION ADVISORY:
In accordance with DBERT Academic Operations Policy, candidate seats that remain unverified past {deadline_date} will be automatically released to the secondary applicant queue to ensure project team composition is locked for Monday standup.

For official verification assistance, contact admissions@dbert.in or reply directly to this notice.

Sincerely,

{sender_name}
{sender_role}
DBERT Admissions & Candidate Verification Directorate
Digital Blinc Education Research and Technology
Email: {sender_email} · Support: support@dbert.in
Portal: https://lms.dbert.in · Sovereign Registry: https://dbert.in

================================================================================
STATUTORY REGULATORY & PRIVACY DISCLOSURE:
This administrative communication is sent to registered applicants of DBERT.
Digital Blinc Education Research and Technology (DBERT) is MSME registered under the Ministry of Micro, Small & Medium Enterprises, Govt. of India (UDYAM-UP-28-0098234).
Registered Office: A-43, Sector 62, Noida, Gautam Buddha Nagar, Uttar Pradesh 201301, India.
If you believe you have received this notice in error or wish to archive your applicant record, reply with 'WITHDRAW' to admissions@dbert.in.
================================================================================
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DBERT Official Candidate Notification</title>
</head>
<body style="margin:0;padding:24px 12px;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:0 auto;background-color:#141A23;border:1.5px solid #232A36;border-radius:14px;overflow:hidden;box-shadow:0 12px 36px rgba(0,0,0,0.45);">
    
    <!-- Top Administrative Header Strip -->
    <div style="background-color:#0E1626;padding:24px 28px;border-bottom:2px solid #E2B96F;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
      <div>
        <div style="font-size:11px;font-weight:700;color:#F3D18B;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">
          DBERT CANDIDATE SELECTION DIRECTORATE
        </div>
        <div style="font-size:20px;font-weight:800;color:#FFFFFF;letter-spacing:0.5px;">
          Official Status Notice
        </div>
      </div>
      <div style="background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.35);color:#FCA5A5;font-size:11px;font-weight:700;padding:5px 12px;border-radius:999px;text-transform:uppercase;letter-spacing:0.5px;">
        Action Required &middot; 48h Window
      </div>
    </div>

    <!-- Main Content -->
    <div style="padding:30px 28px;">
      <p style="font-size:16px;font-weight:700;color:#F8FAFC;margin:0 0 14px 0;">
        Dear {name},
      </p>
      
      <p style="font-size:14px;line-height:1.65;color:#CBD5E1;margin:0 0 20px 0;">
        This is an official administrative status communication regarding your technical internship application on file for the <strong style="color:#FFFFFF;">{domain}</strong> specialization track (Application Reference: <span style="font-family:monospace;color:#38BDF8;font-weight:700;">{ref_id}</span>).
      </p>

      <p style="font-size:14px;line-height:1.65;color:#CBD5E1;margin:0 0 24px 0;">
        Following applicant file processing, your candidate record has advanced to the <strong style="color:#FBBF24;">Active Onboarding Verification</strong> stage for the upcoming sprint cycle scheduled to commence on <strong style="color:#FFFFFF;">{standup_date}</strong>.
      </p>

      <!-- Candidate Dossier Card -->
      <div style="background-color:#0F141C;border:1.5px solid #1E2633;border-radius:12px;padding:20px 22px;margin:0 0 24px 0;">
        <div style="font-size:11px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;color:#E2B96F;margin:0 0 12px 0;padding-bottom:8px;border-bottom:1px solid #1E2633;display:flex;justify-content:space-between;align-items:center;">
          <span>CANDIDATE DOSSIER RECORD</span>
          <span style="background:rgba(234,179,8,0.15);color:#FACC15;padding:2px 8px;border-radius:4px;font-size:10px;">ACTION REQUIRED</span>
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;width:40%;">Applicant Name:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{name}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Application ID:</td>
            <td style="padding:6px 0;color:#38BDF8;font-family:monospace;font-weight:700;">{ref_id}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Technical Track:</td>
            <td style="padding:6px 0;color:#E2B96F;font-weight:700;">{domain}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Current Status:</td>
            <td style="padding:6px 0;color:#F87171;font-weight:700;">VERIFICATION PENDING</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Cohort Sprint Start:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{standup_date}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Verification Deadline:</td>
            <td style="padding:6px 0;color:#FBBF24;font-weight:700;">{deadline_date}</td>
          </tr>
        </table>
      </div>

      <!-- Mandatory Next Course of Actions Box -->
      <div style="background-color:#0D1726;border:1px solid #1E293B;border-radius:12px;padding:20px 22px;margin:0 0 26px 0;">
        <div style="font-size:11.5px;font-weight:800;letter-spacing:0.8px;text-transform:uppercase;color:#38BDF8;margin-bottom:12px;">
          Mandatory Next Course of Actions
        </div>
        <ol style="margin:0;padding-left:18px;font-size:13.5px;line-height:1.75;color:#CBD5E1;">
          <li><strong style="color:#F1F5F9;">Access Portal Verification:</strong> Open the secure applicant gateway via the button below.</li>
          <li><strong style="color:#F1F5F9;">Dossier Reconciliation:</strong> Confirm your registered contact details and academic status.</li>
          <li><strong style="color:#F1F5F9;">Track Confirmation:</strong> Select your confirmed engineering track ({domain}).</li>
          <li><strong style="color:#F1F5F9;">Sprint Allocation:</strong> Receive your mentor briefing, GitHub sprint guidelines, and onboarding calendar.</li>
        </ol>
      </div>

      <!-- Primary Action CTA -->
      <div style="text-align:center;margin:30px 0 24px 0;">
        <a href="{signup_url}" target="_blank" style="display:inline-block;background:linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);color:#FFFFFF;font-weight:800;font-size:15px;text-decoration:none;padding:15px 36px;border-radius:10px;box-shadow:0 6px 20px rgba(37,99,235,0.35);letter-spacing:0.4px;">
          Complete Onboarding Verification &rarr;
        </a>
        <div style="margin-top:12px;font-size:11.5px;color:#94A3B8;">
          Verification takes 2 minutes. Secure destination: <br>
          <a href="{signup_url}" style="color:#38BDF8;text-decoration:none;word-break:break-all;">{signup_url}</a>
        </div>
      </div>

      <!-- Reallocation Warning -->
      <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);border-radius:10px;padding:14px 18px;margin-bottom:24px;font-size:12.5px;line-height:1.65;color:#FCA5A5;">
        <strong style="color:#F87171;">Reallocation Notice:</strong> Unverified candidate allocations past the <strong>{deadline_date}</strong> deadline will be automatically transferred to the waitlist queue to ensure project teams are finalized prior to sprint kickoff.
      </div>

      <!-- Signoff -->
      <div style="border-top:1px solid #1E2633;padding-top:18px;font-size:13px;line-height:1.6;color:#CBD5E1;">
        Sincerely,<br>
        <strong style="color:#F0F4F8;font-size:14px;">{sender_name}</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">{sender_role}<br>DBERT Admissions &amp; Candidate Verification Directorate</span>
      </div>
    </div>

    <!-- Official Disclaimers Footer -->
    <div style="background-color:#0E1626;padding:22px 26px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#64748B;line-height:1.7;">
      <p style="margin:0 0 8px 0;">
        <strong>STATUTORY REGULATORY &amp; PRIVACY DISCLOSURE:</strong> Digital Blinc Education Research and Technology (DBERT) is MSME registered under the Ministry of Micro, Small &amp; Medium Enterprises, Govt. of India (UDYAM-UP-28-0098234).
      </p>
      <p style="margin:0 0 8px 0;">
        Registered Office: A-43, Sector 62, Noida, Gautam Buddha Nagar, Uttar Pradesh 201301, India.
      </p>
      <p style="margin:0;">
        Official Admissions Contact: <a href="mailto:support@dbert.in" style="color:#E2B96F;text-decoration:none;">support@dbert.in</a> &nbsp;&bull;&nbsp;
        &copy; 2026 DBERT &middot; Sovereign Industrial Training &amp; Venture Studio. All Rights Reserved.
      </p>
    </div>
  </div>
</body>
</html>"""

    return subject, plain_text, html_content

def load_reported_milestones() -> set:
    if MILESTONES_FILE.exists():
        try:
            with open(MILESTONES_FILE, "r", encoding="utf-8") as f:
                d = json.load(f)
                return set(d.get("reported_milestones", []))
        except Exception:
            return set()
    return set()

def save_reported_milestone(m: int):
    ms = load_reported_milestones()
    ms.add(m)
    with open(MILESTONES_FILE, "w", encoding="utf-8") as f:
        json.dump({"reported_milestones": sorted(list(ms))}, f, indent=2)

def send_milestone_telemetry(
    service: EmailDeliveryService,
    milestone_pct: int,
    total_sent: int,
    total_candidates: int,
    start_time: float,
    is_live: bool,
    tracking: list
):
    pct = (total_sent / total_candidates) * 100 if total_candidates > 0 else 0
    elapsed_sec = time.time() - start_time
    elapsed_str = str(timedelta(seconds=int(elapsed_sec)))
    rate_per_min = (total_sent / (elapsed_sec / 60.0)) if elapsed_sec > 60 else 0.0

    account_counts = {}
    for t in tracking:
        if t.get("status") == "SENT":
            sender = t.get("sent_from", "unknown")
            account_counts[sender] = account_counts.get(sender, 0) + 1

    account_rows = "".join([
        f"<tr><td style='padding:6px 12px;border-bottom:1px solid #1E293B;'>{acc}</td>"
        f"<td style='padding:6px 12px;border-bottom:1px solid #1E293B;font-weight:bold;color:#10B981;'>{cnt}</td></tr>"
        for acc, cnt in sorted(account_counts.items(), key=lambda x: -x[1])
    ])

    subject = f"[TELEMETRY] Cohort Drive Milestone: {milestone_pct}% Reached ({total_sent}/{total_candidates})"

    html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;background-color:#0B1120;color:#F1F5F9;padding:24px;margin:0;">
  <div style="max-width:620px;margin:0 auto;background-color:#111827;border:1px solid #1F2937;border-radius:12px;padding:28px;">
    <div style="border-bottom:1px solid #1F2937;padding-bottom:16px;margin-bottom:20px;">
      <span style="background-color:#1E3A8A;color:#93C5FD;font-size:11px;font-weight:bold;padding:4px 10px;border-radius:999px;text-transform:uppercase;">
        {milestone_pct}% Milestone Telemetry
      </span>
      <h2 style="color:#FFFFFF;margin:12px 0 4px 0;font-size:22px;">DBERT Cohort Drive Nov 2026 Progress</h2>
      <p style="color:#94A3B8;margin:0;font-size:13px;">~1,590 Candidates Multi-Account Delivery</p>
    </div>

    <div style="display:flex;gap:12px;margin-bottom:20px;">
      <div style="flex:1;background-color:#1E293B;padding:12px;border-radius:8px;text-align:center;">
        <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;">Delivered</div>
        <div style="font-size:22px;font-weight:bold;color:#10B981;">{total_sent}</div>
      </div>
      <div style="flex:1;background-color:#1E293B;padding:12px;border-radius:8px;text-align:center;">
        <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;">Progress</div>
        <div style="font-size:22px;font-weight:bold;color:#38BDF8;">{pct:.1f}%</div>
      </div>
      <div style="flex:1;background-color:#1E293B;padding:12px;border-radius:8px;text-align:center;">
        <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;">Total Cohort</div>
        <div style="font-size:22px;font-weight:bold;color:#F1F5F9;">{total_candidates}</div>
      </div>
    </div>

    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:24px;">
      <tr>
        <td style="padding:8px 0;color:#94A3B8;border-bottom:1px solid #1F2937;"><strong>Mode:</strong></td>
        <td style="padding:8px 0;text-align:right;border-bottom:1px solid #1F2937;color:#10B981;font-weight:bold;">{'LIVE OVER THE WIRE' if is_live else 'DRY RUN'}</td>
      </tr>
      <tr>
        <td style="padding:8px 0;color:#94A3B8;border-bottom:1px solid #1F2937;"><strong>Elapsed:</strong></td>
        <td style="padding:8px 0;text-align:right;border-bottom:1px solid #1F2937;color:#F1F5F9;">{elapsed_str}</td>
      </tr>
      <tr>
        <td style="padding:8px 0;color:#94A3B8;border-bottom:1px solid #1F2937;"><strong>Throughput:</strong></td>
        <td style="padding:8px 0;text-align:right;border-bottom:1px solid #1F2937;color:#F1F5F9;">~{rate_per_min * 60:.1f} emails / hr</td>
      </tr>
    </table>

    <h4 style="color:#E2B96F;margin:0 0 10px 0;font-size:14px;text-transform:uppercase;">Account Load Distribution (5 Accounts)</h4>
    <table style="width:100%;border-collapse:collapse;font-size:12px;background-color:#0F172A;border-radius:6px;overflow:hidden;">
      <thead>
        <tr style="background-color:#1E293B;color:#94A3B8;">
          <th style="padding:8px 12px;text-align:left;">Sending Account</th>
          <th style="padding:8px 12px;text-align:left;">Delivered</th>
        </tr>
      </thead>
      <tbody>
        {account_rows}
      </tbody>
    </table>
  </div>
</body>
</html>"""

    txt = f"DBERT Cohort Drive: {milestone_pct}% Reached ({total_sent}/{total_candidates}). Elapsed: {elapsed_str}."

    for em, recipient_name in TELEMETRY_RECIPIENTS:
        try:
            service.send_email(
                to=em,
                subject=subject,
                html_content=html_body,
                text_content=txt,
                tags={"type": "telemetry", "batch": "cohort_drive_nov2026", "milestone": str(milestone_pct)},
                dry_run=not is_live
            )
            log_message(f"[TELEMETRY] ✓ Sent {milestone_pct}% milestone report to {em}")
        except Exception as e:
            log_message(f"[TELEMETRY] ✗ Failed to send milestone to {em}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Multi-Account Cohort Drive Dispatcher for DBERT")
    parser.add_argument("--live", action="store_true", help="Execute live SMTP delivery (default is dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="Explicit dry run")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of emails to process")
    parser.add_argument("--test-email", type=str, default=None, help="Send a single test email to specified address")
    parser.add_argument("--start-index", type=int, default=1, help="Start from specific index")

    args = parser.parse_args()
    is_live = args.live and not args.dry_run

    log_message("=" * 70)
    log_message(f"Initiating DBERT Cohort Drive Dispatcher (Nov 2026) [Mode: {'LIVE' if is_live else 'DRY RUN'}]")
    log_message("=" * 70)

    if not REGISTRY_FILE.exists():
        log_message(f"Registry file not found at {REGISTRY_FILE}.")
        sys.exit(1)

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    log_message(f"Loaded {len(registry)} candidates from registry.")

    tracking = load_or_init_tracking(registry)
    pending_count = sum(1 for t in tracking if t["status"] == "PENDING")
    sent_count = sum(1 for t in tracking if t["status"] == "SENT")
    log_message(f"Status Summary: Sent={sent_count}, Pending={pending_count}")

    service = EmailDeliveryService()

    # TEST EMAIL MODE
    if args.test_email:
        sample_cand = dict(tracking[0]) if tracking else {}
        sample_cand["email"] = args.test_email
        if "abhinav" in args.test_email.lower():
            sample_cand["holderName"] = "Abhinav Sharma"
            sample_cand["certId"] = "CERT-DBERT-2026-FSD-001"
            sample_cand["domain"] = "Full Stack Development"
            sample_cand["college"] = "DBERT Academic & Engineering Directorate"
        sample_account = service.pool.get_shuffled_accounts()[0] if service.pool and service.pool.accounts else None
        s_name = sample_account.from_name if sample_account else "Abhinav Sharma"
        s_role = sample_account.role if sample_account else "Program Head & Project Mentor"
        s_email = sample_account.email if sample_account else "abhinav.sharma@dbert.in"

        subj, txt, html_body = build_cohort_drive_email(sample_cand, s_name, s_role, s_email)
        log_message(f"Sending test email to: {args.test_email} (From: {s_name} <{s_email}>)")

        res = service.send_email(
            to=args.test_email,
            subject=subj,
            html_content=html_body,
            text_content=txt,
            tags={"type": "test_cohort_drive"},
            dry_run=not is_live
        )
        log_message(f"Test email result: Success={res.success}, ID={res.message_id}, Error={res.error}")
        return

    # BATCH DISPATCH LOOP
    start_time = time.time()
    processed_in_session = 0

    candidates_to_process = [
        t for t in tracking
        if t["index"] >= args.start_index and t["status"] == "PENDING"
    ]

    if args.limit:
        candidates_to_process = candidates_to_process[:args.limit]

    log_message(f"Candidates to process in this run: {len(candidates_to_process)}")

    for t_item in candidates_to_process:
        idx = t_item["index"]
        to_email = t_item["email"]
        name = t_item["holderName"]
        cert_id = t_item["certId"]

        available_accounts = service.pool.get_shuffled_accounts() if service.pool and service.pool.accounts else []
        if not available_accounts:
            log_message("CRITICAL: All accounts in pool are in cooldown or exhausted daily limits. Pausing batch gracefully.")
            break

        selected_account = available_accounts[0]
        s_name = selected_account.from_name
        s_role = selected_account.role or "DBERT Admissions & Student Success Directorate"
        s_email = selected_account.email

        subj, txt, html_body = build_cohort_drive_email(t_item, s_name, s_role, s_email)

        log_message(f"[{idx}/{len(registry)}] Delivering to {name} <{to_email}> via {s_name} <{s_email}>...")

        res = service.send_email(
            to=to_email,
            subject=subj,
            html_content=html_body,
            text_content=txt,
            tags={"batch": "cohort_drive_nov2026", "cert_id": cert_id, "index": str(idx)},
            dry_run=not is_live
        )

        if res.success:
            t_item["status"] = "SENT"
            t_item["sent_at"] = datetime.now().isoformat()
            t_item["sent_from"] = s_email
            t_item["message_id"] = res.message_id
            t_item["error"] = None
            log_message(f"[{idx}/{len(registry)}] ✓ DELIVERED to {to_email} (MsgID: {res.message_id})")
        else:
            t_item["error"] = res.error
            log_message(f"[{idx}/{len(registry)}] ✗ FAILED: {res.error}")

        save_tracking(tracking)
        processed_in_session += 1

        # Check milestones every 10% or 100 emails
        total_delivered = sum(1 for t in tracking if t["status"] == "SENT")
        for m_pct in [10, 25, 50, 75, 90, 100]:
            target_count = int(len(registry) * (m_pct / 100.0))
            reported = load_reported_milestones()
            if total_delivered >= target_count and m_pct not in reported:
                log_message(f"[MILESTONE] Triggering {m_pct}% telemetry dispatch ({total_delivered}/{len(registry)} sent)")
                send_milestone_telemetry(service, m_pct, total_delivered, len(registry), start_time, is_live, tracking)
                save_reported_milestone(m_pct)

        # Micro-breaks & Human Pacing
        if processed_in_session > 0 and processed_in_session % 20 == 0:
            micro_break = random.uniform(35.0, 50.0)
            log_message(f"[PACING] Micro-break for {micro_break:.1f}s after 20 emails...")
            time.sleep(micro_break)
        else:
            sleep_duration = random.uniform(14.0, 26.0) if is_live else 0.05
            time.sleep(sleep_duration)

    total_delivered = sum(1 for t in tracking if t["status"] == "SENT")
    log_message("=" * 70)
    log_message(f"Cohort Drive Batch Completed. Total Delivered: {total_delivered}/{len(registry)}")
    log_message("=" * 70)

if __name__ == "__main__":
    main()
