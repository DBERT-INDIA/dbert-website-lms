#!/usr/bin/env python3
"""
scripts/dispatch_409_provisional.py
Automated batch delivery runner for all 409 provisional candidates.

Key Features:
- Exact Reply-To matching: From and Reply-To set to Abhinav Sharma <abhinav.sharma@dbert.in>
- 30-second pacing interval between candidate dispatches (~3.4h total run)
- Atomic state tracking to disk on every single email (data/dispatch_tracking_409.json & .csv)
- Crash resilience / Resume: Automatically skips already sent candidates
- Automated milestone telemetry reports to ain.sharma.abhinav@gmail.com and ajnatechrpa@gmail.com
  dispatched every 100 emails (milestones at #100, #200, #300, #400, and completion at #409)
- Multipart MIME (RFC 2046) with plain text alternative and clean branded responsive HTML card
- Google Workspace SMTP (smtp.gmail.com:465 SSL) using authenticated local App Password
"""

import os
import sys
import time
import json
import csv
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from email.utils import formatdate

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

from services.delivery_service import EmailDeliveryService, EmailPacer

# File paths
REGISTRY_FILE = DATA_DIR / "all_409_provisional_registry.json"
TRACKING_JSON = DATA_DIR / "dispatch_tracking_409.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_409.csv"
DISPATCH_LOG = DATA_DIR / "dispatch_409.log"

# Sender and Telemetry Targets
FROM_NAME = "Abhinav Sharma"
FROM_EMAIL = "abhinav.sharma@dbert.in"
REPLY_TO_EMAIL = "abhinav.sharma@dbert.in"  # Exactly matching sender email address

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


def load_or_init_tracking(registry: list[dict]) -> list[dict]:
    """Loads existing tracking state or initializes fresh tracking state."""
    if TRACKING_JSON.exists():
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
        tracking.append({
            "index": idx,
            "certId": cert_id,
            "internId": cand.get("internId", ""),
            "holderName": cand.get("holderName", ""),
            "email": cand.get("email", "").strip(),
            "domain": cand.get("domain", "Data Analyst"),
            "project": cand.get("project", "Cognitive Solutions"),
            "duration": cand.get("duration", "15 Aug 2026 – 15 Oct 2026"),
            "score": cand.get("score", 88),
            "grade": cand.get("grade", "Grade A (Very Good)"),
            "verifyUrl": f"https://dbert.in/verify/{cert_id}",
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
    # Write JSON atomically
    tmp_json = TRACKING_JSON.with_suffix(".tmp")
    with open(tmp_json, "w", encoding="utf-8") as f:
        json.dump(tracking, f, indent=2, ensure_ascii=False)
    tmp_json.replace(TRACKING_JSON)

    # Write CSV
    try:
        keys = ["index", "certId", "internId", "holderName", "email", "domain", "status", "sent_at", "message_id", "provider", "error"]
        with open(TRACKING_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            writer.writeheader()
            for row in tracking:
                writer.writerow(row)
    except Exception as e:
        log_message(f"Warning: CSV export error: {e}")


def build_candidate_email(cand: dict) -> tuple[str, str, str]:
    """Builds Subject, Plain Text, and HTML for a provisional candidate."""
    name = cand["holderName"]
    cert_id = cand["certId"]
    intern_id = cand["internId"]
    domain = cand["domain"]
    project = cand["project"]
    duration = cand["duration"]
    score = cand["score"]
    grade = cand["grade"]
    verify_url = cand["verifyUrl"]
    portal_url = "https://dbert.in/verify"

    subject = f"DBERT Internship Verification: {name} [{cert_id}]"

    plain_text = f"""Dear {name},

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
{verify_url}

Please visit the link above to view your complete credential dossier and review your verification status.

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
{portal_url}
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DBERT Internship Verification</title>
</head>
<body style="margin:0;padding:24px 12px;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:600px;margin:0 auto;background-color:#141A23;border:1px solid #232A36;border-radius:10px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
    <!-- Header -->
    <div style="background-color:#0E1626;padding:24px 28px;text-align:center;border-bottom:2px solid #E2B96F;">
      <h1 style="color:#ffffff;font-size:22px;font-weight:800;letter-spacing:1.5px;margin:0 0 4px 0;">DBERT</h1>
      <p style="color:#8A9AB5;font-size:12px;letter-spacing:0.5px;margin:0;text-transform:uppercase;">Digital Blinc Education Research and Technology</p>
    </div>

    <!-- Content -->
    <div style="padding:28px 26px;">
      <p style="font-size:16px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;">
        Dear {name},
      </p>
      
      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 20px 0;">
        Your official technical incubation and internship program record with <strong>DBERT</strong> has been recorded on the verification portal.
      </p>

      <!-- Record Table Card -->
      <div style="background-color:#0F141C;border:1px solid #1E2633;border-radius:8px;padding:18px 20px;margin:0 0 24px 0;">
        <div style="font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#E2B96F;margin:0 0 12px 0;padding-bottom:6px;border-bottom:1px solid #1E2633;">
          Official Credential Record
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;width:38%;">Candidate Name:</td>
            <td style="padding:5px 0;color:#F0F4F8;font-weight:600;">{name}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Domain Track:</td>
            <td style="padding:5px 0;color:#E2B96F;font-weight:700;">{domain}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Program Tenure:</td>
            <td style="padding:5px 0;color:#F0F4F8;font-weight:600;">{duration}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Core Project:</td>
            <td style="padding:5px 0;color:#F0F4F8;font-weight:600;">{project}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Academic Evaluation:</td>
            <td style="padding:5px 0;color:#E2B96F;font-weight:700;">{score}/100 ({grade})</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Certificate ID:</td>
            <td style="padding:5px 0;color:#38BDF8;font-family:Menlo,Consolas,monospace;font-weight:600;">{cert_id}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Permanent Intern ID:</td>
            <td style="padding:5px 0;color:#38BDF8;font-family:Menlo,Consolas,monospace;font-weight:600;">{intern_id}</td>
          </tr>
        </table>
      </div>

      <!-- CTA Button -->
      <div style="text-align:center;margin:28px 0 24px 0;">
        <a href="{verify_url}" target="_blank" style="display:inline-block;background-color:#E2B96F;color:#0B0F17;font-weight:700;font-size:14px;text-decoration:none;padding:13px 30px;border-radius:6px;box-shadow:0 2px 8px rgba(226,185,111,0.25);">
          View Credential Dossier &rarr;
        </a>
        <div style="margin-top:10px;font-size:12px;color:#8A9AB5;">
          Direct Link: <a href="{verify_url}" style="color:#38BDF8;text-decoration:none;">{verify_url}</a>
        </div>
      </div>

      <!-- Signoff -->
      <div style="border-top:1px solid #1E2633;padding-top:18px;margin-top:20px;font-size:13px;line-height:1.6;color:#CBD5E1;">
        Sincerely,<br>
        <strong style="color:#F0F4F8;font-size:14px;">Abhinav Sharma</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">Program Head & Project Mentor<br>DBERT (Digital Blinc Education Research and Technology)</span>
      </div>
    </div>

    <!-- Footer -->
    <div style="background-color:#0E1626;padding:16px 20px;text-align:center;border-top:1px solid #1E2633;font-size:11.5px;color:#8A9AB5;line-height:1.6;">
      Official Verification Portal: <a href="{portal_url}" style="color:#E2B96F;text-decoration:none;font-weight:600;">dbert.in/verify</a> &nbsp;&bull;&nbsp;
      Official Support: <a href="mailto:support@dbert.in" style="color:#E2B96F;text-decoration:none;">support@dbert.in</a><br>
      &copy; 2026 DBERT &middot; Sovereign Technical Incubation Registry &middot; All Rights Reserved.
    </div>
  </div>
</body>
</html>"""

    return subject, plain_text, html_content


def send_milestone_report(
    service: EmailDeliveryService,
    current_count: int,
    total_count: int,
    start_time: float,
    recent_records: list[dict],
    is_live: bool
):
    """Sends a formatted milestone telemetry report to ain and ajna."""
    pct = (current_count / total_count) * 100 if total_count > 0 else 0
    elapsed_sec = time.time() - start_time
    elapsed_str = str(timedelta(seconds=int(elapsed_sec)))
    
    # Calculate ETA
    if current_count > 0:
        avg_per_email = elapsed_sec / current_count
        remaining_sec = avg_per_email * (total_count - current_count)
        eta_str = str(timedelta(seconds=int(remaining_sec)))
    else:
        eta_str = "Calculating..."

    subject = f"DBERT Batch Dispatch Report: Milestone {current_count}/{total_count} ({pct:.1f}%) Completed"

    table_rows = ""
    for r in recent_records[-10:]:
        status_color = "#10B981" if r["status"] == "SENT" else "#EF4444"
        table_rows += f"""<tr>
          <td style="padding:6px;border-bottom:1px solid #1E2633;color:#F0F4F8;">#{r['index']} {r['holderName']}</td>
          <td style="padding:6px;border-bottom:1px solid #1E2633;color:#38BDF8;font-family:monospace;">{r['certId']}</td>
          <td style="padding:6px;border-bottom:1px solid #1E2633;color:#8A9AB5;">{r['email']}</td>
          <td style="padding:6px;border-bottom:1px solid #1E2633;color:{status_color};font-weight:bold;">{r['status']}</td>
          <td style="padding:6px;border-bottom:1px solid #1E2633;color:#8A9AB5;font-size:11px;">{r.get('sent_at') or 'N/A'}</td>
        </tr>"""

    html_content = f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:20px;background:#0B0F17;font-family:Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:650px;margin:0 auto;background:#141A23;border:1px solid #232A36;border-radius:8px;padding:24px;">
    <h2 style="color:#E2B96F;margin:0 0 6px;">DBERT Batch Dispatch Progress Report</h2>
    <p style="color:#8A9AB5;font-size:13px;margin:0 0 18px;">
      Milestone Reached: <strong>{current_count} / {total_count}</strong> ({pct:.1f}% Complete)
    </p>

    <div style="background:#0F141C;border:1px solid #1E2633;border-radius:6px;padding:16px;margin-bottom:20px;">
      <table style="width:100%;font-size:13px;color:#CBD5E1;">
        <tr><td style="padding:4px 0;">Current Status:</td><td style="font-weight:bold;color:#10B981;">{current_count} Dispatched Successfully</td></tr>
        <tr><td style="padding:4px 0;">Elapsed Time:</td><td>{elapsed_str}</td></tr>
        <tr><td style="padding:4px 0;">Estimated Time Remaining:</td><td>{eta_str}</td></tr>
        <tr><td style="padding:4px 0;">Configured Pacing:</td><td>30.0 seconds / email</td></tr>
        <tr><td style="padding:4px 0;">Sender & Reply-To:</td><td>Abhinav Sharma &lt;abhinav.sharma@dbert.in&gt;</td></tr>
      </table>
    </div>

    <h3 style="color:#F0F4F8;font-size:14px;margin:0 0 10px;">Recent 10 Dispatches:</h3>
    <table style="width:100%;border-collapse:collapse;font-size:12px;background:#0F141C;border-radius:4px;overflow:hidden;">
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

    <div style="margin-top:20px;font-size:11px;color:#8A9AB5;text-align:center;">
      This is an automated operational progress report generated by the DBERT Batch Dispatch Engine.
    </div>
  </div>
</body>
</html>"""

    plain_content = f"""DBERT Batch Dispatch Progress Report
===================================================
Milestone: {current_count} / {total_count} ({pct:.1f}% Complete)
Elapsed Time: {elapsed_str}
Estimated Remaining: {eta_str}
Sender & Reply-To: Abhinav Sharma <abhinav.sharma@dbert.in>

Recent Dispatches:
"""
    for r in recent_records[-10:]:
        plain_content += f"- #{r['index']} {r['holderName']} [{r['certId']}] -> {r['email']} ({r['status']})\n"

    log_message(f"--- Sending Milestone Telemetry Report for #{current_count}/{total_count} ---")
    for rcpt_email, rcpt_label in TELEMETRY_RECIPIENTS:
        try:
            res = service.send_email(
                to=rcpt_email,
                subject=subject,
                html_content=html_content,
                text_content=plain_content,
                dry_run=not is_live
            )
            log_message(f"  Milestone report sent to {rcpt_label} <{rcpt_email}>: {'SUCCESS' if res.success else 'FAILED'} (Message-ID: {res.message_id})")
        except Exception as e:
            log_message(f"  Failed sending milestone report to {rcpt_email}: {e}")


def main():
    parser = argparse.ArgumentParser(description="409 Provisional Candidates Batch Dispatch Runner")
    parser.add_argument("--live", action="store_true", help="Execute live outbound SMTP dispatch (default is dry-run)")
    parser.add_argument("--dry-run", action="store_true", help="Explicitly enforce dry-run simulation mode")
    parser.add_argument("--delay", type=float, default=30.0, help="Pacing interval in seconds between emails (default: 30.0)")
    parser.add_argument("--report-interval", type=int, default=100, help="Dispatches between milestone reports (default: 100)")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit on number of candidates to process in this run")
    parser.add_argument("--start-from", type=int, default=None, help="Optional override for starting 1-based index")
    args = parser.parse_args()

    is_live = args.live and not args.dry_run
    delay = args.delay
    report_interval = args.report_interval
    limit = args.limit
    start_from = args.start_from

    print("=" * 76)
    print("      DBERT 409 PROVISIONAL CANDIDATE BATCH DISPATCH ENGINE")
    print("=" * 76)
    print(f" Mode:                   {'[LIVE OUTBOUND SMTP SEND]' if is_live else '[DRY-RUN SIMULATION (ZERO NETWORK CALLS)]'}")
    print(f" Inter-Message Pacing:   {delay}s")
    print(f" Milestone Reporting:    Every {report_interval} emails -> ain & ajna")
    print(f" Sender & Reply-To:      {FROM_NAME} <{FROM_EMAIL}>")
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
    tracking = load_or_init_tracking(registry)

    # 4. Initialize Delivery Engine
    # Note: Pacer interval is configured to `delay` (default 30.0s)
    service = EmailDeliveryService(
        smtp_host=os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.environ.get("SMTP_PORT", "465")),
        smtp_user=os.environ.get("SMTP_USER", "abhinav.sharma@dbert.in"),
        smtp_pass=os.environ.get("SMTP_PASS", "rsupmvvvvwrsuxuh"),
        from_name=FROM_NAME,
        from_email=FROM_EMAIL,
        reply_to=REPLY_TO_EMAIL,  # Exactly matching sender email address
        pacer=EmailPacer(default_interval=delay)
    )

    log_message(f"Delivery engine initialized (SMTP: {service.smtp_host}:{service.smtp_port}, Reply-To: {service.reply_to}).")

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
    total_in_session = len(candidates_to_process)
    already_sent = sum(1 for x in tracking if x["status"] == "SENT")

    log_message(f"Commencing batch dispatch loop at {delay}s pacing...")

    for cand in candidates_to_process:
        idx = cand["index"]
        name = cand["holderName"]
        email = cand["email"]
        cert_id = cand["certId"]

        log_message(f"\n>>> [{idx}/{len(tracking)}] Dispatching to: {name} <{email}> [{cert_id}]")

        subject, plain_text, html_content = build_candidate_email(cand)

        try:
            res = service.send_email(
                to=email,
                subject=subject,
                html_content=html_content,
                text_content=plain_text,
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
                    cand["status"] = "PENDING"
                    cand["error"] = res.error
                    log_message(f"  [QUOTA LIMIT DETECTED] Google daily sending limit active: {res.error}")
                    log_message("  [CIRCUIT BREAKER] Halting batch dispatch gracefully until quota unlocks.")
                    save_tracking_state(tracking)
                    sys.exit(55)
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

        # Milestone Telemetry Check (every report_interval OR when all 409 are complete)
        if (current_cumulative_sent > 0 and current_cumulative_sent % report_interval == 0) or (current_cumulative_sent == len(tracking)):
            send_milestone_report(
                service=service,
                current_count=current_cumulative_sent,
                total_count=len(tracking),
                start_time=start_time,
                recent_records=tracking[:current_cumulative_sent],
                is_live=is_live
            )

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
