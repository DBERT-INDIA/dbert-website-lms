import os
import sys
import smtplib
import ssl
import json
from email.utils import formatdate, make_msgid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REGISTRY_PATH = os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json")

# New Google App Password provided by user (LOCAL ONLY, NOT ON EC2)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "rsupmvvvvwrsuxuh"
FROM_NAME = "Mr. Abhinav Sharma (DBERT)"
FROM_EMAIL = "abhinav.sharma@dbert.in"

RECIPIENTS = [
    "ain.sharma.abhinav@gmail.com",
    "ajnatechrpa@gmail.com"
]

def build_full_provisional_message(rec, recipient_email):
    name = rec["holderName"]
    cert_id = rec["certId"]
    intern_id = rec["internId"]
    domain = rec["domain"]
    project = rec["project"]
    duration = rec["duration"]
    score = rec["score"]
    grade = rec["grade"]
    verify_url = f"https://dbert.in/verify?certid={cert_id}"

    subject = f"Official Internship Credential Packet: Certificate, Evaluation & Recommendation - {name} [{cert_id}]"

    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = recipient_email
    msg["Reply-To"] = FROM_EMAIL
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")
    msg["X-Mailer"] = "DBERT Credential Notification Service"
    msg["X-Entity-Ref-ID"] = cert_id

    text_content = f"""Dear {name},

We are pleased to provide your official DBERT Internship Credential Packet following the successful completion of your 2-Month Technical Incubation & Internship Program.

Official Credential Record:
--------------------------------------------------------------------------------
- Candidate Name:        {name}
- Domain Track:          {domain}
- Program Tenure:        {duration}
- Core Project:          {project}
- Academic Evaluation:   {score}/100 ({grade})
- Certificate ID:        {cert_id}
- Permanent Intern ID:   {intern_id}
- Online Verification:   {verify_url}
--------------------------------------------------------------------------------

You can verify the authenticity of your credentials at any time on our official verification portal:
{verify_url}

You may also add this verified credential directly to your LinkedIn profile using the 1-click verification link above.

Sincerely,

Mr. Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
Verification Portal: https://dbert.in/verify
Official Website: https://dbert.in
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DBERT Credential Packet</title>
<style>
  body {{
    margin: 0;
    padding: 0;
    background-color: #f1f5f9;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    -webkit-font-smoothing: antialiased;
  }}
  .email-wrapper {{
    width: 100%;
    background-color: #f1f5f9;
    padding: 30px 10px;
  }}
  .email-card {{
    max-width: 620px;
    margin: 0 auto;
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }}
  .header-bar {{
    background-color: #0F2942;
    padding: 26px 30px;
    text-align: center;
    border-bottom: 3px solid #D4AF37;
  }}
  .header-title {{
    color: #ffffff;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 0 0 4px 0;
  }}
  .header-sub {{
    color: #cbd5e1;
    font-size: 11px;
    letter-spacing: 0.5px;
    margin: 0;
    text-transform: uppercase;
  }}
  .body-content {{
    padding: 32px 30px 24px 30px;
  }}
  .greeting {{
    font-size: 17px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 12px;
  }}
  .intro-text {{
    font-size: 14px;
    line-height: 1.6;
    color: #334155;
    margin-bottom: 22px;
  }}
  .record-box {{
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 18px 20px;
    margin-bottom: 24px;
  }}
  .record-title {{
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #0F2942;
    margin: 0 0 12px 0;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 6px;
  }}
  .record-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  .record-table td {{
    padding: 6px 0;
    vertical-align: top;
  }}
  .label-col {{
    color: #64748b;
    width: 36%;
    font-weight: 500;
  }}
  .value-col {{
    color: #0f172a;
    font-weight: 600;
  }}
  .highlight-value {{
    color: #0F2942;
    font-weight: 700;
  }}
  .code-font {{
    font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
    font-size: 12.5px;
    color: #0284c7;
  }}
  .cta-section {{
    text-align: center;
    margin: 28px 0;
  }}
  .btn-verify {{
    display: inline-block;
    background-color: #0F2942;
    color: #ffffff !important;
    text-decoration: none;
    font-weight: 700;
    font-size: 14px;
    padding: 13px 32px;
    border-radius: 6px;
    border: 1px solid #D4AF37;
  }}
  .direct-url {{
    font-size: 11.5px;
    color: #64748b;
    margin-top: 10px;
    word-break: break-all;
  }}
  .direct-url a {{
    color: #0284c7;
    text-decoration: none;
  }}
  .docs-box {{
    background-color: #f8fafc;
    border-left: 3px solid #0F2942;
    padding: 14px 18px;
    margin-bottom: 24px;
    border-radius: 0 6px 6px 0;
  }}
  .docs-box-title {{
    font-size: 13px;
    font-weight: 700;
    color: #0F2942;
    margin: 0 0 8px 0;
  }}
  .docs-item {{
    font-size: 12.5px;
    line-height: 1.55;
    color: #475569;
    margin-bottom: 6px;
  }}
  .docs-item strong {{
    color: #0f172a;
  }}
  .sign-off-block {{
    border-top: 1px solid #e2e8f0;
    padding-top: 20px;
    margin-top: 24px;
    font-size: 13.5px;
    color: #334155;
    line-height: 1.5;
  }}
  .sign-name {{
    font-size: 15px;
    font-weight: 700;
    color: #0F2942;
    margin-top: 8px;
  }}
  .sign-role {{
    font-size: 12.5px;
    color: #64748b;
  }}
  .footer-bar {{
    background-color: #f8fafc;
    padding: 18px 30px;
    text-align: center;
    font-size: 11px;
    color: #64748b;
    border-top: 1px solid #e2e8f0;
    line-height: 1.5;
  }}
  .footer-bar a {{
    color: #0F2942;
    text-decoration: none;
    font-weight: 600;
  }}
</style>
</head>
<body>
<div class="email-wrapper">
  <div class="email-card">
    <div class="header-bar">
      <div class="header-title">DBERT</div>
      <div class="header-sub">Digital Blinc Education Research and Technology</div>
    </div>

    <div class="body-content">
      <div class="greeting">Dear {name},</div>
      <p class="intro-text">
        We are pleased to provide your official verified credential packet following the successful completion of your <strong>2-Month Technical Incubation & Internship Program</strong> with <strong>DBERT</strong>.
      </p>

      <div class="record-box">
        <div class="record-title">Official Credential Record</div>
        <table class="record-table">
          <tr>
            <td class="label-col">Candidate Name:</td>
            <td class="value-col">{name}</td>
          </tr>
          <tr>
            <td class="label-col">Domain Track:</td>
            <td class="value-col highlight-value">{domain}</td>
          </tr>
          <tr>
            <td class="label-col">Program Tenure:</td>
            <td class="value-col">{duration}</td>
          </tr>
          <tr>
            <td class="label-col">Core Project:</td>
            <td class="value-col">{project}</td>
          </tr>
          <tr>
            <td class="label-col">Academic Evaluation:</td>
            <td class="value-col highlight-value">{score}/100 ({grade})</td>
          </tr>
          <tr>
            <td class="label-col">Certificate ID:</td>
            <td class="value-col code-font">{cert_id}</td>
          </tr>
          <tr>
            <td class="label-col">Permanent Intern ID:</td>
            <td class="value-col code-font">{intern_id}</td>
          </tr>
        </table>
      </div>

      <div class="cta-section">
        <a href="{verify_url}" target="_blank" class="btn-verify">
          Verify Credential Online &rarr;
        </a>
        <div class="direct-url">
          Direct verification URL: <a href="{verify_url}">{verify_url}</a>
        </div>
      </div>

      <div class="docs-box">
        <div class="docs-box-title">Official Credential Documents on Sovereign Registry:</div>
        <div class="docs-item">
          &bull; <strong>1. Certificate of Completion:</strong> High-resolution credential featuring verification seal and quick-response authenticity code.
        </div>
        <div class="docs-item">
          &bull; <strong>2. Academic Project Evaluation:</strong> Comprehensive 9-dimension competency rubrics with academic clearance stamp.
        </div>
        <div class="docs-item">
          &bull; <strong>3. Official Letter of Recommendation:</strong> Executive institutional endorsement and performance appraisal.
        </div>
      </div>

      <div class="sign-off-block">
        Sincerely,<br>
        <div class="sign-name">{FROM_NAME}</div>
        <div class="sign-role">Program Head & Project Mentor<br>DBERT (Digital Blinc Education Research and Technology)</div>
      </div>
    </div>

    <div class="footer-bar">
      Official Verification Portal: <a href="https://dbert.in/verify">dbert.in/verify</a> &nbsp;&bull;&nbsp; 
      Website: <a href="https://dbert.in">dbert.in</a><br>
      &copy; 2026 DBERT. All rights reserved. This is an official institutional notification.
    </div>
  </div>
</div>
</body>
</html>
"""

    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(text_content, "plain", "utf-8"))
    alt_part.attach(MIMEText(html_content, "html", "utf-8"))
    msg.attach(alt_part)

    return msg

def main():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    sample_id = "CERT-DBERT-2026-DA-057"
    rec = registry.get(sample_id)
    if not rec:
        print(f"Error: {sample_id} not found in registry.")
        sys.exit(1)

    print(f"Loaded record for: {rec['holderName']} ({sample_id})")
    print(f"Connecting to {SMTP_HOST}:{SMTP_PORT} with user's new app password...")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.set_debuglevel(1)
        server.login(SMTP_USER, SMTP_PASS)
        print("Login SUCCESSFUL with new app password!")

        for target in RECIPIENTS:
            print(f"\nDispatching full email message to: {target}...")
            msg = build_full_provisional_message(rec, target)
            res = server.sendmail(FROM_EMAIL, [target], msg.as_string())
            print(f"Sendmail to {target} returned: {res}")

    print("\n[SUCCESS] Dispatched to all test recipients!")

if __name__ == '__main__':
    main()
