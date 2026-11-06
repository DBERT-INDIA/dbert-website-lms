import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
import time

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "rsupmvvvvwrsuxuh"
FROM_EMAIL = "abhinav.sharma@dbert.in"
TARGETS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

# Test 5A: Clean HTML Button ONLY (no raw URLs in text)
def send_test_5a(server, target):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Diagnostic Test 5A: HTML Button link"
    msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
    msg["To"] = target
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")

    text = f"Hello,\n\nPlease verify your official credential record on the DBERT sovereign registry.\n\nVisit: dbert.in/verify\nCertificate ID: CERT-DBERT-2026-DA-057\n\nSent: {formatdate(localtime=True)}"
    html = f"""<html><body style="font-family: Arial, sans-serif; padding: 20px;">
<p>Hello Abhinav,</p>
<p>This is Test 5A testing an HTML button without raw URL strings in the body.</p>
<p style="margin: 20px 0;">
  <a href="https://dbert.in/verify/CERT-DBERT-2026-DA-057" style="background: #0F2942; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">
    View Credential Record &rarr;
  </a>
</p>
<p style="color: #64748b; font-size: 12px;">Portal: dbert.in/verify &bull; ID: CERT-DBERT-2026-DA-057</p>
</body></html>"""
    msg.attach(MIMEText(text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    return server.sendmail(FROM_EMAIL, [target], msg.as_string())

# Test 5B: Plain text with domain path (no https:// prefix)
def send_test_5b(server, target):
    msg = MIMEText(
        f"Hello,\n\nThis is Diagnostic Test 5B testing plain text with domain path (no https:// prefix):\n\ndbert.in/verify/CERT-DBERT-2026-DA-057\n\nSent at: {formatdate(localtime=True)}",
        "plain",
        "utf-8"
    )
    msg["Subject"] = f"Diagnostic Test 5B: Domain path without https"
    msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
    msg["To"] = target
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")
    return server.sendmail(FROM_EMAIL, [target], msg.as_string())

# Test 5C: Clean portal address only
def send_test_5c(server, target):
    msg = MIMEText(
        f"Hello,\n\nThis is Diagnostic Test 5C with portal address and search instructions:\n\n1. Go to: dbert.in/verify\n2. Enter Certificate ID: CERT-DBERT-2026-DA-057\n\nSent at: {formatdate(localtime=True)}",
        "plain",
        "utf-8"
    )
    msg["Subject"] = f"Diagnostic Test 5C: Clean portal address"
    msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
    msg["To"] = target
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")
    return server.sendmail(FROM_EMAIL, [target], msg.as_string())

context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
    server.login(SMTP_USER, SMTP_PASS)
    for target in TARGETS:
        print(f"\n--- Sending to {target} ---")
        r_a = send_test_5a(server, target)
        print("Test 5A dispatched:", r_a)
        time.sleep(2)
        r_b = send_test_5b(server, target)
        print("Test 5B dispatched:", r_b)
        time.sleep(2)
        r_c = send_test_5c(server, target)
        print("Test 5C dispatched:", r_c)
        time.sleep(2)

print("\nAll Test 5 variations dispatched!")
