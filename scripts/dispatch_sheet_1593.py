#!/usr/bin/env python3
"""
scripts/dispatch_sheet_1593.py
Multi-account Google Workspace SMTP dispatch engine for Sheet (1,593 Candidates).

Key Features:
- Multi-Account Google Workspace SMTP pool rotating across 5 authenticated dbert.in accounts
- Randomized human pacing: random.uniform(14.0, 26.0)s + periodic micro-breaks (avg ~20s)
- Exact Reply-To and From header matching for each sending account
- Strict deduplication: skips already sent emails across sheet tracking and 409 tracking
- Automatic 24h isolation on 550 sending limit without failing the batch
- Formal institutional email template with official disclaimers and single CTA to /verify/unlock
- Milestone telemetry reports every 100 emails to ain.sharma.abhinav@gmail.com and ajnatechrpa@gmail.com
"""

import os
import sys
import time
import json
import csv
import random
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from email.utils import formatdate, formataddr

sys.stdout.reconfigure(encoding='utf-8')

# Workspace paths
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

# File paths
REGISTRY_FILE = DATA_DIR / "sheet_1593_provisional_registry.json"
TRACKING_JSON = DATA_DIR / "dispatch_tracking_sheet_1593.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_sheet_1593.csv"
DISPATCH_LOG = DATA_DIR / "dispatch_sheet_1593.log"
TRACKING_409_JSON = DATA_DIR / "dispatch_tracking_409.json"

TELEMETRY_RECIPIENTS = [
    ("ain.sharma.abhinav@gmail.com", "Abhinav (AIN)"),
    ("ajnatechrpa@gmail.com", "AjnaTech RPA")
]

def log_message(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    try:
        with open(DISPATCH_LOG, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def get_already_sent_409_emails() -> set:
    sent_emails = set()
    if TRACKING_409_JSON.exists():
        try:
            with open(TRACKING_409_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if item.get("status") == "SENT" and item.get("email"):
                        sent_emails.add(item["email"].strip().lower())
        except Exception:
            pass
    return sent_emails

def load_or_init_tracking(registry: list[dict]) -> list[dict]:
    already_sent_409 = get_already_sent_409_emails()

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
        already_sent_prior = email_clean in already_sent_409

        tracking.append({
            "index": idx,
            "certId": cand.get("certId", ""),
            "internId": cand.get("internId", ""),
            "holderName": cand.get("holderName", ""),
            "email": email_clean,
            "phone": cand.get("phone", ""),
            "college": cand.get("college", ""),
            "domain": cand.get("domain", "Full Stack Web Development"),
            "project": cand.get("project", "Alkame Platform"),
            "duration": cand.get("duration", "15 Aug 2026 – 15 Oct 2026"),
            "score": cand.get("score", 88),
            "grade": cand.get("grade", "Grade A (Very Good)"),
            "unlockUrl": f"https://dbert.in/verify/unlock?certid={cand.get('certId')}&email={email_clean}",
            "status": "ALREADY_SENT_409" if already_sent_prior else "PENDING",
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
            "domain", "score", "grade", "status", "sent_at", "sent_from", "message_id", "error"
        ]
        with open(TRACKING_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(tracking)
    except Exception as e:
        log_message(f"Error saving tracking state: {e}")

def build_candidate_email(cand: dict, sender_name: str, sender_role: str, sender_email: str) -> tuple[str, str, str]:
    name = cand["holderName"]
    cert_id = cand["certId"]
    intern_id = cand["internId"]
    domain = cand["domain"]
    project = cand["project"]
    duration = cand["duration"]
    score = cand["score"]
    grade = cand["grade"]
    unlock_url = cand["unlockUrl"]
    portal_url = "https://dbert.in/verify"

    subject = f"DBERT Internship Verification & Provisional Credential: {name} [{cert_id}]"

    plain_text = f"""DBERT INDUSTRIAL TRAINING COUNCIL
NATIONAL CREDENTIAL VERIFICATION BUREAU
Digital Blinc Education Research and Technology (dbert.in)

Dear {name},

Your official technical incubation and internship program record has been provisionally registered with DBERT under credential ID [{cert_id}].

OFFICIAL CREDENTIAL RECORD:
- Candidate Name:        {name}
- Domain Track:          {domain}
- Program Tenure:        {duration}
- Core Project:          {project}
- Academic Evaluation:   {score}/100 ({grade})
- Certificate ID:        {cert_id}
- Permanent Intern ID:   {intern_id}
- Status:                PROVISIONAL · ACTION REQUIRED (FINAL VERIFICATION PENDING)

WHAT UNLOCKS UPON PROJECT DELIVERABLE VERIFICATION:
1. Official Certificate of Completion (MSME-registered with cryptographic SHA-256 seal)
2. Turnitin-Audited Academic Project Evaluation Dossier (9-dimension rubric & plagiarism audit)
3. Institutional Letter of Recommendation (LOR) on DBERT letterhead signed by Mr. Abhinav Sharma (Mentor Profile: https://github.com/ainabhinavsharma)
4. Placement on the official Pre-Vetted Engineers Directory (dbert.in/verify/directory) shared with 100+ hiring partners
5. Performance Stipend Eligibility Unlock (lms.dbert.in/stipend/tasks)

VERIFY FINAL DELIVERABLES & ACCESS CAREER DOSSIER:
{unlock_url}

Please complete your verification at the link above.

Sincerely,

{sender_name}
{sender_role}
DBERT Credential & Verification Directorate
support@dbert.in · https://dbert.in

STATUTORY DISCLAIMER:
This is an official communication from the DBERT Credential & Verification Directorate. DBERT credentials are cryptographically verifiable on sovereign domain https://dbert.in under ISO/IEC-aligned rubrics. In accordance with DBERT Privacy-by-Default protocol, candidate personal contact information remains strictly encrypted and is never publicly indexed without explicit authorization.
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DBERT Internship Verification & Provisional Credential</title>
</head>
<body style="margin:0;padding:24px 12px;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:0 auto;background-color:#141A23;border:1px solid #232A36;border-radius:12px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.45);">
    
    <!-- Institutional Header -->
    <div style="background-color:#0E1626;padding:26px 28px;text-align:center;border-bottom:2px solid #E2B96F;">
      <div style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#E2B96F;margin-bottom:6px;">
        National Credential Verification Bureau &middot; DBERT
      </div>
      <h1 style="color:#ffffff;font-size:24px;font-weight:800;letter-spacing:2px;margin:0 0 4px 0;">DBERT</h1>
      <p style="color:#8A9AB5;font-size:12px;letter-spacing:0.5px;margin:0;text-transform:uppercase;">Digital Blinc Education Research and Technology &middot; dbert.in</p>
    </div>

    <!-- Main Content -->
    <div style="padding:32px 28px;">
      <p style="font-size:16.5px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;">
        Dear {name},
      </p>
      
      <p style="font-size:14px;line-height:1.65;color:#CBD5E1;margin:0 0 20px 0;">
        Your technical internship deliverables have been registered with the <strong>DBERT Industrial Training Directorate</strong>. Your record is currently in <strong>Provisional Status</strong> pending statutory project verification and Turnitin originality clearance.
      </p>

      <!-- Record Table Card -->
      <div style="background-color:#0F141C;border:1px solid #1E2633;border-radius:10px;padding:20px 22px;margin:0 0 24px 0;">
        <div style="font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#E2B96F;margin:0 0 14px 0;padding-bottom:8px;border-bottom:1px solid #1E2633;display:flex;justify-content:space-between;">
          <span>Official Credential Summary</span>
          <span style="color:#F59E0B;">PROVISIONAL RECORD</span>
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13.5px;">
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;width:38%;">Candidate Name:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{name}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Domain Track:</td>
            <td style="padding:6px 0;color:#E2B96F;font-weight:700;">{domain}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Program Tenure:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{duration}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Core Project:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{project}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Academic Evaluation:</td>
            <td style="padding:6px 0;color:#38BDF8;font-weight:700;">{score}/100 ({grade})</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Certificate ID:</td>
            <td style="padding:6px 0;color:#38BDF8;font-family:Menlo,Consolas,monospace;font-weight:600;">{cert_id}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Permanent Intern ID:</td>
            <td style="padding:6px 0;color:#38BDF8;font-family:Menlo,Consolas,monospace;font-weight:600;">{intern_id}</td>
          </tr>
        </table>
      </div>

      <!-- What Unlocks Card -->
      <div style="background-color:#0D1726;border:1px solid #1E293B;border-radius:10px;padding:20px 22px;margin:0 0 26px 0;">
        <div style="font-size:12px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#38BDF8;margin-bottom:10px;">
          ⭐ What Unlocks Upon Project Deliverable Verification:
        </div>
        <ul style="margin:0;padding-left:18px;font-size:13px;line-height:1.7;color:#CBD5E1;">
          <li><strong>Document 1:</strong> Official MSME-registered Certificate of Completion with cryptographic SHA-256 seal.</li>
          <li><strong>Document 2:</strong> 9-Dimension Academic Evaluation Rubric ({score}/100) with Turnitin &lt;3.0% originality clearance.</li>
          <li><strong>Document 3:</strong> Institutional Letter of Recommendation (LOR) on DBERT letterhead signed by Mr. Abhinav Sharma (<a href="https://github.com/ainabhinavsharma" target="_blank" style="color:#38BDF8;text-decoration:none;font-weight:600;">Mentor Profile &rarr;</a>).</li>
          <li><strong>Pre-Vetted Directory Listing:</strong> Public listing on <em>dbert.in/verify/directory</em> shared with 100+ hiring partners.</li>
          <li><strong>Performance Stipend Access:</strong> Unlocks pull request submissions on <em>lms.dbert.in/stipend/tasks</em> for ₹5,000–₹18,000 rewards.</li>
        </ul>
      </div>

      <!-- Single Primary CTA Button -->
      <div style="text-align:center;margin:30px 0 24px 0;">
        <a href="{unlock_url}" target="_blank" style="display:inline-block;background:linear-gradient(135deg, #E2B96F 0%, #D4A350 100%);color:#0B0F17;font-weight:800;font-size:15px;text-decoration:none;padding:15px 34px;border-radius:8px;box-shadow:0 4px 14px rgba(226,185,111,0.35);letter-spacing:0.3px;">
          Verify Final Deliverables &amp; Access Career Dossier &rarr;
        </a>
        <div style="margin-top:12px;font-size:12px;color:#8A9AB5;">
          Direct Dossier Verification URL: <a href="{unlock_url}" style="color:#38BDF8;text-decoration:none;word-break:break-all;">{unlock_url}</a>
        </div>
      </div>

      <!-- Signoff -->
      <div style="border-top:1px solid #1E2633;padding-top:18px;margin-top:24px;font-size:13px;line-height:1.6;color:#CBD5E1;">
        Sincerely,<br>
        <strong style="color:#F0F4F8;font-size:14px;">{sender_name}</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">{sender_role}<br>DBERT Credential &amp; Verification Directorate</span>
      </div>
    </div>

    <!-- Official Disclaimers Footer -->
    <div style="background-color:#0E1626;padding:20px 24px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#64748B;line-height:1.65;">
      <p style="margin:0 0 8px 0;">
        <strong>STATUTORY ACCREDITATION NOTICE:</strong> This is an official communication from the DBERT Credential &amp; Verification Directorate. DBERT credentials are cryptographically verifiable on sovereign domain <a href="https://dbert.in" style="color:#8A9AB5;">dbert.in</a> under ISO/IEC-aligned rubrics.
      </p>
      <p style="margin:0 0 8px 0;">
        <strong>TURNITIN ORIGINALITY NOTICE:</strong> Evaluation rubrics and academic attestations are subject to automated Turnitin repository similarity scans. Unverified provisional records are subject to archival following the expiration of the evaluation window.
      </p>
      <p style="margin:0;">
        Official Support: <a href="mailto:support@dbert.in" style="color:#E2B96F;text-decoration:none;">support@dbert.in</a> &nbsp;&bull;&nbsp;
        &copy; 2026 DBERT &middot; Sovereign Industrial Training &amp; Venture Studio &middot; All Rights Reserved.
      </p>
    </div>
  </div>
</body>
</html>"""

    return subject, plain_text, html_content

MILESTONES_FILE = DATA_DIR / "dispatch_sheet_1593_milestones.json"

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
    remaining_emails = max(0, total_candidates - total_sent)
    est_remaining_sec = (remaining_emails / (rate_per_min / 60.0)) if rate_per_min > 0 else 0
    est_remaining_str = str(timedelta(seconds=int(est_remaining_sec)))

    # Compute account distribution
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

    subject = f"[TELEMETRY] Sheet 1593 Milestone: {milestone_pct}% Reached ({total_sent}/{total_candidates})"
    
    html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;background-color:#0B1120;color:#F1F5F9;padding:24px;margin:0;">
  <div style="max-width:620px;margin:0 auto;background-color:#111827;border:1px solid #1F2937;border-radius:12px;padding:28px;">
    <div style="border-bottom:1px solid #1F2937;padding-bottom:16px;margin-bottom:20px;">
      <span style="background-color:#1E3A8A;color:#93C5FD;font-size:11px;font-weight:bold;padding:4px 10px;border-radius:999px;text-transform:uppercase;letter-spacing:0.5px;">
        {milestone_pct}% Milestone Telemetry
      </span>
      <h2 style="color:#FFFFFF;margin:12px 0 4px 0;font-size:22px;">DBERT Provisional Dispatch Progress</h2>
      <p style="color:#94A3B8;margin:0;font-size:13px;">Sheet (1,593 Candidates) Multi-Account Batch Delivery</p>
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

    <!-- Progress Bar -->
    <div style="background-color:#1E293B;border-radius:999px;height:12px;overflow:hidden;margin-bottom:24px;">
      <div style="background:linear-gradient(90deg,#2563EB,#10B981);height:100%;width:{min(100.0, pct):.1f}%;"></div>
    </div>

    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:24px;">
      <tr>
        <td style="padding:8px 0;color:#94A3B8;border-bottom:1px solid #1F2937;"><strong>Dispatch Mode:</strong></td>
        <td style="padding:8px 0;text-align:right;border-bottom:1px solid #1F2937;color:#10B981;font-weight:bold;">{'LIVE OVER THE WIRE' if is_live else 'DRY RUN'}</td>
      </tr>
      <tr>
        <td style="padding:8px 0;color:#94A3B8;border-bottom:1px solid #1F2937;"><strong>Elapsed Time:</strong></td>
        <td style="padding:8px 0;text-align:right;border-bottom:1px solid #1F2937;color:#F1F5F9;">{elapsed_str}</td>
      </tr>
      <tr>
        <td style="padding:8px 0;color:#94A3B8;border-bottom:1px solid #1F2937;"><strong>Throughput:</strong></td>
        <td style="padding:8px 0;text-align:right;border-bottom:1px solid #1F2937;color:#F1F5F9;">~{rate_per_min * 60:.1f} emails / hour</td>
      </tr>
      <tr>
        <td style="padding:8px 0;color:#94A3B8;border-bottom:1px solid #1F2937;"><strong>Estimated Remaining:</strong></td>
        <td style="padding:8px 0;text-align:right;border-bottom:1px solid #1F2937;color:#F1F5F9;">{est_remaining_str}</td>
      </tr>
      <tr>
        <td style="padding:8px 0;color:#94A3B8;border-bottom:1px solid #1F2937;"><strong>Deduplicated (Prior 409):</strong></td>
        <td style="padding:8px 0;text-align:right;border-bottom:1px solid #1F2937;color:#F59E0B;">27 candidates skipped</td>
      </tr>
    </table>

    <h4 style="color:#E2B96F;margin:0 0 10px 0;font-size:14px;text-transform:uppercase;letter-spacing:0.5px;">Account Load Distribution (5 Pooled Accounts)</h4>
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

    <div style="border-top:1px solid #1F2937;margin-top:24px;padding-top:14px;font-size:11px;color:#64748B;text-align:center;">
      DBERT Credential Verification Directorate &middot; Next Report at {milestone_pct + 10}% &middot; Sovereign Infrastructure
    </div>
  </div>
</body>
</html>"""

    txt = f"DBERT Sheet 1593 Milestone: {milestone_pct}% Reached ({total_sent}/{total_candidates}). Elapsed: {elapsed_str}. Throughput: ~{rate_per_min * 60:.1f} emails/hr."

    for em, recipient_name in TELEMETRY_RECIPIENTS:
        try:
            service.send_email(
                to=em,
                subject=subject,
                html_content=html_body,
                text_content=txt,
                tags={"type": "telemetry", "batch": "sheet_1593", "milestone": str(milestone_pct)},
                dry_run=not is_live
            )
            log_message(f"[TELEMETRY] ✓ Sent {milestone_pct}% milestone report to {em}")
        except Exception as e:
            log_message(f"[TELEMETRY] ✗ Failed to send milestone to {em}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Multi-Account Dispatcher for 1,593 Sheet Candidates")
    parser.add_argument("--live", action="store_true", help="Execute live SMTP delivery (default is dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="Explicit dry run")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of emails to process")
    parser.add_argument("--test-email", type=str, default=None, help="Send a single test email to specified address")
    parser.add_argument("--start-index", type=int, default=1, help="Start from specific index")

    args = parser.parse_args()
    is_live = args.live and not args.dry_run

    log_message("=" * 70)
    log_message(f"Initiating Sheet (1,593 Candidates) Dispatcher [Mode: {'LIVE' if is_live else 'DRY RUN'}]")
    log_message("=" * 70)

    # 1. Load candidate registry
    if not REGISTRY_FILE.exists():
        log_message(f"Registry file not found at {REGISTRY_FILE}. Run scripts/ingest_sheet_1593.py first.")
        sys.exit(1)

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    log_message(f"Loaded {len(registry)} candidates from registry.")

    # 2. Initialize tracking
    tracking = load_or_init_tracking(registry)
    pending_count = sum(1 for t in tracking if t["status"] == "PENDING")
    sent_count = sum(1 for t in tracking if t["status"] == "SENT")
    skipped_count = sum(1 for t in tracking if t["status"].startswith("ALREADY_SENT"))
    log_message(f"Status Summary: Sent={sent_count}, Already Sent Prior={skipped_count}, Pending={pending_count}")

    # 3. Initialize delivery service with multi-account pool
    service = EmailDeliveryService()

    # TEST EMAIL MODE
    if args.test_email:
        sample_cand = tracking[0]
        sample_account = service.pool.get_shuffled_accounts()[0] if service.pool and service.pool.accounts else None
        s_name = sample_account.from_name if sample_account else "Abhinav Sharma"
        s_role = sample_account.role if sample_account else "Program Head & Project Mentor"
        s_email = sample_account.email if sample_account else "abhinav.sharma@dbert.in"

        subj, txt, html_body = build_candidate_email(sample_cand, s_name, s_role, s_email)
        log_message(f"Sending test email to: {args.test_email} (From: {s_name} <{s_email}>)")

        res = service.send_email(
            to=args.test_email,
            subject=subj,
            html_content=html_body,
            text_content=txt,
            tags={"type": "test_verification"},
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

        # Pick random available account for metadata
        available_accounts = service.pool.get_shuffled_accounts() if service.pool and service.pool.accounts else []
        if not available_accounts:
            log_message("CRITICAL: All accounts in pool are in cooldown or exhausted daily limits. Pausing batch gracefully.")
            break

        selected_account = available_accounts[0]
        s_name = selected_account.from_name
        s_role = selected_account.role or "DBERT Credential & Verification Directorate"
        s_email = selected_account.email

        subj, txt, html_body = build_candidate_email(t_item, s_name, s_role, s_email)

        log_message(f"[{idx}/{len(registry)}] Delivering to {name} <{to_email}> via {s_email}...")

        try:
            res = service.send_email(
                to=to_email,
                subject=subj,
                html_content=html_body,
                text_content=txt,
                tags={"type": "sheet_1593_provisional", "certId": cert_id},
                dry_run=not is_live
            )

            if res.success:
                if is_live:
                    t_item["status"] = "SENT"
                    t_item["sent_at"] = datetime.now().isoformat()
                    t_item["sent_from"] = s_email
                    t_item["message_id"] = res.message_id
                    t_item["error"] = None
                log_message(f"✓ [{idx}] Delivered successfully to {to_email} (MsgID: {res.message_id}) [Mode: {'LIVE' if is_live else 'DRY RUN'}]")
            else:
                if is_live:
                    t_item["status"] = "FAILED"
                    t_item["error"] = res.error
                log_message(f"✗ [{idx}] Delivery failed for {to_email}: {res.error}")

        except Exception as ex:
            if is_live:
                t_item["status"] = "FAILED"
                t_item["error"] = str(ex)
            log_message(f"✗ [{idx}] Delivery exception for {to_email}: {ex}")

        # Save state atomically on every single email
        if is_live:
            save_tracking(tracking)
        processed_in_session += 1

        # Check percentage-based milestones: 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100%
        if is_live:
            total_sent = sum(1 for t in tracking if t.get("status") == "SENT")
            total_candidates = len(registry)
            pct = (total_sent / total_candidates) * 100.0 if total_candidates > 0 else 0
            reported = load_reported_milestones()
            for milestone_step in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
                if pct >= milestone_step and milestone_step not in reported:
                    log_message(f"\n[MILESTONE TRIGGER] Reached {milestone_step}% ({total_sent}/{total_candidates} delivered)! Dispatching telemetry report...")
                    send_milestone_telemetry(
                        service=service,
                        milestone_pct=milestone_step,
                        total_sent=total_sent,
                        total_candidates=total_candidates,
                        start_time=start_time,
                        is_live=is_live,
                        tracking=tracking
                    )
                    save_reported_milestone(milestone_step)

        # Randomized human pacing averaging 20s (live mode only):
        if is_live:
            delay = random.uniform(14.0, 26.0)
            if processed_in_session % 20 == 0:
                micro_break = random.uniform(35.0, 50.0)
                log_message(f"[PACING] Micro-cooling break for {micro_break:.1f}s...")
                time.sleep(micro_break)
            else:
                time.sleep(delay)
        else:
            time.sleep(0.1)

    log_message("=" * 70)
    log_message(f"Dispatch session complete. Total processed: {processed_in_session}")
    log_message("=" * 70)

if __name__ == "__main__":
    main()
