import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "rsupmvvvvwrsuxuh"
FROM_EMAIL = "abhinav.sharma@dbert.in"
TARGETS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

# Test Sub 1: Subject = "DBERT Internship Update - Badugu venkata rajesh"
sub1 = "DBERT Internship Update - Badugu venkata rajesh"
body1 = f"""Hi Badugu venkata rajesh,

Your internship verification record has been updated on the portal.

You can view your record here:
dbert.in/verify/CERT-DBERT-2026-DA-057

Candidate: Badugu venkata rajesh
Track: Data Analyst
Tenure: 15 Aug 2026 to 15 Oct 2026
Score: 88/100

Best regards,
Abhinav Sharma
DBERT
"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
    server.login(SMTP_USER, SMTP_PASS)
    for target in TARGETS:
        msg = MIMEText(body1, "plain", "utf-8")
        msg["Subject"] = sub1
        msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
        msg["To"] = target
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="dbert.in")

        res = server.sendmail(FROM_EMAIL, [target], msg.as_string())
        print(f"Sent human subject test to {target}: {res}")

print("Dispatched subject test!")
