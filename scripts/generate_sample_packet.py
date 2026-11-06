import os
import re
from io import BytesIO
import qrcode
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz  # PyMuPDF

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "apps", "portal", "static", "certificates")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "sample_kushal_agarwal")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BG_CERT_PATH = os.path.join(ASSETS_DIR, "targets12.png")
SIG_LIGHT_PATH = os.path.join(ASSETS_DIR, "sig_light_edwardian.png")
SIG_DARK_PATH = os.path.join(ASSETS_DIR, "sig_dark_edwardian.png")
PLAGIARISM_STAMP_PATH = os.path.join(ASSETS_DIR, "turnitin_plagiarism_stamp.png")

# Register high-end TrueType serif fonts for luxury Certificate typography
HAS_GEORGIA = False
HAS_PALATINO = False
try:
    pdfmetrics.registerFont(TTFont("Georgia", "C:/Windows/Fonts/georgia.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", "C:/Windows/Fonts/georgiab.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", "C:/Windows/Fonts/georgiai.ttf"))
    pdfmetrics.registerFont(TTFont("Georgia-BoldItalic", "C:/Windows/Fonts/georgiaz.ttf"))
    HAS_GEORGIA = True
    print("Georgia font family successfully registered for Certificate typography.")
except Exception as e:
    print("Warning: Could not load Georgia fonts, fallback to standard Helvetica:", e)

try:
    pdfmetrics.registerFont(TTFont("Palatino-Italic", "C:/Windows/Fonts/palai.ttf"))
    HAS_PALATINO = True
    print("Palatino-Italic registered for ceremonial lead-in typography.")
except Exception as e:
    print("Warning: Could not load Palatino-Italic, fallback to Georgia-Italic:", e)

FONT_CERT_SERIF = "Georgia" if HAS_GEORGIA else "Helvetica"
FONT_CERT_SERIF_BOLD = "Georgia-Bold" if HAS_GEORGIA else "Helvetica-Bold"
FONT_CERT_SERIF_ITALIC = "Georgia-Italic" if HAS_GEORGIA else "Helvetica-Oblique"
FONT_CERT_SERIF_BOLDITALIC = "Georgia-BoldItalic" if HAS_GEORGIA else "Helvetica-BoldOblique"
FONT_CERT_LEADIN = "Palatino-Italic" if HAS_PALATINO else FONT_CERT_SERIF_ITALIC

SIGNATORY_NAME = "Mr. Abhinav Sharma"
SIGNATORY_TITLE = "Program Head & Project Mentor"
SIGNATORY_ORG = "DBERT"
ORG_FULL_NAME = "(Digital Blinc Education Research and Technology)"

# Candidate details (Kushal Agarwal - 2-Month Program)
C_DATA = {
    "name": "Kushal Agarwal",
    "email": "kushalagarwal27496@gmail.com",
    "college": "Ajeekya DY Patil University",
    "domain": "Data Analyst",
    "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
    "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
    "duration": "July to September 2026 (2 Months)",
    "start_date": "July 2026",
    "end_date": "September 2026",
    "cert_id": "CERT-DBERT-2026-DA-001",
    "intern_id": "DBERT-INT-KA-6769-001",
    "phone": "9503296769",
    "score": 84,
    "grade": "Grade: A (Very Good Performance)",
    "eval_date": "01 October 2026",
    "issue_date": "2026-10-01",
    "rubric_marks": [17, 9, 8, 8, 8, 9, 8, 8, 9]  # Total 84
}


# Defensive string fitting helpers (prevents text overflow / wrapping)
def draw_fitted_centre(c, x, y, text, font_name, max_size, max_w, fill_color):
    c.setFillColor(fill_color)
    sz = max_size
    while sz > 7:
        w = c.stringWidth(text, font_name, sz)
        if w <= max_w:
            break
        sz -= 0.5
    c.setFont(font_name, sz)
    c.drawCentredString(x, y, text)
    return sz


def draw_fitted_string(c, x, y, text, font_name, max_size, max_w, fill_color):
    c.setFillColor(fill_color)
    sz = max_size
    while sz > 6.5:
        w = c.stringWidth(text, font_name, sz)
        if w <= max_w:
            break
        sz -= 0.5
    c.setFont(font_name, sz)
    c.drawString(x, y, text)
    return sz


def generate_qr_buffer(url, box_size=8, border=1):
    qr = qrcode.QRCode(version=1, box_size=box_size, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_buf = BytesIO()
    qr_img.save(qr_buf, format="PNG")
    qr_buf.seek(0)
    return qr_buf


def safe_save_canvas(buf_or_path, target_path, generate_fn, *args):
    """Generates PDF to buffer first, then safely writes to file (or _updated if locked by viewer)."""
    buf = BytesIO()
    generate_fn(buf, *args)
    pdf_bytes = buf.getvalue()

    written_path = target_path
    try:
        with open(target_path, "wb") as f:
            f.write(pdf_bytes)
    except (PermissionError, OSError):
        base, ext = os.path.splitext(target_path)
        written_path = f"{base}_updated{ext}"
        with open(written_path, "wb") as f:
            f.write(pdf_bytes)
        print(f"Target was locked by viewer; saved updated version to: {written_path}")

    # Generate PNG preview
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=150)
        png_p = written_path.replace(".pdf", ".png")
        pix.save(png_p)
        # Also save to base png if alt was written
        base_png = target_path.replace(".pdf", ".png")
        if png_p != base_png:
            pix.save(base_png)
        print("Generated preview:", png_p)
    except Exception as e:
        print("Preview error:", e)

    return written_path


# ======================================================================================
# DOCUMENT 1: CERTIFICATE OF COMPLETION (640 x 495 Landscape Canvas)
# Professional Redesign: Palatino lead-in, Georgia-Bold 22pt name, gold hairline rules,
# consolidated metadata, enlarged signature, centered credential block, no MSME
# ======================================================================================
def draw_cert_completion(target_stream, c_data):
    c = canvas.Canvas(target_stream, pagesize=(640, 495))
    c.setTitle(f"Official Verified Certificate of Completion — {c_data['name']} [{c_data['cert_id']}]")
    c.setAuthor("Digital Blinc Education Research and Technology (DBERT)")
    c.setSubject(f"2-Month Technical Incubation & Internship Credential in {c_data['domain']}")
    c.setKeywords(f"DBERT, Internship Certificate, Credential, {c_data['cert_id']}, {c_data['intern_id']}, {c_data['name']}, {c_data['domain']}, Verified, Authenticity Registry")
    c.setCreator("DBERT Academic & Technical Credential Engine v2026.2")

    # 1. Background
    if os.path.isfile(BG_CERT_PATH):
        c.drawImage(BG_CERT_PATH, 0, 0, width=640, height=495)
    else:
        c.setFillColor(colors.HexColor("#0f172a"))
        c.rect(0, 0, 640, 495, fill=1, stroke=0)

    # ──────────────────────────────────────────────────────────────
    # 2. PROFESSIONAL TYPOGRAPHY HIERARCHY (Top → Bottom Pyramid)
    # ──────────────────────────────────────────────────────────────

    # Change 1: Upgraded lead-in with Palatino-Italic 13pt, warm cream
    c.setFillColor(colors.HexColor("#F5F0E8"))
    c.setFont(FONT_CERT_LEADIN, 13)
    c.drawCentredString(320, 320, "This certificate is proudly awarded to")

    # Change 2: Top gold hairline rule (framing the name)
    c.setStrokeColor(colors.HexColor("#D4AF37"))
    c.setLineWidth(0.6)
    c.line(160, 314, 480, 314)

    # Change 3: Larger, more prominent candidate name — Georgia-Bold 22pt
    draw_fitted_centre(c, 320, 290, c_data["name"].strip().upper(),
                       FONT_CERT_SERIF_BOLD, 22, 420, colors.HexColor("#D4AF37"))

    # Change 2 (cont): Bottom gold hairline rule (framing the name)
    c.setStrokeColor(colors.HexColor("#D4AF37"))
    c.setLineWidth(0.6)
    c.line(160, 280, 480, 280)

    # Change 4: Richer completion statement with explicit 2-Month mention
    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.setFont(FONT_CERT_SERIF_ITALIC, 11)
    c.drawCentredString(320, 262, "for successful completion of a 2-Month Internship in")

    # Change 5: Larger domain track — Georgia-Bold 16pt
    draw_fitted_centre(c, 320, 240, c_data["domain"],
                       FONT_CERT_SERIF_BOLD, 16, 420, colors.HexColor("#E5C07B"))

    # Change 6: Thin muted separator above metadata block
    c.setStrokeColor(colors.HexColor("#64748B"))
    c.setLineWidth(0.4)
    c.line(180, 228, 460, 228)

    # Change 6 (cont): Consolidated metadata block — Topics, Project, Duration
    topics = c_data["topics"]
    if len(topics) > 75:
        part1 = topics[:75]
        last_sp = part1.rfind(",")
        if last_sp != -1:
            t1 = topics[:last_sp + 1]
            t2 = topics[last_sp + 1:].strip()
            draw_fitted_centre(c, 320, 214, f"Covering: {t1}",
                               FONT_CERT_SERIF, 9, 460, colors.HexColor("#94A3B8"))
            draw_fitted_centre(c, 320, 202, t2,
                               FONT_CERT_SERIF, 9, 460, colors.HexColor("#94A3B8"))
            project_y = 188
        else:
            draw_fitted_centre(c, 320, 214, f"Covering: {topics}",
                               FONT_CERT_SERIF, 9, 460, colors.HexColor("#94A3B8"))
            project_y = 200
    else:
        draw_fitted_centre(c, 320, 214, f"Covering: {topics}",
                           FONT_CERT_SERIF, 9, 460, colors.HexColor("#94A3B8"))
        project_y = 200

    draw_fitted_centre(c, 320, project_y, f"Project: {c_data['project']}",
                       FONT_CERT_SERIF, 9.5, 460, colors.HexColor("#E2E8F0"))

    duration_str = f"Duration: {c_data['duration']}"
    draw_fitted_centre(c, 320, project_y - 14, duration_str,
                       FONT_CERT_SERIF, 9, 460, colors.HexColor("#94A3B8"))

    # ──────────────────────────────────────────────────────────────
    # 3. BOTTOM TIER: Signature | Credential IDs | QR Code
    # ──────────────────────────────────────────────────────────────

    # Change 7: Upgraded signature block — larger image + gold underline
    sig_x = 65
    sig_w = 105   # enlarged from 88
    sig_h = 16.8  # proportional to 105 (ratio from 861:138)

    if os.path.isfile(SIG_LIGHT_PATH):
        try:
            c.drawImage(ImageReader(SIG_LIGHT_PATH), sig_x, 118,
                        width=sig_w, height=sig_h, mask="auto",
                        preserveAspectRatio=True)
        except Exception as e:
            print("Sig error:", e)

    # Gold accent underline below signature
    c.setStrokeColor(colors.HexColor("#D4AF37"))
    c.setLineWidth(0.5)
    c.line(sig_x, 114, sig_x + sig_w, 114)

    c.setFillColor(colors.white)
    c.setFont(FONT_CERT_SERIF_BOLD, 11.5)
    c.drawString(sig_x, 100, SIGNATORY_NAME)

    c.setFont(FONT_CERT_SERIF, 9)
    c.setFillColor(colors.HexColor("#94A3B8"))
    c.drawString(sig_x, 88, SIGNATORY_TITLE)

    c.setFont(FONT_CERT_SERIF_BOLD, 8.5)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(sig_x, 76, SIGNATORY_ORG)

    # Change 8: Centered credential ID block with spacious bottom clearance
    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.setFont(FONT_CERT_SERIF_BOLD, 8.5)
    c.drawCentredString(320, 110, f"Certificate ID: {c_data['cert_id']}")

    c.setFillColor(colors.HexColor("#94A3B8"))
    c.setFont(FONT_CERT_SERIF, 8)
    c.drawCentredString(320, 96, f"Intern ID: {c_data['intern_id']}")

    c.setFillColor(colors.HexColor("#D4AF37"))
    c.setFont(FONT_CERT_SERIF_BOLD, 9)
    c.drawCentredString(320, 82, "DBERT \u00b7 dbert.in")

    # Change 9: QR Code aligned to background placeholder
    verify_url = f"https://dbert.in/verify?certid={c_data['cert_id']}"
    qr_buf = generate_qr_buffer(verify_url)
    c.drawImage(ImageReader(qr_buf), 553, 64, width=52, height=52)

    # Change 10: Redundant footer lines removed — credential block above replaces them

    c.showPage()
    c.save()


# ======================================================================================
# DOCUMENT 2: ACADEMIC PROJECT EVALUATION CERTIFICATE (Portrait Letter)
# Subtitle Under DBERT, Uniform Metadata Typography (No Wrapping), Single Signature,
# Harmonious Vertical Spacing
# ======================================================================================
def draw_cert_evaluation(target_stream, c_data):
    c = canvas.Canvas(target_stream, pagesize=letter)
    c.setTitle(f"Academic Project Evaluation & Technical Appraisal — {c_data['name']} [{c_data['cert_id']}]")
    c.setAuthor("Digital Blinc Education Research and Technology (DBERT)")
    c.setSubject(f"Comprehensive 9-Dimension Technical & Project Rubric Assessment — Score {c_data.get('score', 84)}/100 ({c_data.get('grade', 'Grade: A')})")
    c.setKeywords(f"DBERT, Academic Evaluation, Performance Appraisal, Rubrics, Turnitin Validated, {c_data['cert_id']}, {c_data['intern_id']}, {c_data['name']}, {c_data.get('project', '')}")
    c.setCreator("DBERT Academic Evaluation & Competency Scoring System v2026.2")
    width, height = letter

    # Double Border
    c.setStrokeColor(colors.HexColor("#0F2942"))
    c.setLineWidth(2)
    c.rect(25, 25, width - 50, height - 50)

    c.setStrokeColor(colors.HexColor("#D4AF37"))
    c.setLineWidth(0.8)
    c.rect(28, 28, width - 56, height - 56)

    # Header with (Digital Blinc Education Research and Technology) & No MSME
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#0F2942"))
    c.drawCentredString(width / 2.0, height - 54, "DBERT")

    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor("#4A5568"))
    c.drawCentredString(width / 2.0, height - 68, ORG_FULL_NAME)

    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(colors.HexColor("#D4AF37"))
    c.drawCentredString(width / 2.0, height - 83, "ACADEMIC PROJECT EVALUATION & COMPETENCY RUBRICS")

    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#718096"))
    c.drawCentredString(width / 2.0, height - 95, "Official Verification Portal: dbert.in/verify")

    c.setStrokeColor(colors.HexColor("#CBD5E0"))
    c.setLineWidth(0.75)
    c.line(40, height - 102, width - 40, height - 102)

    # Candidate Meta Box (Strictly Uniform Typography: Helvetica-Bold 8pt labels, Helvetica 8pt values)
    # Guaranteed zero line-wrapping via defensive fitted string logic
    box_y = height - 188
    box_h = 76
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.rect(40, box_y, width - 80, box_h, fill=True, stroke=False)
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.rect(40, box_y, width - 80, box_h, fill=False, stroke=True)

    left_x = 52
    val_x = 122
    col2_x = 338
    col2_val_x = 418
    line_sp = 14.5
    f_sz = 8.0
    label_col = colors.HexColor("#1A202C")
    val_col = colors.HexColor("#334155")

    # Row 1: Intern Name | Certificate ID
    c.setFont("Helvetica-Bold", f_sz)
    c.setFillColor(label_col)
    c.drawString(left_x, box_y + box_h - 15, "Intern Name:")
    draw_fitted_string(c, val_x, box_y + box_h - 15, c_data["name"], "Helvetica", f_sz, 210, val_col)

    c.setFont("Helvetica-Bold", f_sz)
    c.setFillColor(label_col)
    c.drawString(col2_x, box_y + box_h - 15, "Certificate ID:")
    draw_fitted_string(c, col2_val_x, box_y + box_h - 15, c_data["cert_id"], "Helvetica", f_sz, 145, val_col)

    # Row 2: College / Inst | Intern ID
    c.setFont("Helvetica-Bold", f_sz)
    c.setFillColor(label_col)
    c.drawString(left_x, box_y + box_h - 15 - line_sp, "College / Inst:")
    draw_fitted_string(c, val_x, box_y + box_h - 15 - line_sp, c_data["college"], "Helvetica", f_sz, 210, val_col)

    c.setFont("Helvetica-Bold", f_sz)
    c.setFillColor(label_col)
    c.drawString(col2_x, box_y + box_h - 15 - line_sp, "Intern ID:")
    draw_fitted_string(c, col2_val_x, box_y + box_h - 15 - line_sp, c_data["intern_id"], "Helvetica", f_sz, 145, val_col)

    # Row 3: Domain Track | Tenure
    c.setFont("Helvetica-Bold", f_sz)
    c.setFillColor(label_col)
    c.drawString(left_x, box_y + box_h - 15 - line_sp * 2, "Domain Track:")
    draw_fitted_string(c, val_x, box_y + box_h - 15 - line_sp * 2, c_data["domain"], "Helvetica", f_sz, 210, val_col)

    c.setFont("Helvetica-Bold", f_sz)
    c.setFillColor(label_col)
    c.drawString(col2_x, box_y + box_h - 15 - line_sp * 2, "Tenure:")
    draw_fitted_string(c, col2_val_x, box_y + box_h - 15 - line_sp * 2, c_data["duration"], "Helvetica", f_sz, 145, val_col)

    # Row 4: Project Title | Evaluation Date
    c.setFont("Helvetica-Bold", f_sz)
    c.setFillColor(label_col)
    c.drawString(left_x, box_y + box_h - 15 - line_sp * 3, "Project Title:")
    draw_fitted_string(c, val_x, box_y + box_h - 15 - line_sp * 3, c_data["project"], "Helvetica", f_sz, 210, val_col)

    c.setFont("Helvetica-Bold", f_sz)
    c.setFillColor(label_col)
    c.drawString(col2_x, box_y + box_h - 15 - line_sp * 3, "Evaluation Date:")
    draw_fitted_string(c, col2_val_x, box_y + box_h - 15 - line_sp * 3, c_data["eval_date"], "Helvetica", f_sz, 145, val_col)

    # Rubric Table Header
    table_y = box_y - 20
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor("#0F2942"))
    c.drawString(40, table_y, "PERFORMANCE ASSESSMENT RUBRIC (100 MARKS TOTAL)")

    table_top = table_y - 8
    row_h = 23
    col_w = [24, 196, 205, 45, 62]

    c.setFillColor(colors.HexColor("#0F2942"))
    c.rect(40, table_top - row_h, width - 80, row_h, fill=True, stroke=False)

    c.setFont("Helvetica-Bold", 7.8)
    c.setFillColor(colors.white)
    headers = [
        (45, "#"),
        (69, "Evaluation Parameter"),
        (265, "Assessment Criteria"),
        (474, "Max"),
        (522, "Scored")
    ]
    for x_pos, h_text in headers:
        c.drawString(x_pos, table_top - 15, h_text)

    # Rubrics Data (11 rows total with row_h = 23 -> 253 pt)
    rubrics = [
        ("1", "Technical Architecture & System Design", "Modular structuring, schema design, and clean separation", "20", str(c_data["rubric_marks"][0])),
        ("2", "Code Quality & PEP 8 / Clean Code", "Readability, documentation, docstrings, and robust error handling", "10", str(c_data["rubric_marks"][1])),
        ("3", "Core Algorithms & Implementation", "Effective application of domain-specific logic, libraries, and APIs", "10", str(c_data["rubric_marks"][2])),
        ("4", "Data Integrity, Security & Validation", "Defensive programming, boundary tests, and data security", "10", str(c_data["rubric_marks"][3])),
        ("5", "Testing & Verification Coverage", "Unit assertions, edge test case execution, and debugging proficiency", "10", str(c_data["rubric_marks"][4])),
        ("6", "Project Documentation & Deliverables", "Architecture reports, sprint tracking, and README write-ups", "10", str(c_data["rubric_marks"][5])),
        ("7", "Problem Solving & Analytical Agility", "Autonomous reasoning, obstacle resolution, and initiative", "10", str(c_data["rubric_marks"][6])),
        ("8", "Sprint Cadence & Delivery Rigor", "Punctual milestone completions and commit hygiene", "10", str(c_data["rubric_marks"][7])),
        ("9", "Code Review & Technical Viva", "Defense of architectural decisions and system comprehension", "10", str(c_data["rubric_marks"][8]))
    ]

    cur_y = table_top - row_h
    c.setFont("Helvetica", 7.8)
    for r_idx, r in enumerate(rubrics):
        cur_y -= row_h
        bg_col = colors.HexColor("#F8FAFC") if r_idx % 2 == 1 else colors.white
        c.setFillColor(bg_col)
        c.rect(40, cur_y, width - 80, row_h, fill=True, stroke=False)
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.line(40, cur_y, width - 40, cur_y)

        c.setFillColor(colors.HexColor("#1A202C"))
        c.setFont("Helvetica", 7.8)
        c.drawString(45, cur_y + 8, r[0])
        c.drawString(69, cur_y + 8, r[1])
        draw_fitted_string(c, 265, cur_y + 8, r[2], "Helvetica-Oblique", 7.2, 195, colors.HexColor("#4A5568"))
        c.setFont("Helvetica", 7.8)
        c.setFillColor(colors.HexColor("#1A202C"))
        c.drawString(476, cur_y + 8, r[3])
        c.setFont("Helvetica-Bold", 7.8)
        c.setFillColor(colors.HexColor("#0F2942"))
        c.drawString(526, cur_y + 8, r[4])

    # Total Row
    cur_y -= row_h
    c.setFillColor(colors.HexColor("#EDF2F7"))
    c.rect(40, cur_y, width - 80, row_h, fill=True, stroke=False)
    c.setStrokeColor(colors.HexColor("#CBD5E0"))
    c.line(40, cur_y, width - 40, cur_y)
    c.line(40, cur_y + row_h, width - 40, cur_y + row_h)

    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#0F2942"))
    c.drawString(69, cur_y + 8, "AGGREGATE FINAL SCORE")
    c.drawString(474, cur_y + 8, "100")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(520, cur_y + 8, f"{c_data['score']}/100")

    # Grade & Plagiarism Box
    summary_y = cur_y - 44
    c.setFillColor(colors.HexColor("#F0FDF4"))
    c.rect(40, summary_y, width - 80, 36, fill=True, stroke=False)
    c.setStrokeColor(colors.HexColor("#86EFAC"))
    c.rect(40, summary_y, width - 80, 36, fill=False, stroke=True)

    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor("#166534"))
    c.drawString(50, summary_y + 21, f"Final Academic Evaluation: {c_data['grade']}")
    c.setFont("Helvetica", 7.8)
    c.setFillColor(colors.HexColor("#15803D"))
    c.drawString(50, summary_y + 9, "Project Plagiarism Authenticity: Turnitin Originality Score Passed (< 5% similarity threshold). Dual verified on portal.")

    # Single Signature, Turnitin Academic Stamp & QR Section (Harmoniously spaced)
    footer_zone_y = summary_y - 82

    # 1. Verification QR Code Block (Left)
    verify_url = f"https://dbert.in/verify?certid={c_data['cert_id']}"
    qr_buf = generate_qr_buffer(verify_url, box_size=6, border=1)
    c.drawImage(ImageReader(qr_buf), 45, footer_zone_y + 6, width=48, height=48)

    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#0F2942"))
    c.drawString(98, footer_zone_y + 44, "Scan to Verify Credential")
    c.setFont("Helvetica", 7.2)
    c.setFillColor(colors.HexColor("#4A5568"))
    c.drawString(98, footer_zone_y + 33, f"ID: {c_data['cert_id']}")
    c.drawString(98, footer_zone_y + 22, "Portal: dbert.in/verify")
    c.drawString(98, footer_zone_y + 11, "Tamper-Proof Verification")

    # 2. Academic Plagiarism Clearance Seal (Center)
    if os.path.isfile(PLAGIARISM_STAMP_PATH):
        try:
            c.drawImage(ImageReader(PLAGIARISM_STAMP_PATH), 255, footer_zone_y + 8, width=1.40 * inch, height=0.56 * inch, mask="auto")
        except Exception as e:
            print("Plagiarism stamp error Doc 2:", e)

    # 3. Single Official Signatory Right Block
    sig_x = width - 165
    sig_w = 88
    sig_h = 14.1

    if os.path.isfile(SIG_DARK_PATH):
        try:
            c.drawImage(ImageReader(SIG_DARK_PATH), sig_x, footer_zone_y + 36, width=sig_w, height=sig_h, mask="auto", preserveAspectRatio=True)
        except Exception as e:
            print("Sig dark error:", e)

    c.setStrokeColor(colors.HexColor("#CBD5E0"))
    c.setLineWidth(0.75)
    c.line(sig_x, footer_zone_y + 31, sig_x + 115, footer_zone_y + 31)

    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor("#0F2942"))
    c.drawString(sig_x, footer_zone_y + 20, SIGNATORY_NAME)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#4A5568"))
    c.drawString(sig_x, footer_zone_y + 10, SIGNATORY_TITLE)
    c.drawString(sig_x, footer_zone_y, SIGNATORY_ORG)

    # Bottom Legal Footer Lines
    c.setFont("Helvetica", 7.2)
    c.setFillColor(colors.HexColor("#718096"))
    c.drawCentredString(width / 2.0, 48, "This is an official verified academic credential issued by DBERT.")
    c.drawCentredString(width / 2.0, 38, f"Authenticity can be verified at https://dbert.in/verify?certid={c_data['cert_id']}")

    c.showPage()
    c.save()


# ======================================================================================
# DOCUMENT 3: LETTER OF RECOMMENDATION (Portrait Letter)
# Subtitle Under DBERT, 2-Month Program Appraisal, Single Signature, Full Project Name,
# Harmonious Executive Vertical Proportions
# ======================================================================================
def draw_cert_lor(target_stream, c_data):
    c = canvas.Canvas(target_stream, pagesize=letter)
    c.setTitle(f"Official Letter of Recommendation & Performance Appraisal — {c_data['name']} [{c_data['cert_id']}]")
    c.setAuthor("Mr. Abhinav Sharma, Program Head & Project Mentor, DBERT")
    c.setSubject(f"Institutional Letter of Recommendation & Industry Endorsement for {c_data['name']} ({c_data['domain']})")
    c.setKeywords(f"DBERT, Letter of Recommendation, LOR, Performance Appraisal, Abhinav Sharma, {c_data['cert_id']}, {c_data['intern_id']}, {c_data['name']}, {c_data.get('project', '')}")
    c.setCreator("DBERT Institutional Endorsement & Appraisal Engine v2026.2")
    width, height = letter

    # Double Border
    c.setStrokeColor(colors.HexColor("#0F2942"))
    c.setLineWidth(1.5)
    c.rect(30, 30, width - 60, height - 60)

    c.setStrokeColor(colors.HexColor("#D4AF37"))
    c.setLineWidth(0.75)
    c.rect(33, 33, width - 66, height - 66)

    # Institutional Header with (Digital Blinc Education Research and Technology) & No MSME
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor("#0F2942"))
    c.drawCentredString(width / 2.0, height - 58, "DBERT")

    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor("#4A5568"))
    c.drawCentredString(width / 2.0, height - 72, ORG_FULL_NAME)

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#D4AF37"))
    c.drawCentredString(width / 2.0, height - 87, "OFFICIAL LETTER OF RECOMMENDATION & PERFORMANCE APPRAISAL")

    c.setFont("Helvetica", 7.5)
    c.setFillColor(colors.HexColor("#718096"))
    c.drawCentredString(width / 2.0, height - 99, "Official Verification Portal: dbert.in/verify")

    c.setStrokeColor(colors.HexColor("#CBD5E0"))
    c.setLineWidth(0.75)
    c.line(45, height - 106, width - 45, height - 106)

    # Date & Ref
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor("#2D3748"))
    c.drawString(50, height - 124, f"Date: {c_data['eval_date']}")
    c.drawRightString(width - 50, height - 124, f"Ref: LOR-DBERT-{c_data['cert_id']}")

    c.setFont("Helvetica-Bold", 10.5)
    c.setFillColor(colors.HexColor("#0F2942"))
    c.drawString(50, height - 146, "TO WHOMSOEVER IT MAY CONCERN")

    # Helper for justified paragraphs
    def draw_justified_para(text, start_y, font_size=9.8, lead=15.5):
        c.setFont("Helvetica", font_size)
        c.setFillColor(colors.HexColor("#2D3748"))
        words = text.split()
        cur_line = []
        cur_y = start_y
        max_w = width - 100

        for w in words:
            test_line = " ".join(cur_line + [w])
            if c.stringWidth(test_line, "Helvetica", font_size) <= max_w:
                cur_line.append(w)
            else:
                c.drawString(50, cur_y, " ".join(cur_line))
                cur_y -= lead
                cur_line = [w]
        if cur_line:
            c.drawString(50, cur_y, " ".join(cur_line))
            cur_y -= lead
        return cur_y

    body_y = height - 170

    # Paragraph 1: Explicit 2-Month Program Phrasing
    p1 = (
        f"I am pleased to write this formal Letter of Recommendation for {c_data['name']}, student of "
        f"{c_data['college']}, who successfully completed a rigorous 2-month Internship & Incubation "
        f"Program with DBERT as a {c_data['domain']} from {c_data['start_date']} to {c_data['end_date']}."
    )
    body_y = draw_justified_para(p1, body_y)
    body_y -= 10

    p2 = (
        f"During the internship, {c_data['name']} contributed significantly to the core engineering project: "
        f"\"{c_data['project']}\". The candidate demonstrated exceptional technical proficiency, systematic problem-solving, "
        f"and code quality. Their responsibilities included end-to-end milestone implementations, architectural debugging, "
        f"and collaborative project delivery meeting strict industry standards."
    )
    body_y = draw_justified_para(p2, body_y)
    body_y -= 10

    p3 = (
        f"In our formal project evaluation, {c_data['name']} achieved an outstanding aggregate score of "
        f"{c_data['score']}/100 ({c_data['grade']}), reflecting exemplary analytical discipline, creative initiative, and "
        f"technical maturity. Their work underwent rigorous code review, automated testing, and Turnitin plagiarism validation "
        f"(sub-5% threshold), passing with distinction."
    )
    body_y = draw_justified_para(p3, body_y)
    body_y -= 10

    p4 = (
        f"{c_data['name']} showed outstanding diligence, intellectual curiosity, and high collaborative ethics throughout the "
        f"incubation sprint. I am confident that they possess the skills, work ethic, and adaptability required to excel in any "
        f"challenging production or research environment. I give them my highest recommendation for future academic pursuits and "
        f"professional engineering roles."
    )
    body_y = draw_justified_para(p4, body_y)

    # Candidate Summary Box (Dynamic placement right below body)
    box_y = body_y - 72
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.rect(50, box_y, width - 100, 56, fill=True, stroke=False)
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.rect(50, box_y, width - 100, 56, fill=False, stroke=True)

    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(colors.HexColor("#0F2942"))
    c.drawString(60, box_y + 40, "Candidate Credential Summary:")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(60, box_y + 25, f"Intern ID: {c_data['intern_id']}  ·  Certificate ID: {c_data['cert_id']}")
    # Full project name cleanly displayed
    draw_fitted_string(c, 60, box_y + 11, f"Track: {c_data['domain']}  ·  Project: {c_data['project']}", "Helvetica", 8, width - 120, colors.HexColor("#334155"))

    # ==================================================================================
    # SINGLE SIGNATURE & VERIFICATION QR CODE SECTION
    # (Dual signature eliminated: No redundant digital institutional stamp)
    # ==================================================================================
    footer_zone_y = box_y - 88

    # 1. Verification QR Code Block (Left)
    verify_url = f"https://dbert.in/verify?certid={c_data['cert_id']}"
    qr_buf = generate_qr_buffer(verify_url, box_size=6, border=1)
    c.drawImage(ImageReader(qr_buf), 52, footer_zone_y + 6, width=48, height=48)

    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#0F2942"))
    c.drawString(106, footer_zone_y + 44, "Scan to Verify Credential")
    c.setFont("Helvetica", 7.2)
    c.setFillColor(colors.HexColor("#4A5568"))
    c.drawString(106, footer_zone_y + 33, f"Ref: LOR-DBERT-{c_data['cert_id']}")
    c.drawString(106, footer_zone_y + 22, "Portal: dbert.in/verify")
    c.drawString(106, footer_zone_y + 11, "Tamper-Proof Verification")

    # 2. Single Official Signatory Block (Right)
    sig_x = width - 165
    sig_w = 88
    sig_h = 14.1

    if os.path.isfile(SIG_DARK_PATH):
        try:
            c.drawImage(ImageReader(SIG_DARK_PATH), sig_x, footer_zone_y + 36, width=sig_w, height=sig_h, mask="auto", preserveAspectRatio=True)
        except Exception as e:
            print("Sig dark error:", e)

    c.setStrokeColor(colors.HexColor("#CBD5E0"))
    c.setLineWidth(0.75)
    c.line(sig_x, footer_zone_y + 31, sig_x + 115, footer_zone_y + 31)

    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor("#0F2942"))
    c.drawString(sig_x, footer_zone_y + 20, SIGNATORY_NAME)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#4A5568"))
    c.drawString(sig_x, footer_zone_y + 10, SIGNATORY_TITLE)
    c.drawString(sig_x, footer_zone_y, SIGNATORY_ORG)

    # Bottom Legal Footer Lines (Inside inner border, zero MSME)
    c.setFont("Helvetica", 7.2)
    c.setFillColor(colors.HexColor("#718096"))
    c.drawCentredString(width / 2.0, 54, "Official Letter of Recommendation issued by DBERT.")
    c.drawCentredString(width / 2.0, 44, f"Authenticity can be verified at https://dbert.in/verify?certid={c_data['cert_id']}")

    c.showPage()
    c.save()


# Run Generation for Kushal Agarwal if executed directly
if __name__ == "__main__":
    doc1_target = os.path.join(OUTPUT_DIR, "1_Certificate_of_Completion_CERT-DBERT-2026-DA-001.pdf")
    doc2_target = os.path.join(OUTPUT_DIR, "2_Academic_Project_Evaluation_CERT-DBERT-2026-DA-001.pdf")
    doc3_target = os.path.join(OUTPUT_DIR, "3_Letter_of_Recommendation_CERT-DBERT-2026-DA-001.pdf")

    print("Generating Document 1: Certificate of Completion...")
    doc1_final = safe_save_canvas(None, doc1_target, draw_cert_completion, C_DATA)

    print("Generating Document 2: Academic Project Evaluation...")
    doc2_final = safe_save_canvas(None, doc2_target, draw_cert_evaluation, C_DATA)

    print("Generating Document 3: Letter of Recommendation...")
    doc3_final = safe_save_canvas(None, doc3_target, draw_cert_lor, C_DATA)

    print(f"\nSample Packet Generation Complete!\n  Doc 1: {doc1_final}\n  Doc 2: {doc2_final}\n  Doc 3: {doc3_final}")
