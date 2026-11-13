#!/usr/bin/env python3
"""
scripts/dispatch_409_provisional.py
Automated batch delivery runner for all 409 provisional candidates.

Key Features:
- Multi-Account Google Workspace SMTP pool rotating across 5 authenticated accounts:
    1. abhinav.sharma@dbert.in (Abhinav Sharma, Program Head & Project Mentor)
    2. admissions@dbert.in (DBERT Admissions Directorate)
    3. support@dbert.in (DBERT Student Support & Verification)
    4. director@dbert.in (DBERT Academic Directorate)
    5. admissions.dbert@gmail.com (DBERT Candidate Services)
- Exact Reply-To and From header matching for each sending account
- High-converting institutional email template:
    * 5 value unlocks (Certificate, Turnitin Rubric, LOR, Directory Listing, Stipend Unlock)
    * Single primary CTA: "Verify Final Deliverables & Access Career Dossier →" pointing to https://dbert.in/verify/unlock?certid={certId}&email={email}
    * Zero upfront mention of "₹299" in email body or CTA button
    * Statutory disclaimers & Turnitin originality notices
- Randomized human pacing: random.uniform(18.0, 26.0)s + periodic micro-breaks
- Atomic state tracking to disk on every single email (data/dispatch_tracking_409.json & .csv)
- Crash resilience / Resume: Automatically skips already sent candidates
- Automated milestone telemetry reports to ain.sharma.abhinav@gmail.com and ajnatechrpa@gmail.com
  dispatched after every 10% progress (10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100%)
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
REGISTRY_FILE = DATA_DIR / "all_409_provisional_registry.json"
TRACKING_JSON = DATA_DIR / "dispatch_tracking_409.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_409.csv"
DISPATCH_LOG = DATA_DIR / "dispatch_409.log"
MILESTONES_FILE = DATA_DIR / "dispatch_409_milestones.json"

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


def check_dns(domain: str, qtype: str = "TXT") -> str:
    try:
        cmd = ["powershell", "-NoProfile", "-Command", f"Resolve-DnsName -Name '{domain}' -Type {qtype} -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Strings"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return "DNS check failed"


def load_or_init_tracking(registry: list[dict], reset: bool = False) -> list[dict]:
    """Loads existing tracking state or initializes fresh tracking state."""
    if TRACKING_JSON.exists() and not reset:
        try:
            with open(TRACKING_JSON, "r", encoding="utf-8") as f:
                tracking = json.load(f)
            if len(tracking) == len(registry):
                log_message(f"Loaded existing tracking file with {len(tracking)} records.")
                return tracking
        except Exception as e:
            log_message(f"Warning: Failed to load existing tracking file: {e}. Reinitializing.")

    # Initialize fresh tracking list
    tracking = []
    for idx, cand in enumerate(registry, 1):
        cert_id = cand.get("certId", f"CERT-{idx:03d}")
        cand_email = cand.get("email", "").strip()
        tracking.append({
            "index": idx,
            "certId": cert_id,
            "internId": cand.get("internId", ""),
            "holderName": cand.get("holderName", ""),
            "email": cand_email,
            "domain": cand.get("domain", "Data Analyst"),
            "project": cand.get("project", "Cognitive Solutions"),
            "duration": cand.get("duration", "15 Aug 2026 – 15 Oct 2026"),
            "score": cand.get("score", 88),
            "grade": cand.get("grade", "Grade A (Very Good)"),
            "unlockUrl": f"https://dbert.in/verify/unlock?certid={cert_id}&email={cand_email}",
            "status": "PENDING",  # PENDING, SENT, FAILED, SKIPPED
            "sent_at": None,
            "message_id": None,
            "provider": None,
            "error": None
        })

    save_tracking_state(tracking)
    log_message(f"Initialized new tracking state with {len(tracking)} candidate records.")
    return tracking


def save_tracking_state(tracking: list[dict]):
    """Atomically saves tracking state to JSON and CSV."""
    tmp_json = TRACKING_JSON.with_suffix(".tmp")
    with open(tmp_json, "w", encoding="utf-8") as f:
        json.dump(tracking, f, indent=2, ensure_ascii=False)
    tmp_json.replace(TRACKING_JSON)

    try:
        keys = ["index", "certId", "internId", "holderName", "email", "domain", "status", "sent_at", "message_id", "provider", "error"]
        with open(TRACKING_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            writer.writeheader()
            for row in tracking:
                writer.writerow(row)
    except Exception as e:
        log_message(f"Warning: CSV export error: {e}")


def build_candidate_email(cand: dict, sender_name: str, sender_role: str, sender_email: str) -> tuple[str, str, str]:
    """Builds Subject, Plain Text, and HTML for a provisional candidate."""
    name = cand["holderName"]
    cert_id = cand["certId"]
    intern_id = cand["internId"]
    domain = cand["domain"]
    project = cand["project"]
    duration = cand["duration"]
    score = cand["score"]
    grade = cand["grade"]
    unlock_url = cand.get("unlockUrl") or f"https://dbert.in/verify/unlock?certid={cert_id}&email={cand['email']}"
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
    sent_count: int,
    total_count: int,
    start_time: float,
    recent_records: list[dict],
    is_live: bool
):
    """Sends milestone progress report to ain.sharma.abhinav and ajnatechrpa."""
    elapsed_sec = time.time() - start_time
    elapsed_str = str(timedelta(seconds=int(elapsed_sec)))

    avg_sec = elapsed_sec / max(sent_count, 1)
    remaining_sec = avg_sec * max((total_count - sent_count), 0)
    eta_str = str(timedelta(seconds=int(remaining_sec)))

    subject = f"DBERT Batch Telemetry: {milestone_pct}% Progress Milestone ({sent_count}/{total_count} Candidates)"

    table_rows = ""
    for r in recent_records[-10:]:
        status_color = "#10B981" if r.get("status") == "SENT" else "#EF4444"
        table_rows += f"""<tr>
          <td style="padding:6px;border-bottom:1px solid #1E2633;color:#F0F4F8;">#{r['index']} {r['holderName']}</td>
          <td style="padding:6px;border-bottom:1px solid #1E2633;color:#38BDF8;font-family:monospace;">{r['certId']}</td>
          <td style="padding:6px;border-bottom:1px solid #1E2633;color:#8A9AB5;">{r['email']}</td>
          <td style="padding:6px;border-bottom:1px solid #1E2633;color:{status_color};font-weight:bold;">{r.get('status')}</td>
          <td style="padding:6px;border-bottom:1px solid #1E2633;color:#8A9AB5;font-size:11px;">{r.get('sent_at') or 'N/A'}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:20px;background:#0B0F17;font-family:Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:650px;margin:0 auto;background:#141A23;border:1px solid #232A36;border-radius:10px;padding:24px;">
    <div style="border-bottom:2px solid #E2B96F;padding-bottom:12px;margin-bottom:18px;">
      <h2 style="color:#E2B96F;margin:0 0 4px 0;">DBERT 409 Batch Dispatch Progress</h2>
      <p style="color:#8A9AB5;font-size:12px;margin:0;text-transform:uppercase;letter-spacing:1px;">
        Progress Milestone: <strong>{milestone_pct}% COMPLETE</strong> ({sent_count}/{total_count} Candidates)
      </p>
    </div>

    <div style="background:#0F141C;border:1px solid #1E2633;border-radius:8px;padding:16px;margin-bottom:20px;">
      <table style="width:100%;font-size:13px;color:#CBD5E1;">
        <tr><td style="padding:4px 0;width:40%;">Delivered Successfully:</td><td style="color:#10B981;font-weight:bold;">{sent_count} / {total_count} candidates</td></tr>
        <tr><td style="padding:4px 0;">Elapsed Time:</td><td>{elapsed_str}</td></tr>
        <tr><td style="padding:4px 0;">Estimated Time Remaining:</td><td>{eta_str}</td></tr>
        <tr><td style="padding:4px 0;">Pacing Model:</td><td>Randomized ~20-22s Human Pacing + Micro-breaks</td></tr>
        <tr><td style="padding:4px 0;">SMTP Architecture:</td><td>5 Multi-Account Workspace Pool (Active Rotation)</td></tr>
        <tr><td style="padding:4px 0;">Status:</td><td style="color:#38BDF8;font-weight:bold;">{'DISPATCHING LIVE' if is_live else 'DRY RUN'}</td></tr>
      </table>
    </div>

    <h3 style="color:#F0F4F8;font-size:13px;margin:0 0 8px 0;text-transform:uppercase;letter-spacing:0.5px;">Recent 10 Deliveries:</h3>
    <table style="width:100%;border-collapse:collapse;font-size:12px;background:#0F141C;border-radius:6px;overflow:hidden;">
      <thead>
        <tr style="background:#1E2633;color:#8A9AB5;text-align:left;">
          <th style="padding:8px 6px;">Candidate</th>
          <th style="padding:8px 6px;">Cert ID</th>
          <th style="padding:8px 6px;">Email</th>
          <th style="padding:8px 6px;">Status</th>
          <th style="padding:8px 6px;">Timestamp</th>
        </tr>
      </thead>
      <tbody>
        {table_rows}
      </tbody>
    </table>

    <p style="margin-top:20px;font-size:11px;color:#64748B;text-align:center;">
      Automated Telemetry Dispatcher &middot; DBERT Operational Engineering
    </p>
  </div>
</body>
</html>"""

    log_message(f"--- Dispatched Milestone Telemetry Report for {milestone_pct}% ({sent_count}/{total_count}) ---")
    for rcpt_email, rcpt_label in TELEMETRY_RECIPIENTS:
        try:
            res = service.send_email(
                to=rcpt_email,
                subject=subject,
                html_content=html,
                text_content=f"DBERT Milestone Report: {milestone_pct}% ({sent_count}/{total_count}) delivered.\nElapsed: {elapsed_str}\nETA: {eta_str}",
                tags={"type": "milestone_report", "pct": milestone_pct},
                dry_run=not is_live
            )
            log_message(f"  Milestone report to {rcpt_label} <{rcpt_email}>: {'SUCCESS' if res.success else 'FAILED'} (ID: {res.message_id})")
        except Exception as e:
            log_message(f"  Failed sending telemetry to {rcpt_email}: {e}")

    save_reported_milestone(milestone_pct)


def main():
    parser = argparse.ArgumentParser(description="409 Provisional Candidates Batch Dispatch Runner")
    parser.add_argument("--live", action="store_true", help="Execute live outbound SMTP dispatch (default is dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="Explicitly enforce dry-run simulation mode")
    parser.add_argument("--min-delay", type=float, default=18.0, help="Minimum pacing interval in seconds (default: 18.0)")
    parser.add_argument("--max-delay", type=float, default=26.0, help="Maximum pacing interval in seconds (default: 26.0)")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit on number of candidates to process in this run")
    parser.add_argument("--start-from", type=int, default=None, help="Optional override for starting 1-based index")
    parser.add_argument("--reset-tracking", action="store_true", help="Reset all tracking states to PENDING")
    parser.add_argument("--test-email", type=str, default=None, help="Send single test email to specified address and exit")
    args = parser.parse_args()

    is_live = args.live and not args.dry_run
    min_delay = args.min_delay
    max_delay = args.max_delay
    limit = args.limit
    start_from = args.start_from

    print("=" * 76)
    print("      DBERT 409 PROVISIONAL CANDIDATE BATCH DISPATCH ENGINE")
    print("=" * 76)
    print(f" Mode:                   {'[LIVE OUTBOUND SMTP SEND]' if is_live else '[DRY-RUN SIMULATION (ZERO NETWORK CALLS)]'}")
    print(f" Pacing Model:           Randomized {min_delay}s – {max_delay}s with micro-breaks")
    print(f" Milestone Reporting:    Every 10% (10%..100%) -> ain & ajna")
    print(f" Multi-Account Pool:     5 Google Workspace Accounts Rotating")
    print(f" Registry File:          {REGISTRY_FILE}")
    print(f" State File:             {TRACKING_JSON}")
    print("=" * 76)

    # 1. DNS Pre-flight
    log_message("Executing DNS Pre-Flight Tri-Factor Audit...")
    dmarc = check_dns("_dmarc.dbert.in", "TXT")
    spf = check_dns("dbert.in", "TXT")
    dkim = check_dns("google._domainkey.dbert.in", "TXT")
    log_message(f"  SPF:   {'PASS' if 'include:_spf.google.com' in spf else 'WARN'}")
    log_message(f"  DKIM:  {'PASS' if 'v=DKIM1' in dkim else 'WARN'}")
    log_message(f"  DMARC: {'PASS' if 'v=DMARC1' in dmarc else 'WARN'}")

    # 2. Load Registry
    if not REGISTRY_FILE.exists():
        log_message(f"ERROR: Registry file not found: {REGISTRY_FILE}")
        sys.exit(1)

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    log_message(f"Loaded {len(registry)} provisional candidate records from registry.")

    # 3. Load or Init Tracking State
    tracking = load_or_init_tracking(registry, reset=args.reset_tracking)

    # 4. Initialize Delivery Engine with multi-account pool
    service = EmailDeliveryService()
    pool_count = len(service.pool.accounts) if service.pool else 0
    log_message(f"Delivery engine initialized with {pool_count} Workspace accounts in pool.")

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

    # 5. Determine Candidates to Process
    candidates_to_process = []
    for item in tracking:
        idx = item["index"]
        if start_from is not None and idx < start_from:
            continue
        if item["status"] == "SENT":
            continue
        candidates_to_process.append(item)

    if limit is not None:
        candidates_to_process = candidates_to_process[:limit]

    log_message(f"Candidates pending dispatch in this session: {len(candidates_to_process)} / {len(tracking)}")

    if not candidates_to_process:
        log_message("No candidates require dispatch. All 409 records are already marked SENT.")
        return

    # 6. Main Dispatch Loop
    start_time = time.time()
    processed_count = 0
    reported_milestones = load_reported_milestones()
    total_candidates = len(tracking)

    log_message(f"Commencing batch dispatch loop at randomized {min_delay}s–{max_delay}s pacing...")

    for cand in candidates_to_process:
        idx = cand["index"]
        name = cand["holderName"]
        email = cand["email"]
        cert_id = cand["certId"]

        # Dynamic account rotation
        available_accounts = service.pool.get_shuffled_accounts() if service.pool and service.pool.accounts else []
        if not available_accounts:
            log_message("CRITICAL: All accounts in pool are in cooldown or exhausted limits. Halting batch gracefully.")
            break

        selected_account = available_accounts[0]
        s_name = selected_account.from_name
        s_role = selected_account.role or "DBERT Credential & Verification Directorate"
        s_email = selected_account.email

        log_message(f"\n>>> [{idx}/{total_candidates}] Dispatching via {s_name} <{s_email}> to: {name} <{email}> [{cert_id}]")

        subject, plain_text, html_content = build_candidate_email(cand, s_name, s_role, s_email)

        try:
            res = service.send_email(
                to=email,
                subject=subject,
                html_content=html_content,
                text_content=plain_text,
                tags={"type": "provisional_409_verification", "certId": cert_id},
                dry_run=not is_live
            )

            if res.success:
                cand["status"] = "SENT"
                cand["sent_at"] = datetime.now().isoformat()
                cand["message_id"] = res.message_id
                cand["provider"] = res.provider
                cand["error"] = None
                log_message(f"  [SUCCESS] Sent via {res.provider} | Message-ID: {res.message_id}")
            else:
                if res.error and ("550 5.4.5" in res.error or "sending limit" in res.error.lower()):
                    log_message(f"  [QUOTA LIMIT DETECTED on {s_email}] {res.error}")
                    service.pool.mark_limited(s_email, cooldown_hours=24.0)
                    cand["status"] = "PENDING"
                    cand["error"] = res.error
                    save_tracking_state(tracking)
                    # Check if other accounts remain
                    if not [a for a in service.pool.accounts if a.is_available()]:
                        log_message("  [CIRCUIT BREAKER] All accounts in pool are in cooldown. Exiting.")
                        sys.exit(55)
                    continue

                cand["status"] = "FAILED"
                cand["error"] = res.error
                log_message(f"  [FAILED] {res.error}")

        except Exception as e:
            cand["status"] = "FAILED"
            cand["error"] = str(e)
            log_message(f"  [EXCEPTION] Error sending to {email}: {e}")

        # Save state atomically after each email
        save_tracking_state(tracking)

        processed_count += 1
        current_cumulative_sent = sum(1 for x in tracking if x["status"] == "SENT")
        current_pct = int((current_cumulative_sent / total_candidates) * 100)

        # Milestone Telemetry Check (at 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100%)
        for target_m in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
            if current_pct >= target_m and target_m not in reported_milestones:
                send_milestone_telemetry(
                    service=service,
                    milestone_pct=target_m,
                    sent_count=current_cumulative_sent,
                    total_count=total_candidates,
                    start_time=start_time,
                    recent_records=[x for x in tracking if x["status"] == "SENT"],
                    is_live=is_live
                )
                reported_milestones.add(target_m)

        # Human safety pacing
        if is_live and cand != candidates_to_process[-1]:
            # Occasional micro-break every 30 sends
            if processed_count % 30 == 0:
                micro_break = random.uniform(35.0, 50.0)
                log_message(f"  [HUMAN PACING] Periodic micro-break: sleeping {micro_break:.1f}s...")
                time.sleep(micro_break)
            else:
                sleep_sec = random.uniform(min_delay, max_delay)
                time.sleep(sleep_sec)

    elapsed_total = str(timedelta(seconds=int(time.time() - start_time)))
    final_sent = sum(1 for x in tracking if x["status"] == "SENT")
    final_failed = sum(1 for x in tracking if x["status"] == "FAILED")
    log_message(f"\n=======================================================")
    log_message(f"Batch run completed in: {elapsed_total}")
    log_message(f"Total Sent: {final_sent} / {len(tracking)} | Failed: {final_failed}")
    log_message(f"State saved to {TRACKING_JSON} and {TRACKING_CSV}")
    log_message(f"=======================================================")


if __name__ == "__main__":
    main()
