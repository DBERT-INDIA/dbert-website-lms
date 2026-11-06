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
    ("ain.sharma.abhinav@gmail.com", "ain standard"),
    ("ain.sharma.abhinav+verify@gmail.com", "ain plus-alias"),
    ("ajnatechrpa@gmail.com", "ajna")
]

body = """Dear Badugu venkata rajesh,

Your official technical incubation and internship program record with DBERT has been recorded on the verification portal.

Credential Details:
- Candidate Name:        Badugu venkata rajesh
- Domain Track:          Data Analyst
- Program Tenure:        15 Aug 2026 - 15 Oct 2026
- Core Project:          Cognitive Solutions
- Academic Evaluation:   88/100 (Grade A (Very Good))
- Certificate ID:        CERT-DBERT-2026-DA-057
- Permanent Intern ID:   DBERT-2026-INT-1000

Direct Verification Portal Link:
dbert.in/verify/CERT-DBERT-2026-DA-057

Please visit the link above to view your complete credential dossier and review your verification status.

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
dbert.in/verify
"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
    server.login(SMTP_USER, SMTP_PASS)
    print("Authenticated successfully!")

    for email_addr, label in targets:
        print(f"\nDispatching to {label} ({email_addr})...")
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = f"DBERT Internship Verification: Badugu venkata rajesh [CERT-DBERT-2026-DA-057]"
        msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
        msg["To"] = email_addr
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="dbert.in")

        res = server.sendmail(FROM_EMAIL, [email_addr], msg.as_string())
        print(f"Sent to {email_addr}: {res}")
        time.sleep(5)

print("\nAll dispatched!")
