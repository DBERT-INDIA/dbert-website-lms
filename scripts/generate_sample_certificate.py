import os
import re
from io import BytesIO
from datetime import date
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
import fitz  # PyMuPDF

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "apps", "portal", "static", "certificates")
BG_PATH = os.path.join(ASSETS_DIR, "targets12.png")
SIG_PATH = os.path.join(ASSETS_DIR, "sig_light_cursive.png")

OUTPUT_PDF = os.path.join(BASE_DIR, "sample_certificate_kushal_agarwal.pdf")
OUTPUT_PNG = os.path.join(BASE_DIR, "sample_certificate_kushal_agarwal.png")

# Certificate details
NAME = "Kushal Agarwal"
DOMAIN = "Data Analyst"
TOPICS = "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics"
PROJECT = "Gayatri AI — Enterprise Educational Intelligence Platform"
DURATION = "01 July 2026 to 30 September 2026"
INTERN_ID = "GE-DBERT-INT-KA-2749-001"
CERT_ID = "CERT-GE-DBERT-2026-DA-001"
VERIFY_URL = f"https://lms.dbert.in/verify?certid={CERT_ID}"

# 1. Generate QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=8,
    border=1
)
qr.add_data(VERIFY_URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white")
qr_buf = BytesIO()
qr_img.save(qr_buf, format="PNG")
qr_buf.seek(0)

# 2. Draw Certificate PDF on 640 x 495 canvas
c = canvas.Canvas(OUTPUT_PDF, pagesize=(640, 495))
c.setAuthor("Gayatri Education in collaboration with DBERT")
c.setTitle(f"Internship Certificate — {NAME}")

# Background
if os.path.isfile(BG_PATH):
    c.drawImage(BG_PATH, 0, 0, width=640, height=495)
else:
    c.setFillColor(colors.HexColor("#0f172a"))
    c.rect(0, 0, 640, 495, fill=1, stroke=0)

# Award text
c.setFillColor(colors.white)
c.setFont("Helvetica", 12)
c.drawCentredString(320, 305, "This certificate is awarded to")

# Name
c.setFillColor(colors.HexColor("#facc15"))
c.setFont("Helvetica-BoldOblique", 16)
c.drawCentredString(320, 283, NAME.strip().upper())

# Completion statement
c.setFillColor(colors.white)
c.setFont("Helvetica", 12)
c.drawCentredString(320, 265, "on successful completion of the Internship in")

# Domain
c.setFillColor(colors.HexColor("#e2b96f"))
c.setFont("Helvetica-BoldOblique", 15)
c.drawCentredString(320, 243, DOMAIN)

# Topics
c.setFillColor(colors.white)
c.setFont("Helvetica", 11)
if len(TOPICS) > 75:
    part1 = TOPICS[:75]
    last_space = part1.rfind(",")
    if last_space != -1:
        t1 = TOPICS[:last_space + 1]
        t2 = TOPICS[last_space + 1:].strip()
        c.drawCentredString(320, 218, f"Covering topics: {t1}")
        c.drawCentredString(320, 204, t2)
    else:
        c.drawCentredString(320, 215, f"Covering topics: {TOPICS}")
else:
    c.drawCentredString(320, 215, f"Covering topics: {TOPICS}")

# Project
c.setFont("Helvetica", 11)
c.drawCentredString(320, 187, f"Project Worked: {PROJECT}")

# Duration
c.setFont("Helvetica", 11)
c.drawCentredString(320, 169, f"Internship Duration: {DURATION}")

# Intern ID
c.setFont("Helvetica-Bold", 10.5)
c.setFillColor(colors.HexColor("#cbd5e1"))
c.drawCentredString(320, 132, f"Intern ID: {INTERN_ID}")

# Signature block
if os.path.isfile(SIG_PATH):
    try:
        c.drawImage(ImageReader(SIG_PATH), 103, 105, width=1.25 * inch, height=0.75 * inch, mask="auto")
    except Exception as e:
        print("Sig error:", e)

c.setFillColor(colors.white)
c.setFont("Helvetica-Bold", 12)
c.drawString(103, 95, "Sarita Bansal")

c.setFont("Helvetica", 10)
c.setFillColor(colors.HexColor("#94a3b8"))
c.drawString(103, 83, "Program Head")

# Dynamic QR Code
c.drawImage(ImageReader(qr_buf), 549, 63, width=54, height=54)

# Footer metadata
c.setFillColor(colors.HexColor("#94a3b8"))
c.setFont("Helvetica", 9)
c.drawCentredString(320, 36, f"Certificate ID: {CERT_ID}")

c.setFont("Helvetica-Bold", 8.5)
c.setFillColor(colors.HexColor("#64748b"))
c.drawCentredString(320, 23, "MSME Statutory Registration: UDYAM-UP-29-0109046")

c.setFont("Helvetica", 8)
c.drawCentredString(320, 11, "Gayatri Education in collaboration with DBERT · lms.dbert.in")

c.showPage()
c.save()
print("Saved PDF to:", OUTPUT_PDF)

# 3. Convert to PNG preview using PyMuPDF (fitz)
doc = fitz.open(OUTPUT_PDF)
page = doc.load_page(0)
pix = page.get_pixmap(dpi=150)
pix.save(OUTPUT_PNG)
print("Saved PNG preview to:", OUTPUT_PNG)
