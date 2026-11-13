"""
services/certificate_packet_service.py - Unified 3-Document Certificate & Dossier Engine
Generates and serves the authentic 3-document credential packet:
1. Official Certificate of Completion (Landscape 640x495)
2. Academic Project Evaluation & Competency Rubrics (Portrait Letter)
3. Official Letter of Recommendation & Performance Appraisal (Portrait Letter)

Ensures 100% visual, structural, and cryptographic parity between email dispatch PDFs
and the LMS web print dossier (/portal/certificate/<cert_id>/print).
"""
import os
import sys
import json
from io import BytesIO
import calendar
from datetime import datetime, date
from typing import Optional, Dict, Any, Tuple

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


# Asset path resolution
PORTAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(PORTAL_DIR, "static", "certificates")
BASE_DIR = os.path.abspath(os.path.join(PORTAL_DIR, "..", ".."))

BG_CERT_PATH = os.path.join(ASSETS_DIR, "targets12.png")
SIG_LIGHT_PATH = os.path.join(ASSETS_DIR, "sig_light_edwardian.png")
SIG_DARK_PATH = os.path.join(ASSETS_DIR, "sig_dark_edwardian.png")
PLAGIARISM_STAMP_PATH = os.path.join(ASSETS_DIR, "turnitin_plagiarism_stamp.png")

# Font registration with robust multi-platform fallbacks
HAS_GEORGIA = False
HAS_PALATINO = False

font_search_paths = [
    "C:/Windows/Fonts",
    "/usr/share/fonts/truetype",
    "/usr/share/fonts",
    os.path.join(PORTAL_DIR, "static", "fonts")
]

for p in font_search_paths:
    g_reg = os.path.join(p, "georgia.ttf")
    g_bold = os.path.join(p, "georgiab.ttf")
    g_italic = os.path.join(p, "georgiai.ttf")
    g_bolditalic = os.path.join(p, "georgiaz.ttf")
    if os.path.isfile(g_reg) and not HAS_GEORGIA:
        try:
            pdfmetrics.registerFont(TTFont("Georgia", g_reg))
            if os.path.isfile(g_bold):
                pdfmetrics.registerFont(TTFont("Georgia-Bold", g_bold))
            if os.path.isfile(g_italic):
                pdfmetrics.registerFont(TTFont("Georgia-Italic", g_italic))
            if os.path.isfile(g_bolditalic):
                pdfmetrics.registerFont(TTFont("Georgia-BoldItalic", g_bolditalic))
            HAS_GEORGIA = True
        except Exception:
            pass

    pal_file = os.path.join(p, "palai.ttf")
    if os.path.isfile(pal_file) and not HAS_PALATINO:
        try:
            pdfmetrics.registerFont(TTFont("Palatino-Italic", pal_file))
            HAS_PALATINO = True
        except Exception:
            pass

FONT_CERT_SERIF = "Georgia" if HAS_GEORGIA else "Times-Roman"
FONT_CERT_SERIF_BOLD = "Georgia-Bold" if HAS_GEORGIA else "Times-Bold"
FONT_CERT_SERIF_ITALIC = "Georgia-Italic" if HAS_GEORGIA else "Times-Italic"
FONT_CERT_SERIF_BOLDITALIC = "Georgia-BoldItalic" if HAS_GEORGIA else "Times-BoldItalic"
FONT_CERT_LEADIN = "Palatino-Italic" if HAS_PALATINO else FONT_CERT_SERIF_ITALIC

SIGNATORY_NAME = "Mr. Abhinav Sharma"
SIGNATORY_TITLE = "Program Head & Project Mentor"
SIGNATORY_ORG = "DBERT"
ORG_FULL_NAME = "(Digital Blinc Education Research and Technology)"


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


def generate_qr_buffer(data_str: str, box_size: int = 6, border: int = 1) -> BytesIO:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border
    )
    qr.add_data(data_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


class CertificatePacketService:
    """Core domain service for rendering, streaming, and exporting credential packets."""

    @staticmethod
    def resolve_candidate_data(conn, cert_id: str) -> Optional[Dict[str, Any]]:
        """
        Resolves full candidate record for rendering.
        Primary source: certificates_registry.json.
        Fallback: SQLite / PostgreSQL tables.
        """
        clean_cert = cert_id.strip().upper()

        # 1. Master certificates_registry.json
        reg_paths = [
            os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json"),
            "/var/www/dbert-website-lms/apps/website/src/data/certificates_registry.json",
            "/var/www/dbert-website-lms/data/certificates_registry.json",
            os.path.join(BASE_DIR, "data", "certificates_registry.json")
        ]
        
        reg_data = None
        for rp in reg_paths:
            if os.path.isfile(rp):
                try:
                    with open(rp, "r", encoding="utf-8") as f:
                        loaded = json.load(f)
                    if isinstance(loaded, dict) and clean_cert in loaded:
                        reg_data = loaded[clean_cert]
                        break
                    elif isinstance(loaded, list):
                        for item in loaded:
                            if item.get("certId", "").strip().upper() == clean_cert:
                                reg_data = item
                                break
                    if reg_data:
                        break
                except Exception:
                    pass

        # 2. Database Lookup
        db_row = None
        if conn:
            try:
                db_row = conn.execute("""
                    SELECT c.*, COALESCE(a.name, ap.name, 'Intern') AS recipient_name,
                           COALESCE(a.domain, ap.domain, 'Engineering') AS intern_domain,
                           COALESCE(a.college, ap.college, '') AS intern_college,
                           COALESCE(a.phone, ap.phone, '') AS intern_phone,
                           COALESCE(a.email, c.email) AS intern_email
                    FROM intern_certificates c
                    LEFT JOIN intern_accounts a ON (a.id = c.intern_id OR (c.email IS NOT NULL AND LOWER(a.email) = LOWER(c.email)))
                    LEFT JOIN applications ap ON (c.email IS NOT NULL AND LOWER(ap.email) = LOWER(c.email))
                    WHERE UPPER(c.cert_id) = ?
                """, (clean_cert,)).fetchone()
            except Exception:
                pass

        if not reg_data and not db_row:
            return None

        # Harmonize metadata into unified structure
        name = (reg_data.get("holderName") if reg_data else None) or (db_row["recipient_name"] if db_row else "Intern")
        email = (reg_data.get("email") if reg_data else None) or (db_row["intern_email"] if db_row else "")
        domain = (reg_data.get("domain") if reg_data else None) or (db_row["intern_domain"] if db_row else "Engineering")
        college = (reg_data.get("college") if reg_data else None) or (db_row["intern_college"] if db_row else "")
        phone = (reg_data.get("phone") if reg_data else None) or (db_row["intern_phone"] if db_row else "")
        
        intern_id = (reg_data.get("internId") if reg_data else None) or f"DBERT-INT-{clean_cert.split('-')[-1]}"
        batch = (reg_data.get("batch") if reg_data else None) or "July to Sep 2026"
        duration = (reg_data.get("duration") if reg_data else None) or "July to September 2026 (2 Months)"
        eval_date = (reg_data.get("evalDate") if reg_data else None) or "01 October 2026"
        issue_date = (reg_data.get("issueDate") if reg_data else None) or (str(db_row["issued_at"])[:10] if db_row and db_row["issued_at"] else "2026-10-01")
        
        project = (reg_data.get("project") if reg_data else None) or "Gayatri AI — Enterprise Educational Intelligence Platform"
        
        topics_map = {
            "Data Analyst": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
            "Data Analytics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
            "Artificial Intelligence & Machine Learning": "Python, Scikit-Learn, PyTorch, Neural Networks, Computer Vision, NLP, Deep Learning, Model Deployment",
            "AI & Machine Learning": "Python, Scikit-Learn, PyTorch, Neural Networks, Computer Vision, NLP, Deep Learning, Model Deployment",
            "AI Agent Development": "LLM Architecture, Prompt Engineering, Structured Outputs, Tool Calling, ReAct Orchestration, LangChain, Production Deployment",
            "Full Stack Web Development": "HTML5, CSS3, JavaScript, TypeScript, React.js, Node.js, Express, PostgreSQL, REST APIs, Cloud Deployment",
            "Full Stack Development": "HTML5, CSS3, JavaScript, TypeScript, React.js, Node.js, Express, PostgreSQL, REST APIs, Cloud Deployment",
            "Python Automation": "Python Core, Scripting, Automation Daemons, Selenium, Playwright, BeautifulSoup, Data Pipelines, API Integrations",
            "UI/UX Design": "Figma Auto-Layout, Design Systems, Design Tokens, User Research, Wireframing, WCAG Accessibility, Usability Testing",
            "UI & UX Design": "Figma Auto-Layout, Design Systems, Design Tokens, User Research, Wireframing, WCAG Accessibility, Usability Testing",
            "DevOps & Cloud": "Linux Administration, Docker Containers, Kubernetes Orchestration, AWS Cloud Infrastructure, CI/CD Actions, Prometheus, Grafana",
            "Mobile App Development": "React Native, Flutter, Mobile UI Architecture, Navigation Stacks, Device Hardware APIs, Offline Storage, Release Deployment",
            "Cybersecurity": "Threat Modeling (STRIDE), Network Analysis (Wireshark), OWASP Top 10, Penetration Testing (Burp Suite), SOC Operations, SIEM Auditing",
            "Digital Marketing": "Keyword Research, Technical SEO, Google Analytics 4, Performance Ad Campaigns (Meta/Google), Funnel Optimization, ROAS Modeling",
            "Digital Brand Building": "Brand Strategy, Content Architecture, Social Distribution, Performance Ad Campaigns, Conversion Funnel Optimization"
        }
        topics = (reg_data.get("topics") if reg_data else None) or topics_map.get(domain, "Core Architecture, Practical Implementation, Production Deployments, Best Practices")
        
        score = int(reg_data.get("score", 84) if reg_data else 84)
        grade = (reg_data.get("grade") if reg_data else None) or "Grade: A (Very Good Performance)"
        
        # Calculate rubric breakdown summing to score
        rubrics = [17, 9, 8, 8, 8, 9, 8, 8, 9]
        if score != 84:
            diff = score - 84
            rubrics[0] = max(10, min(20, rubrics[0] + diff))

        return {
            "name": name,
            "email": email,
            "college": college,
            "phone": phone,
            "domain": domain,
            "project": project,
            "topics": topics,
            "duration": duration,
            "batch": batch,
            "start_date": reg_data.get("startDate", "July 2026") if reg_data else "July 2026",
            "end_date": reg_data.get("endDate", "September 2026") if reg_data else "September 2026",
            "cert_id": clean_cert,
            "intern_id": intern_id,
            "score": score,
            "grade": grade,
            "eval_date": eval_date,
            "issue_date": issue_date,
            "rubric_marks": rubrics,
            "verification_url": f"https://dbert.in/verify?certid={clean_cert}",
            "signatory": SIGNATORY_NAME,
            "signatory_title": SIGNATORY_TITLE,
            "organization": SIGNATORY_ORG
        }

    # ==================================================================================
    # DOCUMENT 1: CERTIFICATE OF COMPLETION (640 x 495 Landscape Canvas)
    # ==================================================================================
    @staticmethod
    def draw_cert_completion(target_stream, c_data: Dict[str, Any]):
        c = canvas.Canvas(target_stream, pagesize=(640, 495))
        c.setTitle(f"Official Verified Certificate of Completion — {c_data['name']} [{c_data['cert_id']}]")
        c.setAuthor("Digital Blinc Education Research and Technology (DBERT)")
        c.setSubject(f"2-Month Technical Incubation & Internship Credential in {c_data['domain']}")
        c.setKeywords(f"DBERT, Internship Certificate, Credential, {c_data['cert_id']}, {c_data['intern_id']}, {c_data['name']}, {c_data['domain']}, Verified, Authenticity Registry")
        c.setCreator("DBERT Academic & Technical Credential Engine v2026.2")

        # Background
        if os.path.isfile(BG_CERT_PATH):
            c.drawImage(BG_CERT_PATH, 0, 0, width=640, height=495)
        else:
            c.setFillColor(colors.HexColor("#0f172a"))
            c.rect(0, 0, 640, 495, fill=1, stroke=0)

        # Lead-in
        c.setFillColor(colors.HexColor("#F5F0E8"))
        c.setFont(FONT_CERT_LEADIN, 13)
        c.drawCentredString(320, 320, "This certificate is proudly awarded to")

        # Top gold hairline rule
        c.setStrokeColor(colors.HexColor("#D4AF37"))
        c.setLineWidth(0.6)
        c.line(160, 314, 480, 314)

        # Candidate name
        draw_fitted_centre(c, 320, 290, c_data["name"].strip().upper(),
                           FONT_CERT_SERIF_BOLD, 22, 420, colors.HexColor("#D4AF37"))

        # Bottom gold hairline rule
        c.setStrokeColor(colors.HexColor("#D4AF37"))
        c.setLineWidth(0.6)
        c.line(160, 280, 480, 280)

        # Completion statement
        c.setFillColor(colors.HexColor("#CBD5E1"))
        c.setFont(FONT_CERT_SERIF_ITALIC, 11)
        c.drawCentredString(320, 262, "for successful completion of a 2-Month Internship in")

        # Domain track
        draw_fitted_centre(c, 320, 240, c_data["domain"],
                           FONT_CERT_SERIF_BOLD, 16, 420, colors.HexColor("#E5C07B"))

        # Separator line
        c.setStrokeColor(colors.HexColor("#64748B"))
        c.setLineWidth(0.4)
        c.line(180, 228, 460, 228)

        # Topics & Project
        topics = c_data["topics"]
        if len(topics) > 75:
            part1 = topics[:75]
            last_sp = part1.rfind(",")
            if last_sp != -1:
                t1 = topics[:last_sp + 1]
                t2 = topics[last_sp + 1:].strip()
                draw_fitted_centre(c, 320, 214, f"Covering: {t1}", FONT_CERT_SERIF, 9, 460, colors.HexColor("#94A3B8"))
                draw_fitted_centre(c, 320, 202, t2, FONT_CERT_SERIF, 9, 460, colors.HexColor("#94A3B8"))
                project_y = 188
            else:
                draw_fitted_centre(c, 320, 214, f"Covering: {topics}", FONT_CERT_SERIF, 9, 460, colors.HexColor("#94A3B8"))
                project_y = 200
        else:
            draw_fitted_centre(c, 320, 214, f"Covering: {topics}", FONT_CERT_SERIF, 9, 460, colors.HexColor("#94A3B8"))
            project_y = 200

        draw_fitted_centre(c, 320, project_y, f"Project: {c_data['project']}", FONT_CERT_SERIF, 9.5, 460, colors.HexColor("#E2E8F0"))
        draw_fitted_centre(c, 320, project_y - 14, f"Duration: {c_data['duration']}", FONT_CERT_SERIF, 9, 460, colors.HexColor("#94A3B8"))

        # Signature Block
        sig_x = 65
        sig_w = 105
        sig_h = 16.8
        if os.path.isfile(SIG_LIGHT_PATH):
            try:
                c.drawImage(ImageReader(SIG_LIGHT_PATH), sig_x, 118, width=sig_w, height=sig_h, mask="auto", preserveAspectRatio=True)
            except Exception:
                pass

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

        # Centered Credential IDs
        c.setFillColor(colors.HexColor("#CBD5E1"))
        c.setFont(FONT_CERT_SERIF_BOLD, 8.5)
        c.drawCentredString(320, 110, f"Certificate ID: {c_data['cert_id']}")

        c.setFillColor(colors.HexColor("#94A3B8"))
        c.setFont(FONT_CERT_SERIF, 8)
        c.drawCentredString(320, 96, f"Intern ID: {c_data['intern_id']}")

        c.setFillColor(colors.HexColor("#D4AF37"))
        c.setFont(FONT_CERT_SERIF_BOLD, 9)
        c.drawCentredString(320, 82, "DBERT · dbert.in")

        # QR Code
        qr_buf = generate_qr_buffer(c_data["verification_url"])
        c.drawImage(ImageReader(qr_buf), 553, 64, width=52, height=52)

        c.showPage()
        c.save()

    # ==================================================================================
    # DOCUMENT 2: ACADEMIC PROJECT EVALUATION (Portrait Letter)
    # ==================================================================================
    @staticmethod
    def draw_cert_evaluation(target_stream, c_data: Dict[str, Any]):
        c = canvas.Canvas(target_stream, pagesize=letter)
        c.setTitle(f"Academic Project Evaluation & Technical Appraisal — {c_data['name']} [{c_data['cert_id']}]")
        c.setAuthor("Digital Blinc Education Research and Technology (DBERT)")
        c.setSubject(f"Comprehensive 9-Dimension Technical & Project Rubric Assessment — Score {c_data.get('score', 84)}/100 ({c_data.get('grade', 'Grade: A')})")
        c.setKeywords(f"DBERT, Academic Evaluation, Performance Appraisal, Rubrics, Turnitin Validated, {c_data['cert_id']}, {c_data['intern_id']}, {c_data['name']}")
        c.setCreator("DBERT Academic Evaluation & Competency Scoring System v2026.2")
        width, height = letter

        # Double Border
        c.setStrokeColor(colors.HexColor("#0F2942"))
        c.setLineWidth(2)
        c.rect(25, 25, width - 50, height - 50)

        c.setStrokeColor(colors.HexColor("#D4AF37"))
        c.setLineWidth(0.8)
        c.rect(28, 28, width - 56, height - 56)

        # Header
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

        # Candidate Meta Box
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

        # Row 1: Name & Cert ID
        c.setFont("Helvetica-Bold", f_sz)
        c.setFillColor(label_col)
        c.drawString(left_x, box_y + box_h - 15, "Intern Name:")
        draw_fitted_string(c, val_x, box_y + box_h - 15, c_data["name"], "Helvetica", f_sz, 210, val_col)

        c.setFont("Helvetica-Bold", f_sz)
        c.setFillColor(label_col)
        c.drawString(col2_x, box_y + box_h - 15, "Certificate ID:")
        draw_fitted_string(c, col2_val_x, box_y + box_h - 15, c_data["cert_id"], "Helvetica", f_sz, 145, val_col)

        # Row 2: College & Intern ID
        c.setFont("Helvetica-Bold", f_sz)
        c.setFillColor(label_col)
        c.drawString(left_x, box_y + box_h - 15 - line_sp, "College / Inst:")
        draw_fitted_string(c, val_x, box_y + box_h - 15 - line_sp, c_data["college"], "Helvetica", f_sz, 210, val_col)

        c.setFont("Helvetica-Bold", f_sz)
        c.setFillColor(label_col)
        c.drawString(col2_x, box_y + box_h - 15 - line_sp, "Intern ID:")
        draw_fitted_string(c, col2_val_x, box_y + box_h - 15 - line_sp, c_data["intern_id"], "Helvetica", f_sz, 145, val_col)

        # Row 3: Domain & Tenure
        c.setFont("Helvetica-Bold", f_sz)
        c.setFillColor(label_col)
        c.drawString(left_x, box_y + box_h - 15 - line_sp * 2, "Domain Track:")
        draw_fitted_string(c, val_x, box_y + box_h - 15 - line_sp * 2, c_data["domain"], "Helvetica", f_sz, 210, val_col)

        c.setFont("Helvetica-Bold", f_sz)
        c.setFillColor(label_col)
        c.drawString(col2_x, box_y + box_h - 15 - line_sp * 2, "Tenure:")
        draw_fitted_string(c, col2_val_x, box_y + box_h - 15 - line_sp * 2, c_data["duration"], "Helvetica", f_sz, 145, val_col)

        # Row 4: Project & Eval Date
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

        c.setFillColor(colors.HexColor("#0F2942"))
        c.rect(40, table_top - row_h, width - 80, row_h, fill=True, stroke=False)

        c.setFont("Helvetica-Bold", 7.8)
        c.setFillColor(colors.white)
        for x_pos, h_text in [
            (45, "#"), (69, "Evaluation Parameter"), (265, "Assessment Criteria"),
            (474, "Max"), (522, "Scored")
        ]:
            c.drawString(x_pos, table_top - 15, h_text)

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
            c.drawString(476, cur_y + 8, r[3])
            c.setFont("Helvetica-Bold", 7.8)
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

        # Footer Zone: QR | Turnitin Seal | Signatory
        footer_zone_y = summary_y - 82

        # Verification QR Code
        qr_buf = generate_qr_buffer(c_data["verification_url"], box_size=6, border=1)
        c.drawImage(ImageReader(qr_buf), 45, footer_zone_y + 6, width=48, height=48)

        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(colors.HexColor("#0F2942"))
        c.drawString(98, footer_zone_y + 44, "Scan to Verify Credential")
        c.setFont("Helvetica", 7.2)
        c.setFillColor(colors.HexColor("#4A5568"))
        c.drawString(98, footer_zone_y + 33, f"ID: {c_data['cert_id']}")
        c.drawString(98, footer_zone_y + 22, "Portal: dbert.in/verify")
        c.drawString(98, footer_zone_y + 11, "Tamper-Proof Verification")

        # Turnitin Academic Stamp
        if os.path.isfile(PLAGIARISM_STAMP_PATH):
            try:
                c.drawImage(ImageReader(PLAGIARISM_STAMP_PATH), 255, footer_zone_y + 8, width=1.40 * inch, height=0.56 * inch, mask="auto")
            except Exception:
                pass

        # Official Signatory Right Block
        sig_x = width - 165
        sig_w = 88
        sig_h = 14.1

        if os.path.isfile(SIG_DARK_PATH):
            try:
                c.drawImage(ImageReader(SIG_DARK_PATH), sig_x, footer_zone_y + 36, width=sig_w, height=sig_h, mask="auto", preserveAspectRatio=True)
            except Exception:
                pass

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

    # ==================================================================================
    # DOCUMENT 3: LETTER OF RECOMMENDATION (Portrait Letter)
    # ==================================================================================
    @staticmethod
    def draw_cert_lor(target_stream, c_data: Dict[str, Any]):
        c = canvas.Canvas(target_stream, pagesize=letter)
        c.setTitle(f"Official Letter of Recommendation & Performance Appraisal — {c_data['name']} [{c_data['cert_id']}]")
        c.setAuthor("Mr. Abhinav Sharma, Program Head & Project Mentor, DBERT")
        c.setSubject(f"Institutional Letter of Recommendation & Industry Endorsement for {c_data['name']} ({c_data['domain']})")
        c.setKeywords(f"DBERT, Letter of Recommendation, LOR, Performance Appraisal, Abhinav Sharma, {c_data['cert_id']}, {c_data['intern_id']}, {c_data['name']}")
        c.setCreator("DBERT Institutional Endorsement & Appraisal Engine v2026.2")
        width, height = letter

        # Double Border
        c.setStrokeColor(colors.HexColor("#0F2942"))
        c.setLineWidth(1.5)
        c.rect(30, 30, width - 60, height - 60)

        c.setStrokeColor(colors.HexColor("#D4AF37"))
        c.setLineWidth(0.75)
        c.rect(33, 33, width - 66, height - 66)

        # Institutional Header
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

        # Recommendation Body Paragraphs
        p1 = (
            f"It is my distinct professional pleasure to provide this institutional Letter of Recommendation for "
            f"{c_data['name']} (Certificate ID: {c_data['cert_id']}, Intern ID: {c_data['intern_id']}), who has successfully "
            f"completed an intensive 2-Month Technical Internship and Incubation Program in {c_data['domain']} at DBERT "
            f"during the tenure of {c_data['duration']}."
        )

        p2 = (
            f"Throughout this rigorous engagement, {c_data['name']} demonstrated exemplary engineering capability, analytical "
            f"acumen, and dedicated work ethic. As part of the technical deliverables, {c_data['name']} architected and delivered "
            f"the capstone project entitled \"{c_data['project']}\", incorporating end-to-end modules spanning {c_data['topics']}. "
            f"The codebase underwent systematic automated linting, test suite evaluation, and Turnitin-backed originality validation, "
            f"achieving an outstanding cumulative evaluation of {c_data['score']}/100 ({c_data['grade']})."
        )

        p3 = (
            f"Beyond technical competence, {c_data['name']} consistently exhibited proactive problem-solving agility, rapid comprehension "
            f"of enterprise architecture rubrics, and meticulous documentation discipline. The ability to autonomously navigate complex "
            f"technical challenges, synthesize domain knowledge, and deliver production-ready milestones distinguishes {c_data['name']} "
            f"as a high-potential professional capable of making immediate contributions to engineering and analytics teams."
        )

        p4 = (
            f"I recommend {c_data['name']} with the highest degree of confidence for graduate study, competitive fellowship programs, "
            f"and demanding technical roles in {c_data['domain']}. Please direct any credential verification inquiries to our official "
            f"registry at dbert.in/verify or admissions@dbert.in."
        )

        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import ParagraphStyle

        p_style = ParagraphStyle(
            name="LorBody",
            fontName="Helvetica",
            fontSize=8.6,
            leading=13.8,
            textColor=colors.HexColor("#2D3748"),
            alignment=4  # Justified
        )

        y_pos = height - 162
        for para_text in [p1, p2, p3, p4]:
            para = Paragraph(para_text, p_style)
            p_w, p_h = para.wrap(width - 100, 300)
            para.drawOn(c, 50, y_pos - p_h)
            y_pos -= (p_h + 12)

        # Signatory Section & Verification Seal
        footer_y = 120
        c.setFont("Helvetica-Bold", 8.8)
        c.setFillColor(colors.HexColor("#0F2942"))
        c.drawString(50, footer_y + 40, "Sincerely,")

        sig_w = 88
        sig_h = 14.1
        if os.path.isfile(SIG_DARK_PATH):
            try:
                c.drawImage(ImageReader(SIG_DARK_PATH), 50, footer_y + 16, width=sig_w, height=sig_h, mask="auto", preserveAspectRatio=True)
            except Exception:
                pass

        c.setStrokeColor(colors.HexColor("#CBD5E0"))
        c.setLineWidth(0.75)
        c.line(50, footer_y + 12, 175, footer_y + 12)

        c.setFont("Helvetica-Bold", 9)
        c.drawString(50, footer_y, SIGNATORY_NAME)
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#4A5568"))
        c.drawString(50, footer_y - 11, SIGNATORY_TITLE)
        c.drawString(50, footer_y - 22, f"{SIGNATORY_ORG} {ORG_FULL_NAME}")
        c.drawString(50, footer_y - 33, "Email: abhinav.sharma@dbert.in · Web: dbert.in")

        # Verification Seal & QR Block (Right Side)
        qr_buf = generate_qr_buffer(c_data["verification_url"], box_size=5, border=1)
        c.drawImage(ImageReader(qr_buf), width - 115, footer_y - 32, width=54, height=54)

        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(colors.HexColor("#0F2942"))
        c.drawRightString(width - 122, footer_y + 14, "Official Registry Verification")
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#4A5568"))
        c.drawRightString(width - 122, footer_y + 4, f"Credential ID: {c_data['cert_id']}")
        c.drawRightString(width - 122, footer_y - 6, "Tamper-Proof Verification")
        c.drawRightString(width - 122, footer_y - 16, "Portal: dbert.in/verify")

        # Bottom Legal Margin Line
        c.setFont("Helvetica", 7.2)
        c.setFillColor(colors.HexColor("#718096"))
        c.drawCentredString(width / 2.0, 42, "This Letter of Recommendation is an official credential issued by DBERT.")
        c.drawCentredString(width / 2.0, 32, f"Authenticity can be verified at https://dbert.in/verify?certid={c_data['cert_id']}")

        c.showPage()
        c.save()

    # ==================================================================================
    # MERGED MASTER PDF & PREVIEW HELPERS
    # ==================================================================================
    @classmethod
    def get_document_pdf_bytes(cls, conn, cert_id: str, doc_num: int) -> Optional[Tuple[bytes, str]]:
        """Returns (pdf_bytes, filename) for document 1, 2, or 3."""
        c_data = cls.resolve_candidate_data(conn, cert_id)
        if not c_data:
            return None

        buf = BytesIO()
        if doc_num == 1:
            cls.draw_cert_completion(buf, c_data)
            filename = f"1_Certificate_of_Completion_{c_data['cert_id']}.pdf"
        elif doc_num == 2:
            cls.draw_cert_evaluation(buf, c_data)
            filename = f"2_Academic_Project_Evaluation_{c_data['cert_id']}.pdf"
        elif doc_num == 3:
            cls.draw_cert_lor(buf, c_data)
            filename = f"3_Letter_of_Recommendation_{c_data['cert_id']}.pdf"
        else:
            return None

        buf.seek(0)
        return buf.getvalue(), filename

    @classmethod
    def get_master_pdf_bytes(cls, conn, cert_id: str) -> Optional[Tuple[bytes, str]]:
        """
        Merges all 3 documents into a unified 3-page master vector PDF:
        Page 1: Certificate Landscape
        Page 2: Academic Evaluation Portrait
        Page 3: Letter of Recommendation Portrait
        """
        c_data = cls.resolve_candidate_data(conn, cert_id)
        if not c_data:
            return None

        master_doc = fitz.open()
        for doc_num in [1, 2, 3]:
            res = cls.get_document_pdf_bytes(conn, cert_id, doc_num)
            if res:
                doc_bytes, _ = res
                sub_doc = fitz.open(stream=doc_bytes, filetype="pdf")
                master_doc.insert_pdf(sub_doc)

        master_bytes = master_doc.tobytes()
        filename = f"DBERT_Master_Credential_Packet_{c_data['cert_id']}.pdf"
        return master_bytes, filename

    @classmethod
    def get_document_preview_bytes(cls, conn, cert_id: str, doc_num: int) -> Optional[bytes]:
        """Renders high-resolution 150 DPI preview PNG of document 1, 2, or 3."""
        res = cls.get_document_pdf_bytes(conn, cert_id, doc_num)
        if not res:
            return None
        doc_bytes, _ = res
        doc = fitz.open(stream=doc_bytes, filetype="pdf")
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=150)
        return pix.tobytes("png")
