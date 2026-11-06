import smtplib
import ssl
import json
import os
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REGISTRY_PATH = os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "rsupmvvvvwrsuxuh"
FROM_EMAIL = "abhinav.sharma@dbert.in"
TARGETS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
    registry = json.load(f)

rec = registry.get("CERT-DBERT-2026-DA-057")
name = rec["holderName"]
cert_id = rec["certId"]
intern_id = rec["internId"]
domain = rec["domain"]
project = rec["project"]
duration = rec["duration"]
score = rec["score"]
grade = rec["grade"]

body = f"""DBERT — Digital Blinc Education Research and Technology
Official Credential Record Notification

Dear {name},

We are pleased to provide your official DBERT Technical Incubation & Internship Program credential record:

================================================================================
OFFICIAL CREDENTIAL RECORD
================================================================================
Candidate Name:        {name}
Domain Track:          {domain}
Program Tenure:        {duration}
Core Project:          {project}
Academic Evaluation:   {score}/100 ({grade})
Certificate ID:        {cert_id}
Permanent Intern ID:   {intern_id}
Direct Verification:   dbert.in/verify/{cert_id}
================================================================================

ONLINE VERIFICATION INSTRUCTIONS:
To view and verify your full credential record on the sovereign registry, open your browser and visit:
dbert.in/verify/{cert_id}

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
Official Portal: dbert.in/verify
Website: dbert.in
"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
    server.login(SMTP_USER, SMTP_PASS)
    for target in TARGETS:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = f"Official Internship Credential Record: {name} [{cert_id}]"
        msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
        msg["To"] = target
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="dbert.in")

        res = server.sendmail(FROM_EMAIL, [target], msg.as_string())
        print(f"Sent plain text dossier to {target}: {res}")

print("Dispatched pure plain-text full dossier!")
