import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
import time

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "rsupmvvvvwrsuxuh"
FROM_EMAIL = "abhinav.sharma@dbert.in"

targets = [
    ("ain.sharma.abhinav@gmail.com", "ain"),
    ("ajnatechrpa@gmail.com", "ajna")
]

def build_body(name, cert_id, intern_id, domain, project, duration, score, grade):
    return f"""Dear {name},

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
dbert.in/verify/{cert_id}

Please visit the link above to view your complete credential dossier and review your verification status.

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
dbert.in/verify
"""

name = "Badugu venkata rajesh"
cert_id = "CERT-DBERT-2026-DA-057"
intern_id = "DBERT-2026-INT-1000"
domain = "Data Analyst"
project = "Cognitive Solutions"
duration = "15 Aug 2026 - 15 Oct 2026"
score = 88
grade = "Grade A (Very Good)"

context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
    server.login(SMTP_USER, SMTP_PASS)
    print("Authenticated successfully!")

    for email_addr, label in targets:
        print(f"\nDispatching to {label} ({email_addr})...")
        body = build_body(name, cert_id, intern_id, domain, project, duration, score, grade)
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = f"DBERT Internship Verification: {name} [{cert_id}]"
        msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
        msg["To"] = email_addr
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="dbert.in")

        res = server.sendmail(FROM_EMAIL, [email_addr], msg.as_string())
        print(f"Sent to {email_addr}: result={res}")
        print("Sleeping 10 seconds for clean pacing...")
        time.sleep(10)

print("\nAll guaranteed test emails dispatched!")
