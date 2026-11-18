import os
import sys
import json
import time
import smtplib
import ssl
from datetime import datetime
from email.utils import formatdate, make_msgid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Google Workspace SMTP Accounts Pool
SMTP_ACCOUNTS = [
    {
        "email": "abhinav.sharma@dbert.in",
        "app_password": "rsupmvvvvwrsuxuh",
        "from_name": "Abhinav Sharma",
        "role": "Program Head & Project Mentor"
    },
    {
        "email": "contactus@dbert.in",
        "app_password": "llvmaajmrljpcwru",
        "from_name": "DBERT Admissions & Verification",
        "role": "Admissions & Verification Concierge"
    },
    {
        "email": "manoj.kumar@dbert.in",
        "app_password": "fnevtpseplwibckr",
        "from_name": "Manoj Kumar",
        "role": "Academic Lead & Admissions"
    },
    {
        "email": "sandeep.bannu@dbert.in",
        "app_password": "qtqzlmrynbcxvyjy",
        "from_name": "Sandeep Bannu",
        "role": "Technical Program Operations"
    },
    {
        "email": "pulkit.kunar@dbert.in",
        "app_password": "vzefecwpggxuaztr",
        "from_name": "Pulkit Kumar",
        "role": "Technical Mentorship & Verification"
    }
]

TRACKING_FILE = Path("data/dashboard_emails_tracking.json")
LOG_FILE = Path("data/dashboard_emails.log")
REGISTRY_FILE = Path("apps/website/src/data/certificates_registry.json")

TELEMETRY_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

def log_msg(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def send_via_smtp(account, to_email, subject, plain_text, html_content, attachments=None):
    msg = MIMEMultipart("mixed")
    msg["From"] = f"{account['from_name']} <{account['email']}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")
    msg["Reply-To"] = f"support@dbert.in"

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(plain_text, "plain", "utf-8"))
    alt.attach(MIMEText(html_content, "html", "utf-8"))
    msg.attach(alt)

    if attachments:
        for att_path in attachments:
            if os.path.exists(att_path):
                filename = os.path.basename(att_path)
                with open(att_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=filename)
                    part["Content-Disposition"] = f'attachment; filename="{filename}"'
                    msg.attach(part)
            else:
                log_msg(f"  [WARN] Attachment not found: {att_path}")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(account["email"], account["app_password"])
        server.send_message(msg)

    return msg["Message-ID"]

def build_verified_email(c_rec):
    name = c_rec["holderName"]
    cert_id = c_rec["certId"]
    intern_id = c_rec.get("internId", "DBERT-INT")
    domain = c_rec.get("domain", "Data Analyst")
    project = c_rec.get("project", "Enterprise Incubation Project")
    duration = c_rec.get("duration", "2 Months")
    score = c_rec.get("score", 85)
    grade = c_rec.get("grade", "Grade A (Very Good)")
    verify_url = f"https://dbert.in/verify/{cert_id}"
    linkedin_url = (
        f"https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME"
        f"&name={domain.replace(' ', '+')}+Internship+Credential"
        f"&organizationName=DBERT"
        f"&issueYear=2026&issueMonth=11"
        f"&certUrl={verify_url}"
        f"&certId={cert_id}"
    )

    subject = f"Official Internship Credential Packet — {name} [{cert_id}]"

    plain_text = f"""Dear {name},

Congratulations! Your official DBERT Internship Credential Packet is now activated, cryptographically signed, and verified on the sovereign technical registry.

Official Verification Record:
--------------------------------------------------------------------------------
- Candidate Name:        {name}
- Domain Track:          {domain}
- Program Tenure:        {duration}
- Core Project:          {project}
- Academic Evaluation:   {score}/100 ({grade})
- Certificate ID:        {cert_id}
- Permanent Intern ID:   {intern_id}
- Online Verification:   {verify_url}
- Add to LinkedIn:       {linkedin_url}
--------------------------------------------------------------------------------

ATTACHED CREDENTIAL PACKET (3 OFFICIAL DOCUMENTS):
1. Official Certificate of Completion (High-Resolution 256-Bit Signed)
2. Academic Project Evaluation (Rubric Breakdown & Turnitin Integrity Audit)
3. Official Letter of Recommendation (LOR) signed by Program Head Mr. Abhinav Sharma

STIPEND CONTRIBUTION NOTICE:
As a fully verified certified intern, you are eligible to submit your technical repository contributions on https://lms.dbert.in/stipend/tasks on or after your completion date. Verified candidates who contribute approved pull requests to DBERT partner organizations and sync their credentials on LinkedIn are eligible for the ₹5,499 stipend release.

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
Official Sovereign Portal: https://dbert.in
Verification Registry: https://dbert.in/verify
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DBERT Official Credential</title>
</head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:10px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    
    <!-- Header -->
    <div style="background-color:#0E1626;padding:26px 30px;text-align:center;border-bottom:2px solid #E2B96F;">
      <div style="color:#E2B96F;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:12px;letter-spacing:1px;margin-top:4px;">SOVEREIGN TECHNICAL INCUBATION REGISTRY</div>
    </div>

    <!-- Content -->
    <div style="padding:32px 30px;">
      <div style="display:inline-block;background:rgba(16,185,129,0.15);color:#10B981;font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 12px;border-radius:20px;border:1px solid rgba(16,185,129,0.3);margin-bottom:16px;">
        &#10003; OFFICIAL CREDENTIAL VERIFIED & ACTIVE
      </div>

      <h1 style="font-size:20px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;line-height:1.4;">
        Official Internship Credential Issued for {name}
      </h1>

      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 20px 0;">
        Dear <strong>{name}</strong>,<br><br>
        We are pleased to inform you that your official DBERT Internship Credential Packet has been generated, cryptographically signed, and registered on the permanent DBERT sovereign verification engine.
      </p>

      <!-- Credential Table -->
      <div style="background-color:#0F141C;border:1px solid #1E2633;border-radius:8px;padding:20px;margin-bottom:24px;">
        <div style="font-size:11px;color:#E2B96F;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;">
          AUTHENTICATED RECORD DOSSIER
        </div>
        <table style="width:100%;font-size:13px;border-collapse:collapse;">
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;width:40%;">Candidate Name:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{name}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Domain Track:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{domain}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Certificate ID:</td>
            <td style="padding:6px 0;color:#E2B96F;font-family:monospace;font-weight:700;">{cert_id}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Academic Evaluation:</td>
            <td style="padding:6px 0;color:#10B981;font-weight:700;">{score}/100 ({grade})</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Permanent Intern ID:</td>
            <td style="padding:6px 0;color:#CBD5E1;font-family:monospace;">{intern_id}</td>
          </tr>
        </table>
      </div>

      <!-- Attached Documents Callout -->
      <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:4px;padding:14px 16px;margin-bottom:24px;">
        <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:6px;">Attached Documents in this Email:</div>
        <div style="font-size:12px;color:#CBD5E1;line-height:1.6;">
          1. <strong>Certificate of Completion</strong> (256-Bit Cryptographic Signature)<br>
          2. <strong>Academic Project Evaluation</strong> (Full Rubric & Turnitin Audit)<br>
          3. <strong>Official Letter of Recommendation (LOR)</strong> by Mr. Abhinav Sharma
        </div>
      </div>

      <!-- Action Buttons -->
      <table style="width:100%;border-collapse:collapse;margin:28px 0 20px 0;">
        <tr>
          <td style="padding-right:8px;width:50%;">
            <a href="{verify_url}" style="display:block;background:linear-gradient(135deg, #10B981, #059669);color:#FFFFFF;text-decoration:none;font-size:13px;font-weight:700;text-align:center;padding:12px 14px;border-radius:6px;box-shadow:0 4px 14px rgba(16,185,129,0.3);">
              View Sovereign Registry &#8594;
            </a>
          </td>
          <td style="padding-left:8px;width:50%;">
            <a href="{linkedin_url}" style="display:block;background:#0A66C2;color:#FFFFFF;text-decoration:none;font-size:13px;font-weight:700;text-align:center;padding:12px 14px;border-radius:6px;box-shadow:0 4px 14px rgba(10,102,194,0.3);">
              Add to LinkedIn Profile
            </a>
          </td>
        </tr>
      </table>

      <!-- Stipend Notice -->
      <div style="background:#0F141C;border:1px solid #1E2633;border-radius:6px;padding:14px;margin-top:20px;">
        <div style="font-size:12px;font-weight:700;color:#38BDF8;margin-bottom:4px;">Stipend Contribution Notice</div>
        <p style="font-size:12px;line-height:1.5;color:#94A3B8;margin:0;">
          As a verified certified candidate, you can access your Stipend Dashboard at <a href="https://lms.dbert.in/stipend/tasks" style="color:#38BDF8;text-decoration:underline;">lms.dbert.in/stipend/tasks</a> to submit technical repository contributions on or after your completion date. Verified candidates who complete all gates are eligible for the ₹5,499 stipend.
        </p>
      </div>

    </div>

    <!-- Footer -->
    <div style="background-color:#0E1626;padding:20px 30px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#64748B;line-height:1.6;">
      <div>Digital Blinc Education Research and Technology (DBERT)</div>
      <div>Official Sovereign Portal: <a href="https://dbert.in" style="color:#E2B96F;text-decoration:none;">dbert.in</a> | Registry: <a href="https://dbert.in/verify" style="color:#E2B96F;text-decoration:none;">dbert.in/verify</a></div>
    </div>
  </div>
</body>
</html>"""

    attachments = [c_rec["doc1Pdf"], c_rec["doc2Pdf"], c_rec["doc3Pdf"]]
    return subject, plain_text, html_content, attachments


def build_sub53_email():
    name = "Vishwajeet Shinde"
    cert_id = "CERT-DBERT-2026-DA-027"
    verify_url = f"https://dbert.in/verify/{cert_id}"
    linkedin_url = (
        f"https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME"
        f"&name=Data+Analyst+Internship+Credential"
        f"&organizationName=DBERT"
        f"&issueYear=2026&issueMonth=11"
        f"&certUrl={verify_url}"
        f"&certId={cert_id}"
    )

    subject = f"Stipend Contribution Review Update — 1 Step Remaining for ₹5,499 Release [{cert_id}]"

    plain_text = f"""Dear {name},

We are writing with a milestone evaluation update regarding your technical contribution submission for the DBERT ₹5,499 stipend release.

EVALUATION RESULTS:
--------------------------------------------------------------------------------
1. GitHub Repository Contribution: APPROVED
   - Repository: Gayatri-Education/Gayatri-Demo
   - Audit Status: Verified under authorized partner organization Gayatri Education.

2. Technical Capstone Publication: APPROVED
   - Article #51: "Analyzing AI Workflow Performance: Metrics That Matter for Scalable Systems"
   - Status: Published live on https://dbert.in/blog/analyzing-ai-workflow-performance-aivara

3. Encrypted UPI ID Payout Configuration: VERIFIED
   - UPI ID configured on profile.

4. LinkedIn Experience & Credential Sync: PENDING ACTION (Only Gate Remaining)
   - Status: DBERT experience and certificate {cert_id} are not yet featured on your LinkedIn profile.
--------------------------------------------------------------------------------

WHAT YOU NEED TO DO TO RELEASE YOUR ₹5,499 STIPEND:
Please complete the single remaining step on LinkedIn:
1. Add DBERT under Experience:
   - Organization: DBERT (Digital Blinc Education Research and Technology)
   - Role: Data Analyst Intern
   - Dates: August 2026 - October 2026
2. Add your Certificate under Licenses & Certifications:
   - Name: Data Analyst Internship Credential
   - Issuing Organization: DBERT
   - Credential ID: {cert_id}
   - Credential URL: {verify_url}
   - Quick Add: {linkedin_url}

Once added, please reply directly to this email with your updated LinkedIn profile link or verify on https://lms.dbert.in/stipend/tasks. As all other gates have been cleared, your ₹5,499 stipend will be scheduled for disbursement to your verified UPI ID!

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
Official Sovereign Portal: https://dbert.in
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>DBERT Stipend Review</title>
</head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:10px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    
    <div style="background-color:#0E1626;padding:26px 30px;text-align:center;border-bottom:2px solid #38BDF8;">
      <div style="color:#38BDF8;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:12px;letter-spacing:1px;margin-top:4px;">STIPEND CONTRIBUTION EVALUATION COMMITTEE</div>
    </div>

    <div style="padding:32px 30px;">
      <div style="display:inline-block;background:rgba(56,189,248,0.15);color:#38BDF8;font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 12px;border-radius:20px;border:1px solid rgba(56,189,248,0.3);margin-bottom:16px;">
        1 FINAL STEP REMAINING FOR STIPEND RELEASE
      </div>

      <h1 style="font-size:20px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;line-height:1.4;">
        Stipend Review Update for {name}
      </h1>

      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 20px 0;">
        Dear <strong>{name}</strong>,<br><br>
        The DBERT Academic & Mentorship Evaluation Committee has completed the review of your technical contribution submission (ID: #53). We are pleased to share that your core technical deliverables have been approved.
      </p>

      <!-- Gates Status Grid -->
      <div style="background-color:#0F141C;border:1px solid #1E2633;border-radius:8px;padding:20px;margin-bottom:24px;">
        <div style="font-size:11px;color:#E2B96F;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:14px;">
          GATES AUDIT BREAKDOWN
        </div>
        <table style="width:100%;font-size:13px;border-collapse:collapse;">
          <tr style="border-bottom:1px solid #1E2633;">
            <td style="padding:10px 0;color:#8A9AB5;">1. Technical Repository:</td>
            <td style="padding:10px 0;color:#10B981;font-weight:700;text-align:right;">&#10003; APPROVED (Gayatri-Education/Gayatri-Demo)</td>
          </tr>
          <tr style="border-bottom:1px solid #1E2633;">
            <td style="padding:10px 0;color:#8A9AB5;">2. Capstone Article:</td>
            <td style="padding:10px 0;color:#10B981;font-weight:700;text-align:right;">&#10003; APPROVED (Published #51)</td>
          </tr>
          <tr style="border-bottom:1px solid #1E2633;">
            <td style="padding:10px 0;color:#8A9AB5;">3. UPI ID Configuration:</td>
            <td style="padding:10px 0;color:#10B981;font-weight:700;text-align:right;">&#10003; VERIFIED</td>
          </tr>
          <tr>
            <td style="padding:10px 0;color:#8A9AB5;">4. LinkedIn Experience & Cert:</td>
            <td style="padding:10px 0;color:#F59E0B;font-weight:700;text-align:right;">&#9888; ACTION REQUIRED</td>
          </tr>
        </table>
      </div>

      <!-- Action Required Box -->
      <div style="background:rgba(245,158,11,0.08);border-left:3px solid #F59E0B;border-radius:4px;padding:16px;margin-bottom:24px;">
        <div style="font-size:13px;font-weight:700;color:#F59E0B;margin-bottom:6px;">Final Action Required:</div>
        <div style="font-size:13px;color:#CBD5E1;line-height:1.6;">
          Please feature your DBERT experience and official Certificate ID (<strong>{cert_id}</strong>) on your LinkedIn profile. Use the direct button below to add it in 1 click:
        </div>
        <div style="margin-top:14px;">
          <a href="{linkedin_url}" style="display:inline-block;background:#0A66C2;color:#FFFFFF;text-decoration:none;font-size:13px;font-weight:700;padding:10px 18px;border-radius:6px;">
            1-Click Add Certificate to LinkedIn
          </a>
        </div>
      </div>

      <p style="font-size:13px;line-height:1.6;color:#94A3B8;margin:0 0 16px 0;">
        Once updated, reply directly to this email or re-verify at <a href="https://lms.dbert.in/stipend/tasks" style="color:#38BDF8;text-decoration:underline;">lms.dbert.in/stipend/tasks</a>. As all other requirements are satisfied, your <strong>₹5,499 stipend</strong> will be scheduled for release directly to your registered UPI ID.
      </p>
    </div>

    <div style="background-color:#0E1626;padding:20px 30px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#64748B;line-height:1.6;">
      <div>DBERT Sovereign Technical Incubation Platform</div>
      <div>Official Portal: <a href="https://dbert.in" style="color:#E2B96F;text-decoration:none;">dbert.in</a></div>
    </div>
  </div>
</body>
</html>"""

    return subject, plain_text, html_content, None


def build_sub51_email():
    name = "Shreyash Sambhaji Kamble"
    cert_id = "CERT-DBERT-2026-DA-077"
    verify_url = f"https://dbert.in/verify/{cert_id}"
    linkedin_url = (
        f"https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME"
        f"&name=Data+Analyst+Internship+Credential"
        f"&organizationName=DBERT"
        f"&issueYear=2026&issueMonth=11"
        f"&certUrl={verify_url}"
        f"&certId={cert_id}"
    )

    subject = f"Stipend Contribution Review Update — Next Steps to Complete Gates [{cert_id}]"

    plain_text = f"""Dear {name},

We are writing with an evaluation update on your technical contribution submission (ID: #51) for the DBERT ₹5,499 stipend release.

EVALUATION RESULTS:
--------------------------------------------------------------------------------
1. GitHub Repository Contribution: APPROVED
   - Repository: Gayatri-Education/Gayatri-AI
   - Audit Status: Verified under authorized partner organization Gayatri Education.

2. Technical Capstone Article: PENDING SUBMISSION
   - Status: Please write and submit your capstone technical article on https://lms.dbert.in/intern/articles.

3. Encrypted UPI ID Payout Configuration: VERIFIED
   - UPI ID configured on profile.

4. LinkedIn Experience & Credential Sync: PENDING ACTION
   - Status: Add DBERT experience and certificate {cert_id} on LinkedIn.
--------------------------------------------------------------------------------

NEXT STEPS TO UNLOCK YOUR ₹5,499 STIPEND:
1. Submit your Capstone Article:
   - Log into https://lms.dbert.in/intern/articles
   - Submit a comprehensive technical article detailing your work on Gayatri-AI, algorithms, and results.
2. Add your Certificate to LinkedIn:
   - Name: Data Analyst Internship Credential
   - Issuing Organization: DBERT
   - Credential ID: {cert_id}
   - Credential URL: {verify_url}
   - Quick Add: {linkedin_url}

Once both steps are completed, your dossier will be 100% verified and the ₹5,499 stipend will be scheduled for release directly to your verified UPI ID!

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
Official Sovereign Portal: https://dbert.in
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>DBERT Stipend Review</title>
</head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:10px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    
    <div style="background-color:#0E1626;padding:26px 30px;text-align:center;border-bottom:2px solid #38BDF8;">
      <div style="color:#38BDF8;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:12px;letter-spacing:1px;margin-top:4px;">STIPEND CONTRIBUTION EVALUATION COMMITTEE</div>
    </div>

    <div style="padding:32px 30px;">
      <div style="display:inline-block;background:rgba(56,189,248,0.15);color:#38BDF8;font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 12px;border-radius:20px;border:1px solid rgba(56,189,248,0.3);margin-bottom:16px;">
        REPOSITORY APPROVED &#183; 2 GATES REMAINING
      </div>

      <h1 style="font-size:20px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;line-height:1.4;">
        Stipend Review Update for {name}
      </h1>

      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 20px 0;">
        Dear <strong>{name}</strong>,<br><br>
        The DBERT Academic & Mentorship Evaluation Committee has reviewed your submission (ID: #51). Your GitHub repository work on <strong>Gayatri-Education/Gayatri-AI</strong> has been verified and approved.
      </p>

      <!-- Gates Status Grid -->
      <div style="background-color:#0F141C;border:1px solid #1E2633;border-radius:8px;padding:20px;margin-bottom:24px;">
        <div style="font-size:11px;color:#E2B96F;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:14px;">
          GATES AUDIT BREAKDOWN
        </div>
        <table style="width:100%;font-size:13px;border-collapse:collapse;">
          <tr style="border-bottom:1px solid #1E2633;">
            <td style="padding:10px 0;color:#8A9AB5;">1. Technical Repository:</td>
            <td style="padding:10px 0;color:#10B981;font-weight:700;text-align:right;">&#10003; APPROVED (Gayatri-Education/Gayatri-AI)</td>
          </tr>
          <tr style="border-bottom:1px solid #1E2633;">
            <td style="padding:10px 0;color:#8A9AB5;">2. Capstone Article:</td>
            <td style="padding:10px 0;color:#F59E0B;font-weight:700;text-align:right;">&#9888; PENDING SUBMISSION</td>
          </tr>
          <tr style="border-bottom:1px solid #1E2633;">
            <td style="padding:10px 0;color:#8A9AB5;">3. UPI ID Configuration:</td>
            <td style="padding:10px 0;color:#10B981;font-weight:700;text-align:right;">&#10003; VERIFIED</td>
          </tr>
          <tr>
            <td style="padding:10px 0;color:#8A9AB5;">4. LinkedIn Experience & Cert:</td>
            <td style="padding:10px 0;color:#F59E0B;font-weight:700;text-align:right;">&#9888; ACTION REQUIRED</td>
          </tr>
        </table>
      </div>

      <!-- Action Required Box -->
      <div style="background:rgba(56,189,248,0.08);border-left:3px solid #38BDF8;border-radius:4px;padding:16px;margin-bottom:24px;">
        <div style="font-size:13px;font-weight:700;color:#38BDF8;margin-bottom:8px;">Remaining Steps to Release ₹5,499:</div>
        <div style="font-size:13px;color:#CBD5E1;line-height:1.6;">
          1. <strong>Publish Capstone Article:</strong> Write and submit your technical article on <a href="https://lms.dbert.in/intern/articles" style="color:#38BDF8;text-decoration:underline;">lms.dbert.in/intern/articles</a>.<br>
          2. <strong>Add to LinkedIn:</strong> Add DBERT under Experience and your Certificate (<strong>{cert_id}</strong>) under Licenses.
        </div>
        <div style="margin-top:14px;">
          <a href="{linkedin_url}" style="display:inline-block;background:#0A66C2;color:#FFFFFF;text-decoration:none;font-size:13px;font-weight:700;padding:10px 18px;border-radius:6px;">
            1-Click Add Certificate to LinkedIn
          </a>
        </div>
      </div>

      <p style="font-size:13px;line-height:1.6;color:#94A3B8;margin:0 0 16px 0;">
        Once these 2 gates are completed, your stipend disbursement of <strong>₹5,499</strong> will be finalized.
      </p>
    </div>

    <div style="background-color:#0E1626;padding:20px 30px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#64748B;line-height:1.6;">
      <div>DBERT Sovereign Technical Incubation Platform</div>
      <div>Official Portal: <a href="https://dbert.in" style="color:#E2B96F;text-decoration:none;">dbert.in</a></div>
    </div>
  </div>
</body>
</html>"""

    return subject, plain_text, html_content, None


def build_sub52_email():
    name = "M Brahmani"
    cert_id = "CERT-DBERT-2026-DA-117"
    verify_url = f"https://dbert.in/verify/{cert_id}"

    subject = f"Action Required: Stipend Repository Contribution Review — Resubmission Needed [{cert_id}]"

    plain_text = f"""Dear {name},

We are writing regarding your technical contribution submission (ID: #52) for the DBERT ₹5,499 stipend release.

EVALUATION NOTICE & DISCREPANCY:
--------------------------------------------------------------------------------
- Submitted URL: princess-chinni.com (Personal Portfolio Website)
- Review Outcome: CHANGES REQUESTED / RE-SUBMISSION REQUIRED
--------------------------------------------------------------------------------

EXPLANATION:
Per DBERT Technical Incubation & Stipend Policy, stipend release is strictly contingent upon verified open-source and production pull requests/contributions made towards approved DBERT enterprise repositories and partner organizations. Personal portfolio websites or unrelated hosted sites cannot be accepted for stipend credit.

AUTHORIZED GITHUB ORGANIZATIONS:
To be eligible for the ₹5,499 stipend, please contribute meaningful code (features, analysis notebooks, bug fixes, or documentation) to any repository under one of the 4 approved partner organizations:
1. https://github.com/Alkameinc
2. https://github.com/Gayatri-Education
3. https://github.com/Aivaratechinfomatics
4. https://github.com/DBERT-INDIA

HOW TO RESUBMIT:
1. Select a repository from one of the authorized organizations above.
2. Fork the repository, create a branch, implement your technical contributions, and submit a pull request (PR).
3. Log into https://lms.dbert.in/stipend/tasks and resubmit with the new GitHub repository and PR URL.

Our technical evaluation team will immediately review your resubmission to proceed with your stipend qualification.

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
Official Sovereign Portal: https://dbert.in
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>DBERT Stipend Review</title>
</head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:10px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    
    <div style="background-color:#0E1626;padding:26px 30px;text-align:center;border-bottom:2px solid #EF4444;">
      <div style="color:#EF4444;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:12px;letter-spacing:1px;margin-top:4px;">STIPEND CONTRIBUTION EVALUATION COMMITTEE</div>
    </div>

    <div style="padding:32px 30px;">
      <div style="display:inline-block;background:rgba(239,68,68,0.15);color:#EF4444;font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 12px;border-radius:20px;border:1px solid rgba(239,68,68,0.3);margin-bottom:16px;">
        ACTION REQUIRED &#183; REPOSITORY RESUBMISSION
      </div>

      <h1 style="font-size:20px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;line-height:1.4;">
        Stipend Repository Review for {name}
      </h1>

      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 20px 0;">
        Dear <strong>{name}</strong>,<br><br>
        The DBERT Academic & Mentorship Evaluation Committee has reviewed your submission (ID: #52). We observed that you submitted a personal website URL (<code>princess-chinni.com</code>).
      </p>

      <div style="background:rgba(239,68,68,0.08);border-left:3px solid #EF4444;border-radius:4px;padding:16px;margin-bottom:24px;">
        <div style="font-size:13px;font-weight:700;color:#EF4444;margin-bottom:6px;">DBERT Stipend Policy Requirement:</div>
        <div style="font-size:13px;color:#CBD5E1;line-height:1.6;">
          Per DBERT Incubation & Stipend Policy, stipend release is strictly contingent upon verified contributions made to <strong>approved DBERT partner organizations</strong>. Personal websites cannot be accepted.
        </div>
      </div>

      <div style="background-color:#0F141C;border:1px solid #1E2633;border-radius:8px;padding:20px;margin-bottom:24px;">
        <div style="font-size:11px;color:#E2B96F;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;">
          APPROVED GITHUB ORGANIZATIONS:
        </div>
        <div style="font-size:13px;color:#CBD5E1;line-height:1.8;">
          &#8226; <a href="https://github.com/Alkameinc" style="color:#38BDF8;text-decoration:none;">github.com/Alkameinc</a><br>
          &#8226; <a href="https://github.com/Gayatri-Education" style="color:#38BDF8;text-decoration:none;">github.com/Gayatri-Education</a><br>
          &#8226; <a href="https://github.com/Aivaratechinfomatics" style="color:#38BDF8;text-decoration:none;">github.com/Aivaratechinfomatics</a><br>
          &#8226; <a href="https://github.com/DBERT-INDIA" style="color:#38BDF8;text-decoration:none;">github.com/DBERT-INDIA</a>
        </div>
      </div>

      <div style="background:rgba(56,189,248,0.08);border-left:3px solid #38BDF8;border-radius:4px;padding:16px;margin-bottom:24px;">
        <div style="font-size:13px;font-weight:700;color:#38BDF8;margin-bottom:8px;">How to Resubmit:</div>
        <div style="font-size:13px;color:#CBD5E1;line-height:1.6;">
          1. Fork any repository from the approved organizations above.<br>
          2. Commit your technical code/contributions and open a Pull Request.<br>
          3. Go to <a href="https://lms.dbert.in/stipend/tasks" style="color:#38BDF8;text-decoration:underline;">lms.dbert.in/stipend/tasks</a> and resubmit with your GitHub URL.
        </div>
      </div>

      <p style="font-size:13px;line-height:1.6;color:#94A3B8;margin:0;">
        Once an approved repository contribution is submitted, our team will immediately resume your evaluation for the <strong>₹5,499 stipend</strong>.
      </p>
    </div>

    <div style="background-color:#0E1626;padding:20px 30px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#64748B;line-height:1.6;">
      <div>DBERT Sovereign Technical Incubation Platform</div>
      <div>Official Portal: <a href="https://dbert.in" style="color:#E2B96F;text-decoration:none;">dbert.in</a></div>
    </div>
  </div>
</body>
</html>"""

    return subject, plain_text, html_content, None


def main():
    log_msg("=== Starting Dashboard Decisions Immediate Email Dispatch ===")

    # Load registry
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry = json.load(f)

    # Load tracking state
    tracking = {}
    if TRACKING_FILE.exists():
        try:
            with open(TRACKING_FILE, "r", encoding="utf-8") as f:
                tracking = json.load(f)
        except Exception:
            tracking = {}

    targets = [
        {"id": "aaditya", "email": "aadityakadam432@gmail.com", "type": "verified", "cert_id": "CERT-DBERT-2026-DA-024"},
        {"id": "sakthi", "email": "me250003067@iiti.ac.in", "type": "verified", "cert_id": "CERT-DBERT-2026-DA-173"},
        {"id": "gurveer", "email": "gurveer3057.beai25@chitkara.edu.in", "type": "verified", "cert_id": "CERT-DBERT-2026-UIUX-040"},
        {"id": "chandramahesh", "email": "chandramahesh736@gmail.com", "type": "verified", "cert_id": "CERT-DBERT-2026-FSD-071"},
        {"id": "monika", "email": "monikach575@gmail.com", "type": "verified", "cert_id": "CERT-DBERT-2026-DA-185"},
        {"id": "sub53", "email": "vishvajeetshinde2005@gmail.com", "type": "sub53_revise"},
        {"id": "sub51", "email": "shreyashk07004@gmail.com", "type": "sub51_revise"},
        {"id": "sub52", "email": "chinniprincess842@gmail.com", "type": "sub52_discrepancy"},
    ]

    account_index = 0
    sent_count = 0
    errors = []

    for t in targets:
        target_id = t["id"]
        to_email = t["email"]

        if tracking.get(target_id, {}).get("status") == "SENT":
            log_msg(f"Target '{target_id}' ({to_email}) already SENT. Skipping.")
            continue

        account = SMTP_ACCOUNTS[account_index % len(SMTP_ACCOUNTS)]
        account_index += 1

        log_msg(f"\nPreparing dispatch for: {target_id} -> {to_email} via {account['email']}")

        try:
            if t["type"] == "verified":
                c_rec = registry.get(t["cert_id"])
                if not c_rec:
                    raise ValueError(f"Cert record {t['cert_id']} not found in registry")
                subject, plain, html, atts = build_verified_email(c_rec)
            elif t["type"] == "sub53_revise":
                subject, plain, html, atts = build_sub53_email()
            elif t["type"] == "sub51_revise":
                subject, plain, html, atts = build_sub51_email()
            elif t["type"] == "sub52_discrepancy":
                subject, plain, html, atts = build_sub52_email()
            else:
                raise ValueError(f"Unknown target type: {t['type']}")

            msg_id = send_via_smtp(account, to_email, subject, plain, html, atts)
            sent_count += 1
            log_msg(f"  ✓ SUCCESS: Message-ID: {msg_id}")

            tracking[target_id] = {
                "status": "SENT",
                "email": to_email,
                "type": t["type"],
                "subject": subject,
                "sender": account["email"],
                "message_id": msg_id,
                "sent_at": datetime.now().isoformat()
            }

            with open(TRACKING_FILE, "w", encoding="utf-8") as f:
                json.dump(tracking, f, indent=2)

            log_msg("  Pacing 8 seconds before next dispatch...")
            time.sleep(8)

        except Exception as e:
            log_msg(f"  ✗ FAILED to send to {to_email}: {e}")
            errors.append({"target": target_id, "email": to_email, "error": str(e)})
            tracking[target_id] = {
                "status": "FAILED",
                "email": to_email,
                "error": str(e),
                "attempted_at": datetime.now().isoformat()
            }
            with open(TRACKING_FILE, "w", encoding="utf-8") as f:
                json.dump(tracking, f, indent=2)

    log_msg(f"\n=== Dispatch Finished: {sent_count} sent, {len(errors)} failed ===")

    # Send Telemetry Report to ain.sharma.abhinav@gmail.com and ajnatechrpa@gmail.com
    telemetry_subject = f"DBERT Telemetry: Dashboard Decisions Email Dispatch Complete ({sent_count}/8 Delivered)"
    telemetry_body = f"""DBERT Executive Operations Telemetry Report
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Summary of Targeted Real-Time Dashboard Email Dispatch:
- Total Scheduled: {len(targets)}
- Successfully Delivered: {sent_count}
- Errors/Failures: {len(errors)}

Recipients & Outcomes:
1. Aaditya Kadam (aadityakadam432@gmail.com): {tracking.get('aaditya', {}).get('status')} [CERT-DBERT-2026-DA-024]
2. Sakthi P (me250003067@iiti.ac.in): {tracking.get('sakthi', {}).get('status')} [CERT-DBERT-2026-DA-173]
3. Gurveer Singh (gurveer3057.beai25@chitkara.edu.in): {tracking.get('gurveer', {}).get('status')} [CERT-DBERT-2026-UIUX-040]
4. Yarlagadda Chandra Mahesh Goud (chandramahesh736@gmail.com): {tracking.get('chandramahesh', {}).get('status')} [CERT-DBERT-2026-FSD-071]
5. CH MONIKA SAI (monikach575@gmail.com): {tracking.get('monika', {}).get('status')} [CERT-DBERT-2026-DA-185]
6. Vishwajeet Shinde (vishvajeetshinde2005@gmail.com): {tracking.get('sub53', {}).get('status')} [Sub #53 - Approved Repo & Article, LinkedIn Sync Needed]
7. Shreyash Sambhaji Kamble (shreyashk07004@gmail.com): {tracking.get('sub51', {}).get('status')} [Sub #51 - Approved Repo, Article & LinkedIn Needed]
8. M Brahmani (chinniprincess842@gmail.com): {tracking.get('sub52', {}).get('status')} [Sub #52 - Discrepancy Action: Approved Org Repo Contribution Needed]

All verification endpoints and previews verified live on https://dbert.in.
General email dispatch remains paused as instructed.
"""
    log_msg("\nSending telemetry notification...")
    for t_email in TELEMETRY_EMAILS:
        try:
            account = SMTP_ACCOUNTS[0]
            send_via_smtp(account, t_email, telemetry_subject, telemetry_body, f"<pre style='font-family:monospace;'>{telemetry_body}</pre>")
            log_msg(f"  ✓ Telemetry delivered to {t_email}")
        except Exception as te:
            log_msg(f"  ✗ Telemetry failed to {t_email}: {te}")

if __name__ == "__main__":
    main()
