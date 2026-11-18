import os
import sys
import json
import time
import random
import argparse
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
DATA_DIR = ROOT_DIR / "data"

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
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

from services.delivery_service import EmailDeliveryService

COHORT_FILE = DATA_DIR / "active_54h_cohort.json"
TRACKING_FILE = DATA_DIR / "dispatch_tracking_active_54h.json"
LOG_FILE = DATA_DIR / "dispatch_active_54h.log"

TELEMETRY_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

# 5 SMTP Accounts
SMTP_ACCOUNTS = [
    {
        "user": "abhinav.sharma@dbert.in",
        "pass": "rsupmvvvvwrsuxuh",
        "name": "Abhinav Sharma",
        "role": "Program Head & Project Mentor"
    },
    {
        "user": "manoj.kumar@dbert.in",
        "pass": "fnevtpseplwibckr",
        "name": "Manoj Kumar",
        "role": "Academic Lead & Admissions"
    },
    {
        "user": "sandeep.bannu@dbert.in",
        "pass": "qtqzlmrynbcxvyjy",
        "name": "Sandeep Bannu",
        "role": "Technical Program Operations"
    },
    {
        "user": "contactus@dbert.in",
        "pass": "llvmaajmrljpcwru",
        "name": "DBERT Admissions & Verification",
        "role": "Admissions & Verification Concierge"
    },
    {
        "user": "pulkit.kunar@dbert.in",
        "pass": "vzefecwpggxuaztr",
        "name": "Pulkit Kumar",
        "role": "Technical Mentorship & Verification"
    }
]

def log_msg(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def get_sender_service(acct_info: dict) -> EmailDeliveryService:
    return EmailDeliveryService(
        smtp_host=os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.environ.get("SMTP_PORT", "465")),
        smtp_user=acct_info["user"],
        smtp_pass=acct_info["pass"],
        from_name=acct_info["name"],
        from_email=acct_info["user"],
        reply_to=acct_info["user"]
    )

def build_whatsapp_buttons(cand: dict) -> str:
    name = cand.get("name", "Candidate")
    domain = cand.get("domain", "Engineering")
    email = cand.get("email", "")
    seg = cand.get("segment", "")
    
    adm_text = quote(f"Hi DBERT Admissions, I am {name} ({email}). Query regarding my {domain} fellowship ({seg}).")
    men_text = quote(f"Hi DBERT Mentorship, I am {name} ({email}). Query regarding my sprint tasks for {domain}.")

    return f"""
    <!-- Dual WhatsApp Support Concierge -->
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:16px 20px;margin:24px 0 20px;">
      <div style="font-size:12px;font-weight:700;color:#E2B96F;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">
        💬 1-Tap Dedicated WhatsApp Concierge
      </div>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <a href="https://wa.me/918192911360?text={adm_text}" target="_blank" rel="noopener" style="flex:1;min-width:200px;background:#25D366;color:#0B0F17;font-weight:700;font-size:12px;padding:10px 16px;border-radius:8px;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:6px;box-shadow:0 3px 10px rgba(37,211,102,0.25);">
          📱 Admissions &amp; Payments (+91 81929 11360)
        </a>
        <a href="https://wa.me/918958006294?text={men_text}" target="_blank" rel="noopener" style="flex:1;min-width:200px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.18);color:#F0F4F8;font-weight:700;font-size:12px;padding:10px 16px;border-radius:8px;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:6px;">
          ⚡ Sprints &amp; Mentorship (+91 89580 06294)
        </a>
      </div>
      <p style="font-size:11px;color:#8A9AB5;margin:8px 0 0;line-height:1.4;">
        Available Mon–Sat, 10:00 AM – 8:00 PM IST for instant verification, UTR confirmation, and technical mentorship.
      </p>
    </div>
    """

# TEMPLATE 1: SELECTED
def build_selected_email(cand: dict, sender: dict) -> tuple[str, str, str]:
    name = cand["name"]
    domain = cand["domain"]
    subject = f"DBERT Fellowship Selection Notice — Confirm Your Committed Seat & Batch [{domain}]"
    wa_block = build_whatsapp_buttons(cand)

    plain = f"""Dear {name},

Congratulations! Your application for the DBERT Technical Fellowship in {domain} has cleared evaluation and been officially SELECTED.

Your committed seat reservation is now active. To confirm your batch kickoff date and unlock your curriculum and mentor sprints, please complete your enrollment confirmation:

1. Log in to your portal: https://lms.dbert.in/portal
2. Select your batch kickoff Monday (recent batch for instant unlock or upcoming cohort).
3. Complete the committed seat caution deposit (₹499) via 1-tap UPI (GPay, PhonePe, Paytm) or submit your 12-digit UPI UTR.
4. Your caution deposit is 100% refundable upon fellowship milestone completion.

Instant Support:
- Admissions WhatsApp: +91 81929 11360
- Technical Mentorship: +91 89580 06294

Sincerely,
{sender['name']}
{sender['role']}
DBERT (Digital Blinc Education Research and Technology)
Platform: https://lms.dbert.in
"""

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:12px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    <div style="background-color:#0E1626;padding:24px;text-align:center;border-bottom:2px solid #E2B96F;">
      <div style="color:#E2B96F;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:11px;letter-spacing:1px;margin-top:4px;">SOVEREIGN TECHNICAL INCUBATION PLATFORM</div>
    </div>
    <div style="padding:30px 28px;">
      <div style="display:inline-block;background:rgba(16,185,129,0.15);color:#10B981;font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 12px;border-radius:20px;border:1px solid rgba(16,185,129,0.3);margin-bottom:16px;">
        &#10003; APPLICATION SELECTED &middot; ADMISSIONS CONFIRMATION
      </div>
      <h1 style="font-size:20px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;">
        Congratulations {name}! You Have Been Selected for {domain}
      </h1>
      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 18px 0;">
        Dear <strong>{name}</strong>,<br><br>
        We are pleased to inform you that your application for the <strong>{domain}</strong> Fellowship track has been approved by the DBERT Admissions and Academic Mentorship Board.
      </p>

      <!-- Action Card -->
      <div style="background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.3);border-radius:10px;padding:18px 20px;margin-bottom:24px;">
        <div style="color:#A5B4FC;font-size:13px;font-weight:700;margin-bottom:8px;">
          🚀 Final Step: Choose Batch Date &amp; Confirm Your Seat
        </div>
        <p style="font-size:13px;color:#E2E8F0;line-height:1.6;margin:0 0 14px 0;">
          To guarantee committed participation, candidates confirm their seat with a <strong>₹499 refundable caution deposit</strong>. You can pay seamlessly via 1-tap UPI or submit your 12-digit transaction UTR directly on the portal.
        </p>
        <div style="text-align:center;">
          <a href="https://lms.dbert.in/portal#signin" style="display:inline-block;background:linear-gradient(135deg, #E2B96F, #C59A4E);color:#0B0F17;font-weight:700;font-size:13px;padding:12px 28px;border-radius:6px;text-decoration:none;box-shadow:0 4px 15px rgba(226,185,111,0.3);">
            Log In &amp; Finalize Enrollment &rarr;
          </a>
        </div>
      </div>

      <!-- Feature Highlights -->
      <div style="background:#0F141C;border:1px solid #1E2633;border-radius:8px;padding:18px;margin-bottom:20px;font-size:12.5px;color:#CBD5E1;line-height:1.6;">
        <strong style="color:#F0F4F8;">What Unlocks Upon Confirmation:</strong>
        <ul style="margin:8px 0 0;padding-left:18px;">
          <li>Full access to production-grade curriculum, assignments, and AI tutor</li>
          <li>Live project architecture reviews with senior industry mentors</li>
          <li>Eligibility for the <strong>₹5,000 Milestone Release</strong> upon completing the 4 advancement gates</li>
        </ul>
      </div>

      {wa_block}

      <div style="border-top:1px solid #1E2633;padding-top:16px;margin-top:20px;">
        <strong style="color:#F0F4F8;font-size:13px;">{sender['name']}</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">{sender['role']}<br>DBERT Admissions &amp; Academic Operations</span>
      </div>
    </div>
    <div style="background-color:#0E1626;padding:14px 20px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#8A9AB5;">
      DBERT &middot; Sovereign Technical Incubation Platform &middot; <a href="https://lms.dbert.in" style="color:#E2B96F;text-decoration:none;">lms.dbert.in</a>
    </div>
  </div>
</body>
</html>"""
    return subject, plain, html

# TEMPLATE 2: UNDER REVIEW
def build_under_review_email(cand: dict, sender: dict) -> tuple[str, str, str]:
    name = cand["name"]
    domain = cand["domain"]
    subject = f"Application Update: Your DBERT Fellowship File is in Priority Review [{domain}]"
    wa_block = build_whatsapp_buttons(cand)

    plain = f"""Dear {name},

Thank you for your active engagement with the DBERT Technical Incubation Platform for {domain}.

We noticed your recent activity on the portal. Your application is currently under priority review by our technical mentors and admissions board.

To accelerate your review:
1. Log in to your portal: https://lms.dbert.in/portal
2. Ensure your academic profile, degree course, and college details are complete.
3. Submit a strong Statement of Purpose (minimum 80 characters) detailing your technical goals.
4. Add your GitHub profile or technical portfolio link.

If you have urgent queries or require fast-track prioritization, you can reach out directly:
- Admissions WhatsApp: +91 81929 11360
- Technical Mentorship: +91 89580 06294

Sincerely,
{sender['name']}
{sender['role']}
DBERT
"""

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:12px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    <div style="background-color:#0E1626;padding:24px;text-align:center;border-bottom:2px solid #38BDF8;">
      <div style="color:#E2B96F;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:11px;letter-spacing:1px;margin-top:4px;">SOVEREIGN TECHNICAL INCUBATION PLATFORM</div>
    </div>
    <div style="padding:30px 28px;">
      <div style="display:inline-block;background:rgba(56,189,248,0.15);color:#38BDF8;font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 12px;border-radius:20px;border:1px solid rgba(56,189,248,0.3);margin-bottom:16px;">
        &#9203; APPLICATION FILE UNDER ACTIVE REVIEW
      </div>
      <h1 style="font-size:20px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;">
        Application Status Update for {name}
      </h1>
      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 18px 0;">
        Dear <strong>{name}</strong>,<br><br>
        We have received your application for the <strong>{domain}</strong> Fellowship track. Our admissions board and domain mentors are currently evaluating incoming profiles for the upcoming batch.
      </p>

      <!-- Acceleration Card -->
      <div style="background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.25);border-radius:10px;padding:18px 20px;margin-bottom:24px;">
        <div style="color:#38BDF8;font-size:13px;font-weight:700;margin-bottom:8px;">
          ⚡ How to Expedite Your Selection Decision:
        </div>
        <ul style="margin:0;padding-left:18px;color:#E2E8F0;font-size:12.5px;line-height:1.6;">
          <li>Ensure your college name and degree course are accurately entered</li>
          <li>Complete your Statement of Purpose (SOP) explaining your technical interest</li>
          <li>Link your GitHub profile or project portfolio for mentor review</li>
        </ul>
        <div style="text-align:center;margin-top:16px;">
          <a href="https://lms.dbert.in/portal#signin" style="display:inline-block;background:#38BDF8;color:#0B0F17;font-weight:700;font-size:13px;padding:11px 26px;border-radius:6px;text-decoration:none;">
            Review Profile on LMS &rarr;
          </a>
        </div>
      </div>

      {wa_block}

      <div style="border-top:1px solid #1E2633;padding-top:16px;margin-top:20px;">
        <strong style="color:#F0F4F8;font-size:13px;">{sender['name']}</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">{sender['role']}<br>DBERT Admissions Review Board</span>
      </div>
    </div>
    <div style="background-color:#0E1626;padding:14px 20px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#8A9AB5;">
      DBERT &middot; Sovereign Technical Incubation Platform &middot; <a href="https://lms.dbert.in" style="color:#E2B96F;text-decoration:none;">lms.dbert.in</a>
    </div>
  </div>
</body>
</html>"""
    return subject, plain, html

# TEMPLATE 3: ENROLLMENT PENDING / FLAGGED DEPOSIT
def build_enrollment_pending_email(cand: dict, sender: dict) -> tuple[str, str, str]:
    name = cand["name"]
    domain = cand["domain"]
    subject = f"Action Needed: Complete Your ₹499 Deposit Verification for DBERT Fellowship"
    wa_block = build_whatsapp_buttons(cand)

    plain = f"""Dear {name},

We are reaching out regarding your ₹499 caution deposit for the DBERT {domain} Fellowship.

Your seat reservation is on hold pending transaction reconciliation. To ensure your enrollment is activated without delay:

1. Log in to your portal: https://lms.dbert.in/portal
2. Locate the deposit confirmation section.
3. Submit the exact 12-digit UPI UTR (Transaction ID) from your payment receipt (found in GPay, PhonePe, Paytm, or your bank SMS).
4. If you have already paid, NO duplicate payment is required—entering the 12-digit UTR immediately registers your transaction in the ledger.

For instant manual reconciliation:
- WhatsApp Admissions: +91 81929 11360 (Send your UTR or receipt screenshot)

Sincerely,
{sender['name']}
{sender['role']}
DBERT Admissions
"""

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:12px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    <div style="background-color:#0E1626;padding:24px;text-align:center;border-bottom:2px solid #F59E0B;">
      <div style="color:#E2B96F;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:11px;letter-spacing:1px;margin-top:4px;">SOVEREIGN TECHNICAL INCUBATION PLATFORM</div>
    </div>
    <div style="padding:30px 28px;">
      <div style="display:inline-block;background:rgba(245,158,11,0.15);color:#FBBF24;font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 12px;border-radius:20px;border:1px solid rgba(245,158,11,0.3);margin-bottom:16px;">
        &#9888; ACTION NEEDED &middot; TRANSACTION RECONCILIATION
      </div>
      <h1 style="font-size:20px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;">
        Complete Your ₹499 Deposit Verification for {domain}
      </h1>
      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 18px 0;">
        Dear <strong>{name}</strong>,<br><br>
        Your application for the <strong>{domain}</strong> Fellowship is selected, but your ₹499 caution deposit requires transaction reconciliation to confirm your batch kickoff date.
      </p>

      <!-- Resolution Box -->
      <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.3);border-radius:10px;padding:18px 20px;margin-bottom:24px;">
        <div style="color:#FBBF24;font-size:13px;font-weight:700;margin-bottom:8px;">
          📌 Enter Your 12-Digit UPI UTR for Instant Clearance:
        </div>
        <p style="font-size:13px;color:#E2E8F0;line-height:1.6;margin:0 0 14px 0;">
          If you have completed your payment, please log in to the portal and enter the <strong>12-digit numeric UTR</strong> from your UPI confirmation screen. No duplicate payment is needed!
        </p>
        <div style="text-align:center;">
          <a href="https://lms.dbert.in/portal#signin" style="display:inline-block;background:#F59E0B;color:#0B0F17;font-weight:700;font-size:13px;padding:11px 26px;border-radius:6px;text-decoration:none;">
            Enter UTR on Portal &rarr;
          </a>
        </div>
      </div>

      {wa_block}

      <div style="border-top:1px solid #1E2633;padding-top:16px;margin-top:20px;">
        <strong style="color:#F0F4F8;font-size:13px;">{sender['name']}</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">{sender['role']}<br>DBERT Admissions Ledger Desk</span>
      </div>
    </div>
    <div style="background-color:#0E1626;padding:14px 20px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#8A9AB5;">
      DBERT &middot; Sovereign Technical Incubation Platform &middot; <a href="https://lms.dbert.in" style="color:#E2B96F;text-decoration:none;">lms.dbert.in</a>
    </div>
  </div>
</body>
</html>"""
    return subject, plain, html

# TEMPLATE 4: ENROLLED SPRINT FELLOWS (STIPEND GATES)
def build_enrolled_fellow_email(cand: dict, sender: dict) -> tuple[str, str, str]:
    name = cand["name"]
    domain = cand["domain"]
    g1 = cand.get("g1_linkedin", False)
    g2 = cand.get("g2_article", False)
    g3 = cand.get("g3_verified", False)
    g4 = cand.get("g4_github", False)

    completed_cnt = (1 if g1 else 0) + (1 if g2 else 0) + (1 if g3 else 0) + (1 if g4 else 0)
    subject = f"Sprint Milestone Status: Progress Toward Your ₹5,000 Stipend Release [{domain}]"
    wa_block = build_whatsapp_buttons(cand)

    # Determine next single missing step
    if not g1:
        next_step = "Link your public LinkedIn Profile URL on your LMS profile"
        next_cta = "Link LinkedIn Profile →"
        next_url = "https://lms.dbert.in/intern/profile"
    elif not g2:
        next_step = "Draft and submit your Technical Problem-Solving Case Study"
        next_cta = "Draft Technical Case Study →"
        next_url = "https://lms.dbert.in/intern/articles"
    elif not g3:
        next_step = "Complete official credential verification"
        next_cta = "Verify Credentials →"
        next_url = "https://lms.dbert.in/stipend/tasks"
    elif not g4:
        next_step = "Submit your active GitHub project repository and deployment link"
        next_cta = "Submit GitHub Codebase →"
        next_url = "https://lms.dbert.in/stipend/tasks"
    else:
        next_step = "All 4 Gates Unlocked! Confirm your encrypted UPI ID on the portal"
        next_cta = "Confirm UPI ID for Release →"
        next_url = "https://lms.dbert.in/stipend/tasks"

    plain = f"""Dear {name},

Here is your official milestone progression report for the DBERT {domain} Fellowship.

Your Current 4-Gate Stipend Progress: {completed_cnt}/4 Gates Complete
--------------------------------------------------------------------------------
- Gate 1: LinkedIn Profile Connection:   {'[✓ COMPLETED]' if g1 else '[⏳ ACTION NEEDED: Link Profile]'}
- Gate 2: Technical Case Study Article:  {'[✓ PUBLISHED]' if g2 else '[⏳ ACTION NEEDED: Submit Article]'}
- Gate 3: Official Credential Status:    {'[✓ VERIFIED]' if g3 else '[⏳ PROVISIONAL]'}
- Gate 4: Active GitHub Repository:      {'[✓ SUBMITTED]' if g4 else '[⏳ ACTION NEEDED: Add Repo URL]'}
--------------------------------------------------------------------------------

Target: Release of ₹5,000 Milestone Grant directly to your UPI account upon completing all 4 gates.

Your Priority Next Step:
👉 {next_step}
Direct Link: {next_url}

Need guidance? Reach out:
- Admissions WhatsApp: +91 81929 11360
- Technical Mentorship: +91 89580 06294

Sincerely,
{sender['name']}
{sender['role']}
DBERT Fellowship Directorate
"""

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:12px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    <div style="background-color:#0E1626;padding:24px;text-align:center;border-bottom:2px solid #10B981;">
      <div style="color:#E2B96F;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:11px;letter-spacing:1px;margin-top:4px;">FELLOWSHIP ADVANCEMENT ENGINE &middot; STIPEND MILESTONE</div>
    </div>
    <div style="padding:30px 28px;">
      <div style="display:inline-block;background:rgba(16,185,129,0.15);color:#10B981;font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 12px;border-radius:20px;border:1px solid rgba(16,185,129,0.3);margin-bottom:16px;">
        &#9889; ACTIVE SPRINT FELLOW &middot; {completed_cnt}/4 GATES COMPLETE
      </div>
      <h1 style="font-size:20px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;">
        Your Milestone Progression toward ₹5,000 Stipend Release
      </h1>
      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 18px 0;">
        Dear <strong>{name}</strong>,<br><br>
        As an active fellow in the <strong>{domain}</strong> track, completing all 4 milestone gates unlocks your official grant of <strong>5,000 Coins (₹5,000)</strong> credited directly to your withdrawable UPI wallet.
      </p>

      <!-- 4-Gate Scorecard -->
      <div style="background:#0F141C;border:1px solid #1E2633;border-radius:10px;padding:20px;margin-bottom:22px;">
        <div style="font-size:11px;color:#E2B96F;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:14px;">
          AUTHENTICATED PROGRESS SCORECARD
        </div>
        <table style="width:100%;font-size:13px;border-collapse:collapse;">
          <tr style="border-bottom:1px solid #1A2230;">
            <td style="padding:8px 0;color:#CBD5E1;">Gate 1: LinkedIn Profile Connection</td>
            <td style="padding:8px 0;text-align:right;font-weight:700;color:{'#10B981' if g1 else '#F59E0B'};">{'✓ COMPLETED' if g1 else '⏳ ACTION NEEDED'}</td>
          </tr>
          <tr style="border-bottom:1px solid #1A2230;">
            <td style="padding:8px 0;color:#CBD5E1;">Gate 2: Technical Case Study Article</td>
            <td style="padding:8px 0;text-align:right;font-weight:700;color:{'#10B981' if g2 else '#F59E0B'};">{'✓ PUBLISHED' if g2 else '⏳ ACTION NEEDED'}</td>
          </tr>
          <tr style="border-bottom:1px solid #1A2230;">
            <td style="padding:8px 0;color:#CBD5E1;">Gate 3: Official Credential Status</td>
            <td style="padding:8px 0;text-align:right;font-weight:700;color:{'#10B981' if g3 else '#F59E0B'};">{'✓ VERIFIED' if g3 else '⏳ PROVISIONAL'}</td>
          </tr>
          <tr>
            <td style="padding:8px 0;color:#CBD5E1;">Gate 4: Active GitHub Repository</td>
            <td style="padding:8px 0;text-align:right;font-weight:700;color:{'#10B981' if g4 else '#F59E0B'};">{'✓ SUBMITTED' if g4 else '⏳ ACTION NEEDED'}</td>
          </tr>
        </table>
      </div>

      <!-- Action Card -->
      <div style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:10px;padding:18px 20px;margin-bottom:24px;">
        <div style="color:#10B981;font-size:13px;font-weight:700;margin-bottom:6px;">
          🎯 Your Priority Next Step:
        </div>
        <p style="font-size:13px;color:#E2E8F0;line-height:1.6;margin:0 0 14px 0;">
          <strong>{next_step}</strong> to advance your stipend milestone.
        </p>
        <div style="text-align:center;">
          <a href="{next_url}" style="display:inline-block;background:#10B981;color:#022C22;font-weight:800;font-size:13px;padding:12px 28px;border-radius:6px;text-decoration:none;box-shadow:0 4px 15px rgba(16,185,129,0.3);">
            {next_cta}
          </a>
        </div>
      </div>

      {wa_block}

      <div style="border-top:1px solid #1E2633;padding-top:16px;margin-top:20px;">
        <strong style="color:#F0F4F8;font-size:13px;">{sender['name']}</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">{sender['role']}<br>DBERT Fellowship Mentorship Directorate</span>
      </div>
    </div>
    <div style="background-color:#0E1626;padding:14px 20px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#8A9AB5;">
      DBERT &middot; Sovereign Technical Incubation Platform &middot; <a href="https://lms.dbert.in" style="color:#E2B96F;text-decoration:none;">lms.dbert.in</a>
    </div>
  </div>
</body>
</html>"""
    return subject, plain, html

# TEMPLATE 5: VERIFIED ALUMNI
def build_verified_alumni_email(cand: dict, sender: dict) -> tuple[str, str, str]:
    name = cand["name"]
    domain = cand["domain"]
    cert_id = cand.get("cert_id") or "CERT-DBERT-2026"
    verify_url = f"https://dbert.in/verify/{cert_id}"
    subject = f"Your Sovereign Verification Dossier & Pre-Vetted Directory Placement [{cert_id}]"
    wa_block = build_whatsapp_buttons(cand)

    plain = f"""Dear {name},

Your official credential in {domain} is fully verified and cryptographically active on the sovereign verification engine:
{verify_url}

Your credential includes:
- Certificate of Completion with embedded verification QR code
- 9-Dimension Academic Project Evaluation rubric
- Formal Letter of Recommendation

View Dossier: {verify_url}
Pre-Vetted Directory: https://dbert.in/verify/directory

Sincerely,
{sender['name']}
{sender['role']}
DBERT
"""

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:12px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    <div style="background-color:#0E1626;padding:24px;text-align:center;border-bottom:2px solid #E2B96F;">
      <div style="color:#E2B96F;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:11px;letter-spacing:1px;margin-top:4px;">SOVEREIGN TECHNICAL INCUBATION PLATFORM</div>
    </div>
    <div style="padding:30px 28px;">
      <div style="display:inline-block;background:rgba(16,185,129,0.15);color:#10B981;font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 12px;border-radius:20px;border:1px solid rgba(16,185,129,0.3);margin-bottom:16px;">
        &#10003; VERIFIED CREDENTIAL &middot; PRE-VETTED DIRECTORY ACTIVE
      </div>
      <h1 style="font-size:20px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;">
        Official Verified Credential Dossier for {name}
      </h1>
      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 18px 0;">
        Dear <strong>{name}</strong>,<br><br>
        Your official credentials in <strong>{domain}</strong> (Certificate ID: <code>{cert_id}</code>) are permanently active on the sovereign verification registry and featured on the DBERT Pre-Vetted Engineers Directory.
      </p>

      <div style="text-align:center;margin:24px 0;">
        <a href="{verify_url}" style="display:inline-block;background:linear-gradient(135deg, #E2B96F, #C59A4E);color:#0B0F17;font-weight:700;font-size:13px;padding:12px 28px;border-radius:6px;text-decoration:none;box-shadow:0 4px 15px rgba(226,185,111,0.3);">
          View Live Verification Dossier &rarr;
        </a>
      </div>

      {wa_block}

      <div style="border-top:1px solid #1E2633;padding-top:16px;margin-top:20px;">
        <strong style="color:#F0F4F8;font-size:13px;">{sender['name']}</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">{sender['role']}<br>DBERT Sovereign Verification Registry</span>
      </div>
    </div>
    <div style="background-color:#0E1626;padding:14px 20px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#8A9AB5;">
      DBERT &middot; Sovereign Technical Incubation Platform &middot; <a href="https://dbert.in" style="color:#E2B96F;text-decoration:none;">dbert.in</a>
    </div>
  </div>
</body>
</html>"""
    return subject, plain, html

def build_email_for_candidate(cand: dict, sender: dict) -> tuple[str, str, str]:
    seg = cand.get("segment", "SELECTED")
    if seg == "SELECTED":
        return build_selected_email(cand, sender)
    elif seg == "UNDER_REVIEW":
        return build_under_review_email(cand, sender)
    elif seg == "ENROLLMENT_PENDING":
        return build_enrollment_pending_email(cand, sender)
    elif seg == "ENROLLED_FELLOW":
        return build_enrolled_fellow_email(cand, sender)
    elif seg == "VERIFIED_ALUMNI":
        return build_verified_alumni_email(cand, sender)
    else:
        return build_selected_email(cand, sender)

def send_telemetry(sent_cnt: int, total_cnt: int, tracking: list):
    log_msg(f"Sending telemetry milestone report ({sent_cnt}/{total_cnt})...")
    service = get_sender_service(SMTP_ACCOUNTS[0])
    subject = f"[DBERT TELEMETRY] Active 54h Cohort Dispatch ({sent_cnt}/{total_cnt} Sent)"
    
    html = f"""
    <div style="font-family:Arial,sans-serif;padding:20px;background:#0F172A;color:#fff;border-radius:10px;">
      <h2 style="color:#10B981;">DBERT Active 54h Cohort Dispatch Milestone</h2>
      <p>Progress: <strong>{sent_cnt} / {total_cnt} ({sent_cnt/total_cnt*100:.1f}%)</strong> emails delivered across 5 rotating accounts.</p>
      <p>Latest delivered candidates:</p>
      <ul>
        {''.join(f'<li><strong>{x["name"]}</strong> &lt;{x["email"]}&gt; [{x["segment"]}] - Sent via {x.get("sender_email")}</li>' for x in tracking[-10:] if x["status"] == "SENT")}
      </ul>
      <p style="color:#94A3B8;font-size:12px;">Live monitoring: <a href="https://lms.dbert.in/admin" style="color:#38BDF8;">https://lms.dbert.in/admin</a></p>
    </div>
    """
    for t_em in TELEMETRY_EMAILS:
        try:
            service.send_email(
                to=t_em,
                subject=subject,
                html_content=html,
                text_content=f"Telemetry: {sent_cnt}/{total_cnt} sent.",
                dry_run=False
            )
            log_msg(f"Telemetry dispatched to {t_em}")
        except Exception as te:
            log_msg(f"Telemetry failed for {t_em}: {te}")

def main():
    parser = argparse.ArgumentParser(description="Multi-account staged dispatch for active 54h cohort")
    parser.add_argument("--test-suite", type=str, help="Send 1 sample of each of the 5 templates to specified email")
    parser.add_argument("--live", action="store_true", help="Launch live SMTP delivery")
    parser.add_argument("--dry-run", action="store_true", help="Simulate batch delivery without sending")
    parser.add_argument("--delay-min", type=float, default=18.0, help="Min delay in seconds")
    parser.add_argument("--delay-max", type=float, default=26.0, help="Max delay in seconds")
    args = parser.parse_args()

    if not COHORT_FILE.exists():
        log_msg(f"Cohort file not found: {COHORT_FILE}")
        sys.exit(1)

    with open(COHORT_FILE, "r", encoding="utf-8") as f:
        cohort = json.load(f)

    # TEST SUITE MODE
    if args.test_suite:
        test_email = args.test_suite.strip()
        log_msg(f"Executing Multi-Template Test Suite -> {test_email}")
        
        sample_cand_base = {
            "name": "Abhinav Sharma",
            "email": test_email,
            "domain": "Artificial Intelligence & Machine Learning",
            "cert_id": "CERT-DBERT-2026-AIML-092",
            "g1_linkedin": True,
            "g2_article": False,
            "g3_verified": True,
            "g4_github": False
        }

        segments = [
            ("SELECTED", "1_Selected"),
            ("UNDER_REVIEW", "2_Under_Review"),
            ("ENROLLMENT_PENDING", "3_Enrollment_Pending"),
            ("ENROLLED_FELLOW", "4_Enrolled_Fellow"),
            ("VERIFIED_ALUMNI", "5_Verified_Alumni")
        ]

        for i, (seg, label) in enumerate(segments):
            sender = SMTP_ACCOUNTS[i % len(SMTP_ACCOUNTS)]
            service = get_sender_service(sender)
            cand = dict(sample_cand_base)
            cand["segment"] = seg
            subj, plain, html = build_email_for_candidate(cand, sender)
            subj = f"[TEST SUITE {label}] {subj}"
            log_msg(f"Sending sample {label} via {sender['user']}...")
            res = service.send_email(
                to=test_email,
                subject=subj,
                html_content=html,
                text_content=plain,
                dry_run=False
            )
            if res.success:
                log_msg(f"  ✓ {label} sent! MsgID: {res.message_id}")
            else:
                log_msg(f"  ✗ {label} failed: {res.error}")
            time.sleep(3)

        log_msg("Test Suite complete!")
        return

    # BATCH DISPATCH MODE
    if TRACKING_FILE.exists():
        with open(TRACKING_FILE, "r", encoding="utf-8") as f:
            tracking = json.load(f)
    else:
        tracking = []
        for c in cohort:
            tracking.append({
                "email": c["email"],
                "name": c["name"],
                "domain": c["domain"],
                "segment": c["segment"],
                "status": "PENDING",
                "sender_email": None,
                "sent_at": None,
                "message_id": None,
                "error": None
            })
        with open(TRACKING_FILE, "w", encoding="utf-8") as f:
            json.dump(tracking, f, indent=2)

    is_live = args.live and not args.dry_run
    log_msg("=" * 80)
    log_msg(f"Starting Cohort Dispatch for {len(tracking)} candidates (Mode: {'LIVE' if is_live else 'DRY RUN'})")
    log_msg("=" * 80)

    delivered_count = sum(1 for x in tracking if x["status"] == "SENT")
    account_idx = 0

    for idx, item in enumerate(tracking):
        if item["status"] == "SENT":
            continue

        cand = cohort[idx]
        sender = SMTP_ACCOUNTS[account_idx % len(SMTP_ACCOUNTS)]
        service = get_sender_service(sender)

        subj, plain, html = build_email_for_candidate(cand, sender)
        log_msg(f">>> [{idx+1}/{len(tracking)}] Dispatching to: {cand['name']} <{cand['email']}> [{cand['segment']}] via {sender['user']}")

        try:
            res = service.send_email(
                to=cand["email"],
                subject=subj,
                html_content=html,
                text_content=plain,
                dry_run=not is_live
            )

            if res.success:
                if is_live:
                    item["status"] = "SENT"
                    item["sender_email"] = sender["user"]
                    item["sent_at"] = datetime.now().isoformat()
                    item["message_id"] = res.message_id
                    item["error"] = None
                    delivered_count += 1
                    log_msg(f"  ✓ [SUCCESS] MsgID: {res.message_id}")
                else:
                    log_msg(f"  ✓ [DRY RUN OK] Sim MsgID: {res.message_id}")
            else:
                item["status"] = "PENDING"
                item["error"] = res.error
                log_msg(f"  ✗ [FAILED] {res.error}")
                if res.error and ("550 5.4.5" in res.error or "sending limit" in res.error.lower()):
                    log_msg("  [CIRCUIT BREAKER] Daily sending limit reached on this account. Halting.")
                    if is_live:
                        with open(TRACKING_FILE, "w", encoding="utf-8") as f:
                            json.dump(tracking, f, indent=2)
                    sys.exit(55)

        except Exception as e:
            item["status"] = "PENDING"
            item["error"] = str(e)
            log_msg(f"  ✗ [EXCEPTION] {e}")

        if is_live:
            with open(TRACKING_FILE, "w", encoding="utf-8") as f:
                json.dump(tracking, f, indent=2)

            account_idx += 1

            # Milestone telemetry every 50 deliveries
            if delivered_count > 0 and delivered_count % 50 == 0:
                send_telemetry(delivered_count, len(tracking), tracking)

            delay = random.uniform(args.delay_min, args.delay_max)
            log_msg(f"  Sleeping {delay:.1f}s before next dispatch (anti-spam pacing)...")
            time.sleep(delay)

    log_msg("=" * 80)
    log_msg(f"COHORT DISPATCH COMPLETE: {delivered_count}/{len(tracking)} DELIVERED.")
    log_msg("=" * 80)

    if is_live and delivered_count > 0:
        send_telemetry(delivered_count, len(tracking), tracking)

if __name__ == "__main__":
    main()
