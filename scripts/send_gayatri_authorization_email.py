"""
Script: send_gayatri_authorization_email.py
Purpose: Dispatches official corporate authorization email to Envista Cyber Defence
         granting rights to use, promote, and demonstrate Gayatri AI products.
Sender: abhinav.sharma@dbert.in
Recipients: kaarthik.krishnan@envistacyberdefence.com, amitkumar.more@envistacyberdefence.com
"""

import sys
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "rsupmvvvvwrsuxuh"
SENDER_NAME = "Abhinav Sharma"

# Recipients
RECIPIENTS = [
    "kaarthik.krishnan@envistacyberdefence.com",
    "amitkumar.more@envistacyberdefence.com"
]
CC_LIST = [
    "abhinav.sharma@dbert.in"
]

SUBJECT = "Official Authorization: Product Usage, Promotion & Demonstration Rights for Gayatri AI — Envista Cyber Defence"

PLAIN_TEXT = """OFFICIAL MEMORANDUM & LETTER OF AUTHORIZATION
Ref: DBERT/AUTH/2026/GAYATRI-ECD-01
Date: November 17, 2026

To:
Mr. Kaarthik Krishnan & Mr. Amitkumar More
Envista Cyber Defence
kaarthik.krishnan@envistacyberdefence.com | amitkumar.more@envistacyberdefence.com

From:
Mr. Abhinav Sharma
Founder & Lead, DBERT
abhinav.sharma@dbert.in | https://dbert.in

Subject: Official Authorization to Use, Promote, and Demonstrate Gayatri AI Products

Dear Mr. Kaarthik Krishnan and Mr. Amitkumar More,

I am writing on behalf of DBERT (https://dbert.in) to formally grant Envista Cyber Defence, and specifically you both as its authorized representatives, the official authority and rights to use, promote, and demonstrate the Gayatri AI suite of products.

Official Product Portal: https://gayatrieducation.tech

Please note that Gayatri AI is one of the premier proprietary artificial intelligence products conceptualized, engineered, and developed under the DBERT Incubation and Internship Program (https://dbert.in). It represents our flagship breakthrough in lightweight, localized, and resilient multi-agent AI ecosystems for high-security, education, and enterprise environments.

Under this official authorization, Envista Cyber Defence is hereby granted the non-exclusive authority to:
1. Conduct Live Product Demonstrations: Deliver interactive walkthroughs, technical presentations, and executive demonstrations of Gayatri AI products and architectural capabilities to enterprise prospects, educational institutions, cybersecurity clients, and strategic stakeholders.
2. Market & Solution Promotion: Promote, reference, and position Gayatri AI solutions (as hosted on https://gayatrieducation.tech) across your corporate cybersecurity, EdTech, and enterprise advisory channels and collateral.
3. Proof-of-Concept (PoC) & Pilot Trials: Evaluate and deploy demonstration sandboxes and pilot environments for prospective clients seeking advanced AI-driven educational and enterprise intelligence workflows.

Governance & Collaboration Terms:
- Proprietary Notice: Core intellectual property, proprietary algorithms, and brand architecture of Gayatri AI remain vested with DBERT and the Gayatri AI project team.
- Technical Support & Sandbox Access: The DBERT Engineering and Incubation Desk will provide full technical assistance, updated demo sandboxes, API access tokens, and solution architecture documentation to ensure seamless client demonstrations.
- Direct Escalation Desk: For specialized client requirements, tailored enterprise SLAs, or custom deployments, our admissions and incubation desk remains at your immediate service.

We highly value our partnership with Envista Cyber Defence and look forward to your active advocacy and successful client demonstrations of Gayatri AI.

Should you require any customized demonstration collateral, sandbox provisioning, or technical briefing sessions, please feel free to reach out to me directly at abhinav.sharma@dbert.in or through our technical desk at admissions@dbert.in.

Warm regards,

Abhinav Sharma
Founder & Lead, DBERT
Admissions & Incubation Council
DBERT (https://dbert.in)
Email: abhinav.sharma@dbert.in
Admissions Desk: +91 81929 11360
Official Product Portal: https://gayatrieducation.tech
"""

HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #1e293b;
    background-color: #f8fafc;
    margin: 0;
    padding: 24px;
  }
  .container {
    max-width: 680px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    border: 1px solid #e2e8f0;
  }
  .header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    padding: 32px 36px;
    color: #ffffff;
  }
  .badge {
    display: inline-block;
    background: rgba(99, 102, 241, 0.25);
    border: 1px solid rgba(165, 180, 252, 0.4);
    color: #c7d2fe;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 12px;
  }
  .header h1 {
    margin: 0;
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.3;
  }
  .header .ref {
    margin-top: 8px;
    font-size: 12px;
    color: #94a3b8;
  }
  .content {
    padding: 36px;
  }
  .salutation {
    font-size: 16px;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 16px;
  }
  p {
    font-size: 14px;
    color: #334155;
    margin-bottom: 16px;
  }
  .highlight-card {
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    margin: 22px 0;
  }
  .highlight-card p {
    margin: 0;
    color: #1e40af;
    font-size: 14px;
    font-weight: 500;
  }
  .auth-box {
    background: #faf5ff;
    border: 1px solid #e9d5ff;
    border-radius: 8px;
    padding: 20px 24px;
    margin: 24px 0;
  }
  .auth-box h3 {
    margin: 0 0 12px 0;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #6b21a8;
  }
  .auth-list {
    margin: 0;
    padding-left: 18px;
  }
  .auth-list li {
    font-size: 13.5px;
    color: #3b0764;
    margin-bottom: 10px;
    line-height: 1.5;
  }
  .auth-list li strong {
    color: #1e1b4b;
  }
  .cta-block {
    text-align: center;
    margin: 28px 0 20px 0;
  }
  .cta-btn {
    display: inline-block;
    background: #2563eb;
    color: #ffffff !important;
    text-decoration: none;
    font-weight: 600;
    font-size: 14px;
    padding: 12px 28px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
  }
  .footer-sig {
    margin-top: 32px;
    padding-top: 24px;
    border-top: 1px solid #e2e8f0;
  }
  .sig-name {
    font-size: 15px;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
  }
  .sig-title {
    font-size: 13px;
    color: #64748b;
    margin: 2px 0 0 0;
  }
  .sig-org {
    font-size: 12px;
    color: #94a3b8;
    margin: 2px 0 0 0;
  }
  .meta-footer {
    background: #f1f5f9;
    padding: 16px 36px;
    font-size: 11px;
    color: #64748b;
    text-align: center;
    border-top: 1px solid #e2e8f0;
  }
</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="badge">Official Corporate Authorization</div>
      <h1>Grant of Usage, Promotion & Demonstration Rights: Gayatri AI</h1>
      <div class="ref">Ref: DBERT/AUTH/2026/GAYATRI-ECD-01 &bull; Date: November 17, 2026</div>
    </div>
    
    <div class="content">
      <div class="salutation">Dear Mr. Kaarthik Krishnan and Mr. Amitkumar More,</div>
      
      <p>I am writing on behalf of <strong>DBERT</strong> (<a href="https://dbert.in" style="color: #2563eb; text-decoration: none;">dbert.in</a>) to formally grant <strong>Envista Cyber Defence</strong>, and specifically you both as its authorized executive representatives, the official authority and rights to <strong>use, promote, and demonstrate the Gayatri AI product suite</strong>.</p>
      
      <div class="highlight-card">
        <p><strong>Incubation Pedigree & Institutional Lineage:</strong><br>
        Please note that <strong>Gayatri AI</strong> is one of the premier proprietary artificial intelligence products conceptualized, engineered, and developed under the <strong>DBERT Incubation and Internship Program</strong> (<a href="https://dbert.in" style="color: #1d4ed8; text-decoration: underline;">https://dbert.in</a>). It represents our flagship breakthrough in lightweight, offline-resilient, multi-agent frameworks tailored for high-security enterprise and educational environments.</p>
      </div>

      <p>Official Product Platform: <a href="https://gayatrieducation.tech" style="color: #2563eb; font-weight: 600; text-decoration: none;">https://gayatrieducation.tech</a></p>

      <div class="auth-box">
        <h3>Scope of Authorized Rights</h3>
        <ol class="auth-list">
          <li><strong>Enterprise & Client Demonstrations:</strong> Full authorization to present, showcase, and run live interactive demonstrations of Gayatri AI software, model architectures, and student/enterprise portals to prospective clients, universities, institutions, and enterprise partners.</li>
          <li><strong>Marketing & Portfolio Promotion:</strong> Authority to promote, reference, and feature Gayatri AI capabilities (<a href="https://gayatrieducation.tech" style="color: #6b21a8;">gayatrieducation.tech</a>) within Envista Cyber Defence’s solution portfolios, cybersecurity advisory services, and digital transformation proposals.</li>
          <li><strong>Proof-of-Concept (PoC) Engagements:</strong> Authority to orchestrate client pilot evaluations and technical proof-of-concept setups utilizing official Gayatri AI sandboxes and frameworks.</li>
        </ol>
      </div>

      <p><strong>Technical Governance & Support Desk:</strong><br>
      The DBERT Incubation and Engineering Council will provide full technical backing, sandbox provisioning, API documentation, and updated presentation assets to support your demonstration engagements. All underlying product intellectual property and source architectures remain protected under DBERT stewardship.</p>

      <div class="cta-block">
        <a href="https://gayatrieducation.tech" class="cta-btn">Access Gayatri AI Platform &rarr;</a>
      </div>

      <p>We deeply appreciate the synergy between DBERT and Envista Cyber Defence and look forward to your active advocacy and impactful client showcases.</p>

      <p>Should you require customized sandboxes, co-branded demonstration materials, or technical briefings, please reach out directly to my desk.</p>

      <div class="footer-sig">
        <p class="sig-name">Abhinav Sharma</p>
        <p class="sig-title">Founder & Lead, DBERT</p>
        <p class="sig-org">Admissions, Incubation & Technical Council &bull; <a href="https://dbert.in" style="color: #64748b; text-decoration: none;">dbert.in</a></p>
        <p class="sig-org">Email: <a href="mailto:abhinav.sharma@dbert.in" style="color: #2563eb; text-decoration: none;">abhinav.sharma@dbert.in</a> &bull; Admissions Desk: +91 81929 11360</p>
      </div>
    </div>

    <div class="meta-footer">
      This document constitutes an official electronic authorization issued by DBERT (dbert.in) for Envista Cyber Defence.<br>
      &copy; 2026 DBERT & Gayatri AI. All rights reserved.
    </div>
  </div>
</body>
</html>
"""

def send_authorization_email(dry_run=False):
    print("=" * 70)
    print("DBERT / GAYATRI AI - CORPORATE AUTHORIZATION EMAIL DISPATCH")
    print("=" * 70)
    print(f"Sender: {SENDER_NAME} <{SMTP_USER}>")
    print(f"Recipients (To): {', '.join(RECIPIENTS)}")
    print(f"Copy (CC): {', '.join(CC_LIST)}")
    print(f"Subject: {SUBJECT}")
    print(f"Product Website: https://gayatrieducation.tech")
    print(f"Incubation Entity: DBERT Incubation & Internship Program (https://dbert.in)")
    print("=" * 70)

    if dry_run:
        print("[DRY RUN MODE] Email rendered successfully. No message dispatched.")
        return True

    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = f"{SENDER_NAME} <{SMTP_USER}>"
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Cc"] = ", ".join(CC_LIST)
    msg["Reply-To"] = SMTP_USER
    msg["X-Mailer"] = "DBERT Executive Dispatcher v2.0"
    msg["Message-ID"] = f"<auth-gayatri-ecd-{int(datetime.now().timestamp())}@{SMTP_USER.split('@')[1]}>"

    # Attach Plain and HTML parts
    part1 = MIMEText(PLAIN_TEXT, "plain", "utf-8")
    part2 = MIMEText(HTML_CONTENT, "html", "utf-8")
    msg.attach(part1)
    msg.attach(part2)

    all_destinations = RECIPIENTS + CC_LIST

    print(f"Connecting to SMTP SSL {SMTP_SERVER}:{SMTP_PORT} ...")
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context, timeout=25) as server:
            server.login(SMTP_USER, SMTP_PASS)
            print(f"Authenticated successfully as {SMTP_USER}.")
            server.sendmail(SMTP_USER, all_destinations, msg.as_string())
            print(f"[SUCCESS] Official authorization email successfully dispatched to:")
            for r in all_destinations:
                print(f"   -> {r}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to dispatch email: {e}")
        return False

if __name__ == "__main__":
    is_live = "--send" in sys.argv or "--live" in sys.argv
    dry_run = not is_live
    send_authorization_email(dry_run=dry_run)
