#!/usr/bin/env python3
"""
scripts/dispatch_discrepancy_and_roadmap.py

DBERT Dual-Track Dispatch Engine:
1. Discrepancy Cohort (10 candidates):
   - Detailed notification regarding flagged GitHub repositories (not under approved orgs:
     Alkameinc, Gayatri-Education, Aivaratechinfomatics, DBERT-INDIA) or unverified LinkedIn.
   - Explains why stipend release is paused and outlines the 3-step remediation on LMS.
2. Engaged Interns Roadmap (Batch 1: 250 candidates):
   - Comprehensive guide on how to receive Certificate of Completion (LMS quizzes + ₹299 verification form).
   - How to unlock ₹5,000 Stipend (4 gates, approved GitHub org contribution, LinkedIn experience).
   - Personalized progress bar and missing gates action items.

Rotates across 5 Google Workspace SMTP accounts with anti-spam pacing, atomic tracking, and telemetry.
"""

import os
import sys
import smtplib
import ssl
import time
import json
import argparse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from pathlib import Path
from urllib.parse import quote

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
TRACKING_FILE = DATA_DIR / "discrepancy_roadmap_tracking.json"
LOG_FILE = DATA_DIR / "discrepancy_roadmap_dispatch.log"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# 5 Authenticated Google Workspace SMTP Relay Accounts
SMTP_ACCOUNTS = [
    {
        "user": "abhinav.sharma@dbert.in",
        "pass": "rsupmvvvvwrsuxuh",
        "name": "Abhinav Sharma",
        "title": "Program Head & Project Mentor",
        "role": "DBERT Academic & Incubation Board"
    },
    {
        "user": "contactus@dbert.in",
        "pass": "llvmaajmrljpcwru",
        "name": "DBERT Admissions & Verification",
        "title": "Admissions & Verification Council",
        "role": "DBERT Academic Operations"
    },
    {
        "user": "manoj.kumar@dbert.in",
        "pass": "fnevtpseplwibckr",
        "name": "Manoj Kumar",
        "title": "Academic Lead & Admissions",
        "role": "DBERT Academic Operations"
    },
    {
        "user": "sandeep.bannu@dbert.in",
        "pass": "qtqzlmrynbcxvyjy",
        "name": "Sandeep Bannu",
        "title": "Technical Program Operations",
        "role": "DBERT Technical Fellowship Operations"
    },
    {
        "user": "pulkit.kunar@dbert.in",
        "pass": "vzefecwpggxuaztr",
        "name": "Pulkit Kumar",
        "title": "Admissions Desk & Candidate Support",
        "role": "DBERT Candidate Operations"
    }
]

TELEMETRY_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

APPROVED_ORGS = [
    {"name": "Alkameinc", "url": "https://github.com/Alkameinc"},
    {"name": "Gayatri-Education", "url": "https://github.com/Gayatri-Education"},
    {"name": "Aivaratechinfomatics", "url": "https://github.com/Aivaratechinfomatics"},
    {"name": "DBERT-INDIA", "url": "https://github.com/DBERT-INDIA"}
]

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [DISPATCH] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
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
    with open(TRACKING_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def get_smtp_connection(account: dict):
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=25)
    server.login(account["user"], account["pass"])
    return server

# ==============================================================================
# TEMPLATE 1: DISCREPANCY REVISION NOTICE (10 CANDIDATES)
# ==============================================================================

def build_discrepancy_email(c: dict, sender: dict) -> tuple:
    name = c.get("name", "Fellow")
    email = c.get("email")
    domain = c.get("domain", "Technical Fellowship")
    sub_id = c.get("submission_id", "STIPEND-SUB")
    repo_url = c.get("github_repo_url", "Submitted Repository")
    linkedin_url = c.get("linkedin_url", "")
    feedback_note = c.get("feedback_note", "")
    issues = c.get("issues", [])

    subject = f"[ACTION REQUIRED] Revision Needed on Stipend Milestone Submission — DBERT Engineering Review"

    # Plain text version
    plain_issues = []
    if "INVALID_GITHUB_ORG" in issues:
        plain_issues.append(
            "- UNAUTHORIZED GITHUB REPOSITORY: The repository you submitted does not belong to an approved DBERT organization. "
            "Under DBERT engineering policy, stipends are strictly funded for verified contributions to official partner repositories under: "
            "Alkameinc (https://github.com/Alkameinc), Gayatri-Education (https://github.com/Gayatri-Education), "
            "Aivaratechinfomatics (https://github.com/Aivaratechinfomatics), or DBERT-INDIA (https://github.com/DBERT-INDIA). "
            "Contributions to personal accounts, forks, or unapproved third-party repositories cannot be verified for stipend release."
        )
    if "UNVERIFIED_LINKEDIN" in issues:
        plain_issues.append(
            f"- UNVERIFIED LINKEDIN PROFILE: Your submitted LinkedIn URL ({linkedin_url or 'Not Provided'}) does not show DBERT under your Experience "
            "or Licenses & Certifications, or has not been linked and verified."
        )

    plain_issues_text = "\n\n".join(plain_issues)

    plain = f"""Dear {name},

This is an official communication regarding your recent Capstone & Stipend milestone submission on the DBERT LMS (Submission #{sub_id} — {domain} track).

During the evaluation of your deliverables by the DBERT Engineering Evaluation Committee, your submission was reviewed and flagged with the following discrepancy items:

FLAGGED DISCREPANCIES:
--------------------------------------------------------------------------------
{plain_issues_text}

MENTOR REVIEW NOTES:
--------------------------------------------------------------------------------
"{feedback_note}"
--------------------------------------------------------------------------------

WHY HAS YOUR STIPEND RELEASE NOT BEEN PROCESSED YET?
Under DBERT academic and financial guidelines, the ₹5,000 milestone stipend is sponsored strictly for verified open-source contributions directly committed to authorized partner repositories under the 4 recognized organizations, alongside verified public professional experience on LinkedIn. 

HOW TO RECTIFY & EXPEDITE YOUR STIPEND RELEASE:
We have updated your submission status to "Revision Requested" and reopened your milestone submission form on the DBERT LMS:
1. Ensure your contribution is merged or active in an authorized organization repository:
   - https://github.com/Alkameinc
   - https://github.com/Gayatri-Education
   - https://github.com/Aivaratechinfomatics
   - https://github.com/DBERT-INDIA
2. Update your LinkedIn profile: Add your DBERT internship under Experience ('Digital Blinc Education Research and Technology') and link your credential.
3. Visit https://lms.dbert.in/stipend/tasks and submit your updated GitHub repository URL and demo link.

Once resubmitted, your deliverables will be prioritized for expedited review and stipend scheduling.

If you have questions regarding repo access or contribution guidelines, connect directly with Admissions Concierge on WhatsApp:
https://wa.me/918192911360?text={quote(f'Hi Team, regarding my stipend submission #{sub_id} revision request for {domain}.')}

Warm regards,

{sender['name']}
{sender['title']}
DBERT Academic & Technical Fellowship Board
Digital Blinc Education Research and Technology
Official Portal: https://dbert.in | LMS: https://lms.dbert.in
"""

    # HTML Issues block
    html_issues_list = []
    if "INVALID_GITHUB_ORG" in issues:
        html_issues_list.append("""
        <div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #EF4444; padding: 14px 18px; border-radius: 0 8px 8px 0; margin-bottom: 12px;">
          <div style="font-weight: 800; color: #FCA5A5; font-size: 13px; text-transform: uppercase; margin-bottom: 4px;">
            ⚠️ Unauthorized GitHub Repository
          </div>
          <div style="font-size: 13px; color: #E2E8F0; line-height: 1.5;">
            Submitted repository: <code style="color:#FCA5A5; font-size: 12px; word-break: break-all;">""" + repo_url + """</code><br>
            Under DBERT policy, stipends are strictly funded for verified contributions to official partner repositories under one of our 4 authorized organizations:
            <div style="margin-top: 8px; font-weight: 600;">
              &bull; <a href="https://github.com/Alkameinc" target="_blank" style="color:#38BDF8; text-decoration: none;">Alkameinc</a> &bull;
              <a href="https://github.com/Gayatri-Education" target="_blank" style="color:#38BDF8; text-decoration: none;">Gayatri-Education</a> &bull;
              <a href="https://github.com/Aivaratechinfomatics" target="_blank" style="color:#38BDF8; text-decoration: none;">Aivaratechinfomatics</a> &bull;
              <a href="https://github.com/DBERT-INDIA" target="_blank" style="color:#38BDF8; text-decoration: none;">DBERT-INDIA</a>
            </div>
            <span style="font-size: 12px; color: #94A3B8;">Contributions to personal forks or unapproved repositories cannot be verified for stipend disbursement.</span>
          </div>
        </div>
        """)
    if "UNVERIFIED_LINKEDIN" in issues:
        html_issues_list.append("""
        <div style="background: rgba(245, 158, 11, 0.08); border-left: 4px solid #F59E0B; padding: 14px 18px; border-radius: 0 8px 8px 0; margin-bottom: 12px;">
          <div style="font-weight: 800; color: #FDE68A; font-size: 13px; text-transform: uppercase; margin-bottom: 4px;">
            ⚠️ LinkedIn Experience Unverified
          </div>
          <div style="font-size: 13px; color: #E2E8F0; line-height: 1.5;">
            Submitted Profile: <span style="color:#FCD34D;">""" + (linkedin_url or "Not Linked") + """</span><br>
            Your public LinkedIn profile does not reflect DBERT under your Experience or Licenses &amp; Certifications. Please add your DBERT Internship role and verify.
          </div>
        </div>
        """)

    html_issues_rendered = "".join(html_issues_list)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ margin: 0; padding: 0; background-color: #07090E; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #E2E8F0; }}
.wrapper {{ max-width: 620px; margin: 0 auto; background-color: #0E131F; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden; }}
.header {{ background: linear-gradient(135deg, #7C2D12 0%, #991B1B 100%); padding: 34px 30px; border-bottom: 2px solid #EF4444; text-align: left; }}
.badge {{ display: inline-block; background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.4); padding: 5px 14px; border-radius: 9999px; font-size: 11px; font-weight: 700; color: #FCA5A5; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 12px; }}
.header h1 {{ margin: 0 0 6px; font-size: 21px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; }}
.header p {{ margin: 0; font-size: 13px; color: #FECACA; }}
.body {{ padding: 30px; }}
.grid {{ width: 100%; border-collapse: collapse; margin: 18px 0; }}
.grid td {{ padding: 9px 12px; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px; }}
.grid td.label {{ color: #94A3B8; font-weight: 600; width: 36%; }}
.grid td.val {{ color: #F8FAFC; font-weight: 700; text-align: right; }}
.notes-box {{ background: rgba(245, 158, 11, 0.05); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 10px; padding: 16px 20px; margin: 20px 0; }}
.step-card {{ background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07); border-radius: 8px; padding: 12px 16px; margin: 8px 0; font-size: 13px; line-height: 1.5; }}
.btn {{ display: inline-block; background: #F59E0B; color: #000000 !important; text-decoration: none; padding: 14px 28px; border-radius: 8px; font-weight: 800; font-size: 14px; text-align: center; margin: 20px 0; }}
.footer {{ padding: 22px 30px; background: #07090E; border-top: 1px solid rgba(255,255,255,0.06); font-size: 12px; color: #64748B; line-height: 1.6; text-align: center; }}
</style>
</head>
<body>
<div style="padding: 24px 12px;">
  <div class="wrapper">
    <div class="header">
      <div class="badge">⚠️ Action Required &bull; Submission Revision</div>
      <h1>Stipend Deliverable Review Update</h1>
      <p>Official Feedback from DBERT Engineering Evaluation Committee</p>
    </div>
    <div class="body">
      <p style="font-size: 15px; line-height: 1.6; margin-top: 0;">Dear <strong>{name}</strong>,</p>
      <p style="font-size: 14px; line-height: 1.6; color: #CBD5E1;">
        Thank you for submitting your Capstone &amp; Stipend milestone deliverables for the <strong>{domain}</strong> track. During technical verification, our evaluation panel identified discrepancies requiring your immediate revision before stipend processing can proceed.
      </p>

      <table class="grid">
        <tr>
          <td class="label">Candidate Name</td>
          <td class="val">{name}</td>
        </tr>
        <tr>
          <td class="label">Domain Track</td>
          <td class="val">{domain}</td>
        </tr>
        <tr>
          <td class="label">Submission Ref</td>
          <td class="val"><code>#{sub_id}</code></td>
        </tr>
        <tr>
          <td class="label">Review Status</td>
          <td class="val" style="color:#FBBF24;">Action Required (Changes Requested)</td>
        </tr>
      </table>

      <div style="font-size: 12px; font-weight: 800; color: #EF4444; text-transform: uppercase; letter-spacing: 0.5px; margin: 20px 0 8px;">
        Flagged Review Items:
      </div>

      {html_issues_rendered}

      <div class="notes-box">
        <div style="font-size: 11px; font-weight: 800; color: #F59E0B; text-transform: uppercase; margin-bottom: 6px;">
          Evaluation Committee Notes:
        </div>
        <div style="font-size: 13px; color: #FEF3C7; line-height: 1.5; font-style: italic;">
          "{feedback_note}"
        </div>
      </div>

      <div style="font-size: 12px; font-weight: 800; color: #38BDF8; text-transform: uppercase; letter-spacing: 0.5px; margin: 24px 0 10px;">
        3-Step Remediation to Unlock Payout:
      </div>

      <div class="step-card">
        <strong style="color:#F8FAFC;">1. Contribute to Approved Organization Repo:</strong><br>
        Ensure your technical contribution is submitted to an official repository under <a href="https://github.com/Alkameinc" style="color:#38BDF8;">Alkameinc</a>, <a href="https://github.com/Gayatri-Education" style="color:#38BDF8;">Gayatri-Education</a>, <a href="https://github.com/Aivaratechinfomatics" style="color:#38BDF8;">Aivaratechinfomatics</a>, or <a href="https://github.com/DBERT-INDIA" style="color:#38BDF8;">DBERT-INDIA</a>.
      </div>
      <div class="step-card">
        <strong style="color:#F8FAFC;">2. Feature DBERT on LinkedIn:</strong><br>
        Add your DBERT Internship role under Experience and attach your credential to your public LinkedIn profile.
      </div>
      <div class="step-card">
        <strong style="color:#F8FAFC;">3. Resubmit on LMS:</strong><br>
        We have unlocked the submission portal on your LMS dashboard. Submit your updated repository and demo links.
      </div>

      <div style="text-align: center;">
        <a href="https://lms.dbert.in/stipend/tasks" class="btn">Update &amp; Resubmit on LMS &rarr;</a>
      </div>

      <p style="font-size: 13px; color: #94A3B8; line-height: 1.6; text-align: center; margin-top: 14px;">
        Need guidance with GitHub repo assignments? Connect with our Admissions Concierge on WhatsApp at <a href="https://wa.me/918192911360" style="color: #38BDF8; text-decoration: none;">+91 81929 11360</a>.
      </p>
    </div>
    <div class="footer">
      <strong>DBERT (Digital Blinc Education Research and Technology)</strong><br>
      Admissions &amp; Engineering Evaluation Desk &bull; WhatsApp Support: +91 81929 11360<br>
      Official Sovereign Domain: <a href="https://dbert.in" style="color: #38BDF8; text-decoration: none;">https://dbert.in</a> &bull; LMS: <a href="https://lms.dbert.in" style="color: #38BDF8; text-decoration: none;">https://lms.dbert.in</a>
    </div>
  </div>
</div>
</body>
</html>"""

    return subject, plain, html


# ==============================================================================
# TEMPLATE 2: CERTIFICATE & STIPEND ROADMAP (BATCH 1: 250 CANDIDATES)
# ==============================================================================

def build_roadmap_email(c: dict, sender: dict) -> tuple:
    name = c.get("name", "Fellow")
    email = c.get("email")
    domain = c.get("domain", "Applied Engineering")
    cert_id = c.get("cert_id") or ""
    completed_count = c.get("completed_count", 0)
    missing_count = c.get("missing_count", 4)
    pct = c.get("progress_pct", 0)
    missing_gates = c.get("missing_gates", [])

    subject = f"[ROADMAP] Steps to Receive Your DBERT Certificate of Completion & ₹5,000 Stipend"

    # Build missing gate bullet points for plain text
    plain_checklist = []
    for g in missing_gates:
        g_name = g.get("gate_name")
        g_cta = g.get("cta")
        if "Certificate" in g_name or "Verification Form" in g_name:
            plain_checklist.append(f"- [PENDING] Course Certificate & Verification Form: Complete your LMS quizzes and submit the ₹299 verification form at {FORM_URL}")
        elif "Duration" in g_name:
            plain_checklist.append(f"- [PENDING] Internship Duration: Complete your 60-day active sprint on the LMS at {g_cta}")
        elif "UPI" in g_name:
            plain_checklist.append(f"- [PENDING] Payout UPI ID Setup: Link your verified, Fernet-encrypted UPI ID for direct payout transfer at {g_cta}")
        elif "LinkedIn" in g_name:
            plain_checklist.append(f"- [PENDING] Public LinkedIn Experience: Add DBERT under Experience and Licenses on LinkedIn and verify on LMS at {g_cta}")
        else:
            plain_checklist.append(f"- [PENDING] {g_name}: Complete on LMS at {g_cta}")

    plain_checklist_str = "\n".join(plain_checklist)

    plain = f"""Dear {name},

We are reaching out with an official roadmap update on your DBERT Technical Internship in {domain}. You have currently completed {completed_count} of 4 prerequisite gates ({pct}% complete).

Below is the definitive guide on how to receive your official Certificate of Completion and unlock your ₹5,000 Milestone Stipend.

================================================================================
PART 1: HOW TO RECEIVE YOUR CERTIFICATE OF COMPLETION
================================================================================
1. Complete Course Tasks & Quizzes:
   Complete your modular quizzes and project tasks on the DBERT LMS (https://lms.dbert.in).
2. Submit ₹299 Document Verification Form:
   If you have not already submitted your verification request, fill out the official form here:
   {FORM_URL}
   (Includes ₹299 verification fee covering cryptographic registry registration, Turnitin evaluation rubric, and formal Letter of Recommendation).
3. Public Dossier Activation:
   Once processed, your 3-document credential packet (Certificate, Academic Evaluation, LOR) is permanently published and cryptographically verifiable at https://dbert.in/verify.

================================================================================
PART 2: HOW TO UNLOCK YOUR ₹5,000 MILESTONE STIPEND
================================================================================
The ₹5,000 stipend is granted upon satisfaction of the 4 pre-flight gates:
1. Verified Course Certificate on file.
2. 60-day internship duration milestone met.
3. Registered UPI ID on profile (Fernet-encrypted).
4. Public DBERT experience featured on LinkedIn.

CRITICAL OPEN-SOURCE GITHUB REQUIREMENT:
Under DBERT engineering policy, all capstone deliverable repositories MUST be contributed directly to official repositories under one of our 4 approved GitHub organizations:
- Alkameinc (https://github.com/Alkameinc)
- Gayatri-Education (https://github.com/Gayatri-Education)
- Aivaratechinfomatics (https://github.com/Aivaratechinfomatics)
- DBERT-INDIA (https://github.com/DBERT-INDIA)

Note: Contributions to personal forks or outside organizations will not be accepted for stipend disbursement.

================================================================================
YOUR REMAINING ACTION ITEMS ({missing_count} Pending):
================================================================================
{plain_checklist_str}

Direct Stipend & Milestone Dashboard:
https://lms.dbert.in/stipend/tasks

For queries, contact Admissions Concierge on WhatsApp:
https://wa.me/918192911360?text={quote(f'Hi Team, I have a question regarding my certificate and stipend roadmap for {domain}.')}

Warm regards,

{sender['name']}
{sender['title']}
DBERT Academic & Technical Fellowship Board
Digital Blinc Education Research and Technology
Portal: https://dbert.in | LMS: https://lms.dbert.in
"""

    # Build HTML checklist
    html_items = []
    for g in missing_gates:
        g_name = g.get("gate_name")
        g_cta = g.get("cta")
        if "Certificate" in g_name or "Verification Form" in g_name:
            html_items.append(f"""
            <div style="background: rgba(239, 68, 68, 0.08); border-left: 3px solid #EF4444; padding: 12px 14px; border-radius: 0 8px 8px 0; margin-bottom: 8px;">
              <div style="font-weight: 700; color: #FCA5A5; font-size: 13px;">⚠️ Gate 1: Course Certificate &amp; Verification Form</div>
              <div style="font-size: 12px; color: #CBD5E1; margin-top: 4px; line-height: 1.4;">
                Complete LMS quizzes and submit the ₹299 verification form to receive your official credentials:
                <a href="{FORM_URL}" target="_blank" style="color: #38BDF8; font-weight: 600; text-decoration: underline;">Complete Verification Form &rarr;</a>
              </div>
            </div>
            """)
        elif "Duration" in g_name:
            html_items.append(f"""
            <div style="background: rgba(245, 158, 11, 0.08); border-left: 3px solid #F59E0B; padding: 12px 14px; border-radius: 0 8px 8px 0; margin-bottom: 8px;">
              <div style="font-weight: 700; color: #FDE68A; font-size: 13px;">⏳ Gate 2: Internship Duration &amp; Active Sprint</div>
              <div style="font-size: 12px; color: #CBD5E1; margin-top: 4px; line-height: 1.4;">
                Requires completion of 60 days of active sprints. Track your live timeline at:
                <a href="{g_cta}" style="color: #38BDF8; font-weight: 600; text-decoration: underline;">View Sprint Progress &rarr;</a>
              </div>
            </div>
            """)
        elif "UPI" in g_name:
            html_items.append(f"""
            <div style="background: rgba(59, 130, 246, 0.08); border-left: 3px solid #3B82F6; padding: 12px 14px; border-radius: 0 8px 8px 0; margin-bottom: 8px;">
              <div style="font-weight: 700; color: #93C5FD; font-size: 13px;">💳 Gate 3: Payout UPI ID Setup</div>
              <div style="font-size: 12px; color: #CBD5E1; margin-top: 4px; line-height: 1.4;">
                Link your verified, Fernet-encrypted UPI ID for direct payout transfer:
                <a href="{g_cta}" style="color: #38BDF8; font-weight: 600; text-decoration: underline;">Configure Payout UPI ID &rarr;</a>
              </div>
            </div>
            """)
        elif "LinkedIn" in g_name:
            html_items.append(f"""
            <div style="background: rgba(168, 85, 247, 0.08); border-left: 3px solid #A855F7; padding: 12px 14px; border-radius: 0 8px 8px 0; margin-bottom: 8px;">
              <div style="font-weight: 700; color: #D8B4FE; font-size: 13px;">🔗 Gate 4: Public LinkedIn Experience</div>
              <div style="font-size: 12px; color: #CBD5E1; margin-top: 4px; line-height: 1.4;">
                Add DBERT under Experience and Licenses on LinkedIn and link your profile at:
                <a href="{g_cta}" style="color: #38BDF8; font-weight: 600; text-decoration: underline;">Verify LinkedIn on LMS &rarr;</a>
              </div>
            </div>
            """)
        else:
            html_items.append(f"""
            <div style="background: rgba(255, 255, 255, 0.04); border-left: 3px solid #64748B; padding: 12px 14px; border-radius: 0 8px 8px 0; margin-bottom: 8px;">
              <div style="font-weight: 700; color: #E2E8F0; font-size: 13px;">Pending: {g_name}</div>
              <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">
                <a href="{g_cta}" style="color: #38BDF8; text-decoration: underline;">Open Milestone Dashboard &rarr;</a>
              </div>
            </div>
            """)

    html_items_str = "".join(html_items)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ margin: 0; padding: 0; background-color: #07090E; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #E2E8F0; }}
.wrapper {{ max-width: 620px; margin: 0 auto; background-color: #0E131F; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden; }}
.header {{ background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%); padding: 34px 30px; border-bottom: 2px solid #6366F1; text-align: left; }}
.badge {{ display: inline-block; background: rgba(99, 102, 241, 0.2); border: 1px solid rgba(99, 102, 241, 0.4); padding: 5px 14px; border-radius: 9999px; font-size: 11px; font-weight: 700; color: #A5B4FC; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 12px; }}
.header h1 {{ margin: 0 0 6px; font-size: 21px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; }}
.header p {{ margin: 0; font-size: 13px; color: #C7D2FE; }}
.body {{ padding: 30px; }}
.progress-card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px 20px; margin: 20px 0; }}
.progress-bar-bg {{ background: rgba(255,255,255,0.08); border-radius: 9999px; height: 10px; width: 100%; overflow: hidden; margin-top: 10px; }}
.progress-bar-fill {{ background: linear-gradient(90deg, #6366F1, #10B981); height: 100%; border-radius: 9999px; width: {pct}%; }}
.section-card {{ background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 18px 20px; margin: 18px 0; }}
.section-title {{ font-size: 14px; font-weight: 800; color: #F8FAFC; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }}
.btn {{ display: inline-block; background: #6366F1; color: #FFFFFF !important; text-decoration: none; padding: 14px 28px; border-radius: 8px; font-weight: 700; font-size: 14px; text-align: center; margin: 20px 0; }}
.footer {{ padding: 22px 30px; background: #07090E; border-top: 1px solid rgba(255,255,255,0.06); font-size: 12px; color: #64748B; line-height: 1.6; text-align: center; }}
</style>
</head>
<body>
<div style="padding: 24px 12px;">
  <div class="wrapper">
    <div class="header">
      <div class="badge">🎓 Fellowship Roadmap &bull; Certificate &amp; Stipend</div>
      <h1>Official Completion &amp; Stipend Guide</h1>
      <p>Clear roadmap for {domain} fellows at DBERT</p>
    </div>
    <div class="body">
      <p style="font-size: 15px; line-height: 1.6; margin-top: 0;">Dear <strong>{name}</strong>,</p>
      <p style="font-size: 14px; line-height: 1.6; color: #CBD5E1;">
        Thank you for your active participation in the <strong>{domain}</strong> track. You have successfully cleared <strong>{completed_count} of 4</strong> prerequisite milestones.
      </p>

      <div class="progress-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 12px; font-weight: 800; color: #A5B4FC; text-transform: uppercase;">Milestone Progress</span>
          <span style="font-size: 13px; font-weight: 800; color: #10B981;">{completed_count}/4 Gates ({pct}%)</span>
        </div>
        <div class="progress-bar-bg">
          <div class="progress-bar-fill"></div>
        </div>
      </div>

      <!-- Part 1: Certificate -->
      <div class="section-card" style="border-left: 4px solid #38BDF8;">
        <div class="section-title" style="color: #38BDF8;">
          📜 Part 1: How to Receive Your Verified Certificate
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
          <strong>1. Complete Course Tasks:</strong> Finalize your quizzes and project submissions on the LMS.<br>
          <strong>2. Submit ₹299 Verification Form:</strong> If not completed, submit the document verification form to register your permanent cryptographic credential:
          <div style="margin: 8px 0;">
            <a href="{FORM_URL}" target="_blank" style="color: #38BDF8; font-weight: 700; text-decoration: underline;">
              &rarr; Submit ₹299 Certificate Verification Form
            </a>
          </div>
          <strong>3. Published Credential:</strong> Your 3-document packet (Certificate, Academic Evaluation, LOR) is made publicly verifiable on <code style="color:#38BDF8;">dbert.in/verify</code>.
        </div>
      </div>

      <!-- Part 2: Stipend -->
      <div class="section-card" style="border-left: 4px solid #10B981;">
        <div class="section-title" style="color: #10B981;">
          💰 Part 2: How to Unlock Your ₹5,000 Stipend
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
          Your ₹5,000 stipend is scheduled upon clearing the 4 pre-flight gates and submitting your capstone deliverable.<br><br>
          <div style="background: rgba(16, 185, 129, 0.08); padding: 12px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.2);">
            <strong style="color:#34D399;">CRITICAL OPEN-SOURCE GITHUB REQUIREMENT:</strong><br>
            All stipend deliverables <strong>MUST</strong> be submitted to official repositories under our 4 authorized partner organizations:
            <div style="margin-top: 6px; font-weight: 600;">
              &bull; <a href="https://github.com/Alkameinc" target="_blank" style="color:#38BDF8;">Alkameinc</a> &bull;
              <a href="https://github.com/Gayatri-Education" target="_blank" style="color:#38BDF8;">Gayatri-Education</a> &bull;
              <a href="https://github.com/Aivaratechinfomatics" target="_blank" style="color:#38BDF8;">Aivaratechinfomatics</a> &bull;
              <a href="https://github.com/DBERT-INDIA" target="_blank" style="color:#38BDF8;">DBERT-INDIA</a>
            </div>
            <span style="font-size: 11px; color:#94A3B8;">Contributions to personal forks or outside organizations cannot be verified for stipend release.</span>
          </div>
        </div>
      </div>

      <!-- Personalized Missing Gates -->
      <div style="font-size: 12px; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin: 24px 0 10px;">
        Your Remaining Action Items ({missing_count} Remaining):
      </div>

      {html_items_str}

      <div style="text-align: center;">
        <a href="https://lms.dbert.in/stipend/tasks" class="btn">Open Stipend &amp; Milestone Dashboard &rarr;</a>
      </div>

      <p style="font-size: 13px; color: #94A3B8; line-height: 1.6; text-align: center; margin-top: 14px;">
        Need assistance with any step? Contact Admissions Concierge on WhatsApp at <a href="https://wa.me/918192911360" style="color: #38BDF8; text-decoration: none;">+91 81929 11360</a>.
      </p>
    </div>
    <div class="footer">
      <strong>DBERT (Digital Blinc Education Research and Technology)</strong><br>
      Academic &amp; Incubation Desk &bull; WhatsApp Support: +91 81929 11360<br>
      Official Sovereign Domain: <a href="https://dbert.in" style="color: #38BDF8; text-decoration: none;">https://dbert.in</a> &bull; LMS: <a href="https://lms.dbert.in" style="color: #38BDF8; text-decoration: none;">https://lms.dbert.in</a>
    </div>
  </div>
</div>
</body>
</html>"""

    return subject, plain, html


# ==============================================================================
# TELEMETRY DISPATCHER
# ==============================================================================

def send_completion_telemetry(batch_type: str, sent_count: int, failed_count: int, skipped_count: int, total_count: int, elapsed_sec: float, tracking: dict):
    subject = f"[TELEMETRY] DBERT {batch_type.upper()} Dispatch Completed: {sent_count}/{total_count} Delivered ({len(SMTP_ACCOUNTS)} SMTP Accounts)"
    
    elapsed_min = round(elapsed_sec / 60, 1)
    
    discrepancy_count = sum(1 for v in tracking.values() if v.get("status") == "SENT" and v.get("type") == "DISCREPANCY")
    roadmap_count = sum(1 for v in tracking.values() if v.get("status") == "SENT" and v.get("type") == "ROADMAP")

    body = f"""DBERT OPERATIONAL DISPATCH TELEMETRY REPORT
================================================================================
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Dispatch Batch: {batch_type.upper()}
Total Targets in Queue: {total_count}
Successfully Delivered: {sent_count}
Skipped (Already Sent): {skipped_count}
Failed: {failed_count}
Elapsed Time: {elapsed_min} minutes
SMTP Node Pool: 5 Google Workspace relay accounts rotated

DELIVERY BREAKDOWN:
- Discrepancy Notices (Flagged GitHub / LinkedIn Submissions): {discrepancy_count}
- Engaged Interns Roadmap (Batch 1 Priority 1-3): {roadmap_count}

Approved GitHub Organizations Enforced:
1. https://github.com/Alkameinc
2. https://github.com/Gayatri-Education
3. https://github.com/Aivaratechinfomatics
4. https://github.com/DBERT-INDIA

Live Tracking File: data/discrepancy_roadmap_tracking.json
Audit Log: data/discrepancy_roadmap_dispatch.log
================================================================================
"""
    log("Sending completion telemetry...")
    sender = SMTP_ACCOUNTS[0]
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=20) as s:
            s.login(sender["user"], sender["pass"])
            for rcpt in TELEMETRY_EMAILS:
                msg = MIMEMultipart("plain")
                msg["Subject"] = subject
                msg["From"] = f"{sender['name']} <{sender['user']}>"
                msg["To"] = rcpt
                msg["Date"] = formatdate(localtime=True)
                msg.attach(MIMEText(body, "plain", "utf-8"))
                s.sendmail(sender["user"], [rcpt], msg.as_string())
                log(f"   -> Telemetry sent to {rcpt}")
    except Exception as e:
        log(f"   -> Failed to send telemetry: {e}")


# ==============================================================================
# MAIN DISPATCH PIPELINE
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Dispatch discrepancy notices and engaged interns roadmap.")
    parser.add_argument("--live", action="store_true", help="Execute live SMTP delivery (default: dry-run)")
    parser.add_argument("--batch", choices=["discrepancy", "batch1", "batch2", "batch3", "batch4", "all_engaged", "all"], default="all", help="Target batch (default: all = discrepancy + batch1)")
    parser.add_argument("--delay", type=float, default=10.0, help="Delay in seconds between sends (default: 10s)")
    args = parser.parse_args()

    tracking = load_tracking()

    print("=" * 80)
    print("DBERT MULTI-SMTP DISCREPANCY & ROADMAP DISPATCH ENGINE")
    print(f"Mode: {'LIVE DISPATCH' if args.live else 'DRY RUN (Preview Only)'} | Batch Target: {args.batch.upper()}")
    print("=" * 80)

    queue = []

    # 1. Load Discrepancy Cohort (10 candidates)
    if args.batch in ["discrepancy", "all"]:
        disc_file = DATA_DIR / "cohort_discrepancy_10.json"
        if disc_file.exists():
            disc_data = json.load(open(disc_file, encoding="utf-8"))
            for item in disc_data:
                queue.append(("DISCREPANCY", item))

    # 2. Load Engaged Interns Batches
    if args.batch in ["batch1", "all"]:
        b1_file = DATA_DIR / "engaged_interns_batch1.json"
        if b1_file.exists():
            b1_data = json.load(open(b1_file, encoding="utf-8"))
            for item in b1_data:
                queue.append(("ROADMAP", item))

    if args.batch in ["batch2", "all_engaged"]:
        b2_file = DATA_DIR / "engaged_interns_batch2.json"
        if b2_file.exists():
            b2_data = json.load(open(b2_file, encoding="utf-8"))
            for item in b2_data:
                queue.append(("ROADMAP", item))

    if args.batch in ["batch3", "all_engaged"]:
        b3_file = DATA_DIR / "engaged_interns_batch3.json"
        if b3_file.exists():
            b3_data = json.load(open(b3_file, encoding="utf-8"))
            for item in b3_data:
                queue.append(("ROADMAP", item))

    if args.batch in ["batch4", "all_engaged"]:
        b4_file = DATA_DIR / "engaged_interns_batch4.json"
        if b4_file.exists():
            b4_data = json.load(open(b4_file, encoding="utf-8"))
            for item in b4_data:
                queue.append(("ROADMAP", item))

    log(f"Queue loaded: {len(queue)} total recipients for batch '{args.batch}'.")
    disc_count = sum(1 for t, _ in queue if t == "DISCREPANCY")
    road_count = sum(1 for t, _ in queue if t == "ROADMAP")
    print(f"Breakdown -> Discrepancy Notices: {disc_count}, Engaged Roadmap: {road_count}")

    smtp_index = 0
    sent_count = 0
    skipped_count = 0
    failed_count = 0
    start_time = time.time()

    # Reconnectable SMTP session cache
    active_server = None
    current_smtp_user = None

    try:
        for idx, (target_type, cand) in enumerate(queue, 1):
            email = cand["email"].strip().lower()
            key = f"{target_type}_{email}"

            if tracking.get(key, {}).get("status") == "SENT":
                skipped_count += 1
                continue

            # Pick next SMTP account
            active_account = SMTP_ACCOUNTS[smtp_index % len(SMTP_ACCOUNTS)]
            smtp_index += 1

            if target_type == "DISCREPANCY":
                subject, plain, html = build_discrepancy_email(cand, active_account)
            else:
                subject, plain, html = build_roadmap_email(cand, active_account)

            if not args.live:
                log(f"[DRY-RUN] #{idx}/{len(queue)} [{target_type}] -> {email} ({cand.get('name')}) via {active_account['user']}: {subject[:55]}...")
                sent_count += 1
                continue

            # Live Send with account reconnection management
            try:
                if active_server is None or current_smtp_user != active_account["user"]:
                    if active_server:
                        try: active_server.quit()
                        except Exception: pass
                    active_server = get_smtp_connection(active_account)
                    current_smtp_user = active_account["user"]

                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = f"{active_account['name']} <{active_account['user']}>"
                msg["To"] = email
                msg["Date"] = formatdate(localtime=True)
                msg["Message-ID"] = make_msgid(domain="dbert.in")
                msg["Reply-To"] = active_account["user"]
                msg["X-Entity-Ref-ID"] = key

                msg.attach(MIMEText(plain, "plain", "utf-8"))
                msg.attach(MIMEText(html, "html", "utf-8"))

                active_server.sendmail(active_account["user"], [email], msg.as_string())
                log(f"[LIVE-SENT] #{idx}/{len(queue)} [{target_type}] -> {email} via {active_account['user']}")

                tracking[key] = {
                    "type": target_type,
                    "email": email,
                    "name": cand.get("name"),
                    "status": "SENT",
                    "sender": active_account["user"],
                    "sent_at": datetime.now().isoformat(),
                    "subject": subject
                }
                save_tracking(tracking)
                sent_count += 1

                time.sleep(args.delay)

            except Exception as e:
                log(f"[ERROR] #{idx} [{target_type}] -> {email} failed via {active_account['user']}: {e}")
                failed_count += 1
                if active_server:
                    try: active_server.quit()
                    except Exception: pass
                active_server = None
                current_smtp_user = None
                time.sleep(5)

    finally:
        if active_server:
            try: active_server.quit()
            except Exception: pass

    log(f"Pipeline completed: Sent: {sent_count}, Skipped (Already Sent): {skipped_count}, Failed: {failed_count}")
    if args.live:
        elapsed_sec = time.time() - start_time
        send_completion_telemetry(args.batch, sent_count, failed_count, skipped_count, len(queue), elapsed_sec, tracking)

if __name__ == "__main__":
    main()
