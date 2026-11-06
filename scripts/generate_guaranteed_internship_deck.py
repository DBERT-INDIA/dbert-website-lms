"""
Generate DBERT Guaranteed Internship Program Candidate Pitch Deck.
Output: guaranteed_internship_program_dbert.pptx
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # Color Palette - Modern Dark Slate & Neon Accents
    BG_COLOR = RGBColor(11, 15, 23)        # #0B0F17 Deep Slate
    CARD_BG = RGBColor(21, 28, 44)         # #151C2C Dark Navy Surface
    CARD_BORDER = RGBColor(43, 53, 76)     # #2B354C Subtle Border
    CARD_BG_LIGHT = RGBColor(28, 38, 59)   # #1C263B Elevated Surface
    
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_MUTED = RGBColor(148, 163, 184)   # #94A3B8 Slate Gray
    TEXT_SUBTLE = RGBColor(100, 116, 139)  # #64748B Dim Gray
    
    ACCENT_AMBER = RGBColor(245, 158, 11)  # #F59E0B DBERT Amber
    ACCENT_CYAN = RGBColor(6, 182, 212)    # #06B6D4 Electric Cyan
    ACCENT_GREEN = RGBColor(16, 185, 129)  # #10B981 Emerald
    ACCENT_ROSE = RGBColor(244, 63, 94)    # #F43F5E Coral / Alert
    
    FONT_TITLE = "Segoe UI"
    FONT_BODY = "Segoe UI"
    FONT_MONO = "Consolas"

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, doclabel, title, subtitle=None):
        # Doclabel pill
        label_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf_label = label_box.text_frame
        tf_label.word_wrap = True
        tf_label.margin_left = tf_label.margin_right = tf_label.margin_top = tf_label.margin_bottom = 0
        p_label = tf_label.paragraphs[0]
        p_label.text = doclabel.upper()
        p_label.font.name = FONT_MONO
        p_label.font.size = Pt(10)
        p_label.font.bold = True
        p_label.font.color.rgb = ACCENT_AMBER

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = FONT_TITLE
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        # Subtitle
        if subtitle:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.7), Inches(0.45))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(11.5)
            p_sub.font.color.rgb = TEXT_MUTED

    def add_footer(slide, current_slide, total_slides=14):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"DBERT TALENT INCUBATOR  •  GUARANTEED INTERNSHIP PROGRAM (2026 COHORT)          [ SLIDE {current_slide:02d} / {total_slides:02d} ]"
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_SUBTLE

    def add_card(slide, left, top, width, height, bg_rgb=CARD_BG, border_rgb=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_rgb
        card.line.color.rgb = border_rgb
        card.line.width = Pt(1)
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Accent decorative top glow bar
    glow = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(2.2), Inches(0.06))
    glow.fill.solid()
    glow.fill.fore_color.rgb = ACCENT_AMBER
    glow.line.fill.background()

    # Category Pill
    cat_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(11.5), Inches(0.4))
    tf_cat = cat_box.text_frame
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = "DBERT TALENT INCUBATOR  •  CAREER ACCELERATION COHORT 2026"
    p_cat.font.name = FONT_MONO
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = ACCENT_AMBER

    # Title
    t_box = slide1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.8))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Guaranteed Internship Program"
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(40)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE
    
    p_t2 = tf_t.add_paragraph()
    p_t2.text = "Break through 1,000-applicant job boards. Master production engineering, deploy real client capstones, and unlock guaranteed paid placement with 100% money-back peace of mind."
    p_t2.font.name = FONT_BODY
    p_t2.font.size = Pt(14)
    p_t2.font.color.rgb = TEXT_MUTED
    p_t2.space_before = Pt(14)

    # 3 Stat Cards across bottom
    stats_data = [
        ("2,480+ ACTIVE ROLES", "Verified India Pipeline", "47.3% Remote (1,174) • 52.7% On-Site (1,306)\nBengaluru, Mumbai, Delhi-NCR, Pune", ACCENT_CYAN),
        ("100% PLACEMENT GUARANTEE", "Backed by Full Refund", "80% sprint completion + capstone project\nPaid stipends: ₹10,000 – ₹35,000 / month", ACCENT_GREEN),
        ("₹1,999 INTRODUCTORY FEE", "Slashed from ₹7,999 (75% OFF)", "2-Month intensive sprint • Zero ISA cut\nYou keep 100% of your future earnings", ACCENT_AMBER)
    ]

    for idx, (title, sub, body, accent) in enumerate(stats_data):
        cx = 0.8 + idx * 4.0
        cy = 4.0
        cw = 3.7
        ch = 2.4
        add_card(slide1, cx, cy, cw, ch, CARD_BG, CARD_BORDER)

        t_stat = slide1.shapes.add_textbox(Inches(cx + 0.25), Inches(cy + 0.25), Inches(cw - 0.5), Inches(ch - 0.5))
        tf_s = t_stat.text_frame
        tf_s.word_wrap = True

        p1 = tf_s.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_MONO
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = accent

        p2 = tf_s.add_paragraph()
        p2.text = sub
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(4)

        p3 = tf_s.add_paragraph()
        p3.text = body
        p3.font.name = FONT_BODY
        p3.font.size = Pt(10)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(8)

    add_footer(slide1, 1)

    # ==========================================
    # SLIDE 2: THE BRUTAL REALITY OF FRESHER HIRING
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "§ 01 — THE BROKEN HIRING MARKET", 
               "Why 90% of Fresher Applications Disappear into Black Holes",
               "Traditional job applications have an 89% rejection rate before human eyes ever read the resume.")

    cards_s2 = [
        ("TRAP 01", "The 1,200+ Applicant Inbox Crush",
         "When an Indian startup posts an internship on LinkedIn or open job boards, hundreds of resumes flood in within 48 hours.\n\nRecruiters physically cannot read every application and rely on brutal surface filters that reject qualified candidates simply due to queue position.", ACCENT_ROSE),
        ("TRAP 02", "Automated ATS Discard Filters",
         "Applicant Tracking Systems scan for contextual keywords, clean single-column structure, and parseable date formats.\n\nFancy two-column Canva templates, skill-bar graphics (e.g. 4/5 stars in Python), and missing role keywords cause automated instant rejection before human review.", ACCENT_AMBER),
        ("TRAP 03", "The 'Toy Project' Disqualification",
         "Listing tutorial datasets like Titanic Survival, Iris Flower classification, or Boston Housing signals you followed a generic tutorial.\n\nRecruiters and hiring managers know freshers who rely on toy datasets lack practical commercial understanding and cannot handle real messy corporate data.", ACCENT_CYAN)
    ]

    for idx, (pill, title, desc, accent) in enumerate(cards_s2):
        cx = 0.8 + idx * 4.0
        cy = 2.1
        cw = 3.7
        ch = 4.6
        add_card(slide2, cx, cy, cw, ch)

        t_card = slide2.shapes.add_textbox(Inches(cx + 0.3), Inches(cy + 0.3), Inches(cw - 0.6), Inches(ch - 0.6))
        tf = t_card.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = pill
        p0.font.name = FONT_MONO
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(12)

    add_footer(slide2, 2)

    # ==========================================
    # SLIDE 3: WHY OPEN JOB BOARDS LEAVE CANDIDATES STRANDED
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "§ 02 — THE COMPETITIVE LANDSCAPE", 
               "The Hidden Traps of Internshala & Open Portals",
               "Traditional job boards monetize job listings and employer ads — not student career outcomes.")

    cards_s3 = [
        ("INTERNSHALA REALITY", "The Endless Application Lottery", [
            "• Massive applicant flooding: 800 to 2,500+ candidates per listing.",
            "• Ghost listings: Over 60% of postings never send candidate callbacks.",
            "• Rampant unpaid tasks: Commission-only 'Campus Ambassador' roles disguised as professional internships.",
            "• Zero skill verification: Recruiters have no way to distinguish serious talent from spam applicants.",
            "• No placement guarantee: Candidates are left completely on their own to apply endlessly."
        ], ACCENT_ROSE),
        ("UNSTOP REALITY", "The Tier-1 Tournament Trap", [
            "• Fierce elimination tournaments: Hackathons & corporate case challenges.",
            "• Heavy institutional bias: Corporate sponsors prioritize IITs, IIMs, and premier colleges.",
            "• Razor-thin shortlist rates: Less than 0.5%–1% of participants receive interview calls.",
            "• High stress, zero mentorship: You compete blindly without code reviews or personalized feedback.",
            "• No guaranteed pathway: Winning a certificate does not equal a paid placement offer."
        ], ACCENT_AMBER),
        ("THE CANDIDATE's COST", "3 to 6 Months of Lost Opportunity", [
            "• Application fatigue: Spending 20+ hours a week submitting resumes into silent inboxes.",
            "• Loss of confidence: Self-doubt caused by algorithmic rejection and ghosting.",
            "• Wasted time on toy projects: Learning tools without commercial business application.",
            "• Predatory bootcamps: Other programs trap candidates in exploitative 15% salary cuts (ISAs).",
            "• DBERT Fix: Direct talent incubator, verified capstones, and guaranteed placement."
        ], ACCENT_CYAN)
    ]

    for idx, (pill, title, points, accent) in enumerate(cards_s3):
        cx = 0.8 + idx * 4.0
        cy = 2.1
        cw = 3.7
        ch = 4.6
        add_card(slide3, cx, cy, cw, ch)

        t_card = slide3.shapes.add_textbox(Inches(cx + 0.3), Inches(cy + 0.3), Inches(cw - 0.6), Inches(ch - 0.6))
        tf = t_card.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = pill
        p0.font.name = FONT_MONO
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(4)

        for pt in points:
            p_pt = tf.add_paragraph()
            p_pt.text = pt
            p_pt.font.name = FONT_BODY
            p_pt.font.size = Pt(10.5)
            p_pt.font.color.rgb = TEXT_MUTED
            p_pt.space_before = Pt(8)

    add_footer(slide3, 3)

    # ==========================================
    # SLIDE 4: COMPARISON MATRIX: DBERT VS INTERNSHALA VS UNSTOP
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "§ 03 — HEAD-TO-HEAD COMPARISON", 
               "DBERT vs. Internshala vs. Unstop: Side-by-Side Evaluation",
               "Why modern engineering candidates choose a dedicated talent incubator over generic job boards.")

    # Table dimensions
    t_left = Inches(0.8)
    t_top = Inches(2.1)
    t_width = Inches(11.73)
    t_height = Inches(4.6)

    table_shape = slide4.shapes.add_table(7, 4, t_left, t_top, t_width, t_height)
    table = table_shape.table
    table.columns[0].width = Inches(2.4)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(3.0)
    table.columns[3].width = Inches(3.33)

    headers = ["EVALUATION CRITERIA", "INTERNSHALA", "UNSTOP", "DBERT GUARANTEED PROGRAM"]
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG_LIGHT if c_idx < 3 else RGBColor(30, 58, 95)
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_AMBER if c_idx == 3 else TEXT_WHITE

    rows_data = [
        ("Placement Guarantee", "Zero guarantee (0%). Left to fend on open board.", "Zero guarantee. Winners get trophies/cash.", "100% Guaranteed Paid Placement or Full Refund"),
        ("Applicant Competition", "500 – 2,500+ applicants competing per post.", "1,000+ teams in elimination hackathons.", "Direct curated pipeline. Capped at 35 per batch."),
        ("Stipend Quality", "Frequent unpaid or sub-standard stipends (<₹5K).", "No stipend guarantee (prizes only).", "100% Paid: ₹10,000 – ₹35,000 / month."),
        ("Portfolio & Vetting", "Resume keyword screening only. No code audit.", "Timed MCQ quizzes and automated tests.", "Live GitHub PRs, NovyPro Power BI & Capstones."),
        ("Interview Preparation", "None. No practice or feedback provided.", "Generic question sets and community forums.", "Built-in Gemini AI Mock Technical Interview Simulator."),
        ("Commercial Risk & Cost", "Free / Paid certificate add-ons with 0 outcomes.", "Free entry, massive time investment, <1% win.", "Introductory ₹1,999 (Slashed from ₹7,999) + 0% ISA.")
    ]

    for r_idx, row in enumerate(rows_data, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.fill.solid()
            if c_idx == 3:
                cell.fill.fore_color.rgb = RGBColor(18, 38, 64) # Highlight DBERT column
            else:
                cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 1 else RGBColor(17, 24, 39)
            
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY if c_idx > 0 else FONT_MONO
            p.font.size = Pt(9.5)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
            elif c_idx == 3:
                p.font.bold = True
                p.font.color.rgb = ACCENT_GREEN
            else:
                p.font.color.rgb = TEXT_MUTED

    add_footer(slide4, 4)

    # ==========================================
    # SLIDE 5: THE DBERT UNFAIR ADVANTAGE (VENTURE STUDIO)
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "§ 04 — ECOSYSTEM ADVANTAGE", 
               "The DBERT Unfair Advantage: Active Venture Studio Ecosystem",
               "We don't simply aggregate job links — we build production AI systems and incubate startups.")

    pillars = [
        ("PILLAR 01", "Production Engineering Studio", 
         "DBERT operates an active software laboratory building live products like DBERT Chat, Document AI, and LMS engines.\n\nBecause our senior staff ships code in production daily, what you learn is 100% practical: live Git branches, automated CI/CD pipelines, containerization, and clean database schemas.", ACCENT_AMBER),
        ("PILLAR 02", "Direct Startup Talent Syndicate", 
         "Dozens of partner startups build and scale their technical products within the DBERT venture ecosystem.\n\nWhen these companies need entry-level data analysts, AI agent engineers, and full stack developers, they hire directly from our vetted sprint cohorts — bypassing open job boards completely.", ACCENT_CYAN),
        ("PILLAR 03", "Zero-ISA & Ethical Economics", 
         "Traditional bootcamps trap learners in predatory Income Share Agreements (ISAs) deducting 15% of salary for years.\n\nDBERT charges a simple, transparent introductory fee of ₹1,999. You keep 100% of your internship stipend, 100% of your future salary, and carry zero debt.", ACCENT_GREEN)
    ]

    for idx, (pill, title, desc, accent) in enumerate(pillars):
        cx = 0.8 + idx * 4.0
        cy = 2.1
        cw = 3.7
        ch = 4.6
        add_card(slide5, cx, cy, cw, ch)

        t_card = slide5.shapes.add_textbox(Inches(cx + 0.3), Inches(cy + 0.3), Inches(cw - 0.6), Inches(ch - 0.6))
        tf = t_card.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = pill
        p0.font.name = FONT_MONO
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(12)

    add_footer(slide5, 5)

    # ==========================================
    # SLIDE 6: CURRENT JOB POOL INTELLIGENCE
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "§ 05 — LIVE DATABASE INTELLIGENCE", 
               "Inside the DBERT Portal: 6,622 Verified Opportunities",
               "Directly queried and audited from our production database (apps/portal/internship.db).")

    # 4 Stat Cards across top
    pool_stats = [
        ("6,622", "TOTAL OPPORTUNITIES", "Curated and verified across India & Global tech hubs", ACCENT_AMBER),
        ("2,480", "ACTIVE INDIA ROLES", "47.3% Remote • 52.7% On-Location in top tech metros", ACCENT_CYAN),
        ("₹10K – ₹35K", "MONTHLY STIPENDS", "100% paid opportunities with transparent compensation", ACCENT_GREEN),
        ("4,142", "GLOBAL / REMOTE ROLES", "International pipeline across Europe, UK, and US startups", RGBColor(168, 85, 247))
    ]

    for idx, (num, lbl, sub, accent) in enumerate(pool_stats):
        cx = 0.8 + idx * 3.0
        cy = 2.1
        cw = 2.75
        ch = 1.9
        add_card(slide6, cx, cy, cw, ch)

        t_box = slide6.shapes.add_textbox(Inches(cx + 0.2), Inches(cy + 0.2), Inches(cw - 0.4), Inches(ch - 0.4))
        tf = t_box.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = num
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = accent

        p2 = tf.add_paragraph()
        p2.text = lbl
        p2.font.name = FONT_MONO
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.name = FONT_BODY
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = TEXT_MUTED
        p3.space_before = Pt(4)

    # 2 Wide Cards below
    wide_cards = [
        ("SOURCING INTELLIGENCE & PARTNER NETWORK", 
         "Where Do Our Internship Openings Come From?",
         "• DBERT Studio Partners: Direct hiring quotas reserved for DBERT cohort graduates.\n"
         "• Unstop & Internshala High-Value Feeds: Filtered to remove unpaid and spam listings.\n"
         "• LinkedIn Remote India Network: Daily scrubbed and verified hiring manager posts.\n"
         "• Global API Syndication: Direct sync with Arbeitnow, Remotive, and AngelList startup feeds.",
         0.8, 4.25, 5.75, 2.45, ACCENT_CYAN),
        ("THE DBERT QUALITY & ANTI-SPAM FILTER", 
         "Zero Unpaid Exploitation. Guaranteed Transparency.",
         "• Unpaid Filter: Every listing with zero or commission-based pay is purged from our portal.\n"
         "• Company Legality Audit: MSME, GST, and LinkedIn verified startup entities only.\n"
         "• Freshness Protocol: Job feeds are auto-expired after 30 days to prevent dead-end applications.\n"
         "• Transparent Stipend Band: Clear upfront disclosure of monthly compensation before applying.",
         6.75, 4.25, 5.75, 2.45, ACCENT_GREEN)
    ]

    for (pill, title, points, cx, cy, cw, ch, accent) in wide_cards:
        add_card(slide6, cx, cy, cw, ch)
        t_box = slide6.shapes.add_textbox(Inches(cx + 0.25), Inches(cy + 0.2), Inches(cw - 0.5), Inches(ch - 0.4))
        tf = t_box.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = pill
        p0.font.name = FONT_MONO
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = points
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(6)

    add_footer(slide6, 6)

    # ==========================================
    # SLIDE 7: REMOTE VS ON-LOCATION BREAKDOWN (INDIA MARKET)
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "§ 06 — GEOGRAPHIC REACH", 
               "Flexibility That Fits You: Remote vs. On-Location Breakdown",
               "Whether you prefer working from home or inside high-growth tech hubs, our 2,480 India roles have you covered.")

    # Left Column: Remote (47.3%)
    add_card(slide7, 0.8, 2.1, 5.7, 4.6)
    t_rem = slide7.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(5.1), Inches(4.1))
    tf_rem = t_rem.text_frame
    tf_rem.word_wrap = True

    p_r0 = tf_rem.paragraphs[0]
    p_r0.text = "WORK FROM ANYWHERE  •  47.3% OF POOL"
    p_r0.font.name = FONT_MONO
    p_r0.font.size = Pt(11)
    p_r0.font.bold = True
    p_r0.font.color.rgb = ACCENT_CYAN

    p_r1 = tf_rem.add_paragraph()
    p_r1.text = "1,174 Remote Internships"
    p_r1.font.name = FONT_TITLE
    p_r1.font.size = Pt(22)
    p_r1.font.bold = True
    p_r1.font.color.rgb = TEXT_WHITE
    p_r1.space_before = Pt(4)

    rem_points = [
        ("Zero Relocation Costs:", "Save ₹15,000–₹25,000/mo on metro rent, food, and daily transit."),
        ("Pan-India Access:", "Students in Tier-2/3 cities work directly for Tier-1 Bengaluru and Mumbai startups."),
        ("Flexible Schedules:", "Asynchronous sprint workflows allowing college exam and study balance."),
        ("Primary Remote Domains:", "Data Analytics, AI Prompt Engineering, Python Automation & Web Development."),
        ("Verified Hardware Stipends:", "Select partner roles provide laptop allowances and home office setups.")
    ]

    for title, desc in rem_points:
        p = tf_rem.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r1.font.size = Pt(10)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = TEXT_MUTED
        r2.font.size = Pt(10)
        p.space_before = Pt(6)

    # Right Column: On-Location (52.7%)
    add_card(slide7, 6.8, 2.1, 5.7, 4.6)
    t_loc = slide7.shapes.add_textbox(Inches(7.1), Inches(2.35), Inches(5.1), Inches(4.1))
    tf_loc = t_loc.text_frame
    tf_loc.word_wrap = True

    p_l0 = tf_loc.paragraphs[0]
    p_l0.text = "OFFICE & HYBRID HUBS  •  52.7% OF POOL"
    p_l0.font.name = FONT_MONO
    p_l0.font.size = Pt(11)
    p_l0.font.bold = True
    p_l0.font.color.rgb = ACCENT_AMBER

    p_l1 = tf_loc.add_paragraph()
    p_l1.text = "1,306 On-Location Roles"
    p_l1.font.name = FONT_TITLE
    p_l1.font.size = Pt(22)
    p_l1.font.bold = True
    p_l1.font.color.rgb = TEXT_WHITE
    p_l1.space_before = Pt(4)

    loc_points = [
        ("Delhi NCR (166+ Roles):", "Noida Cyber City, Gurgaon DLF CyberHub, Central Delhi startup hubs."),
        ("Mumbai & MMR (131+ Roles):", "Bandra Kurla Complex (BKC), Andheri tech corridors, Navi Mumbai."),
        ("Bengaluru (130+ Roles):", "Koramangala, HSR Layout, Indiranagar, Electronic City & Whitefield."),
        ("Pune & Western Hubs (36+ Roles):", "Hinjawadi Infotech Park, Baner, Viman Nagar startups."),
        ("Emerging Tech Hubs (100+ Roles):", "Jaipur (36), Chennai (27), Hyderabad, Ahmedabad, and Kolkata."),
        ("Direct PPO Potential:", "82% of in-office interns convert to full-time Pre-Placement Offers (PPOs).")
    ]

    for title, desc in loc_points:
        p = tf_loc.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r1.font.size = Pt(10)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = TEXT_MUTED
        r2.font.size = Pt(10)
        p.space_before = Pt(5)

    add_footer(slide7, 7)

    # ==========================================
    # SLIDE 8: THE 4 CORE IN-DEMAND TRACKS
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "§ 07 — CURRICULUM BLUEPRINTS", 
               "The 4 High-Demand Skill Tracks That Guarantee Hiring",
               "Targeted engineering paths designed to match exact role requirements in our 2,480 active Indian postings.")

    tracks = [
        ("DATA ANALYTICS & BI", "1,146 Active India Openings",
         "• Core Stack: Advanced Excel (XLOOKUP, Power Query), Business SQL, Power BI, Python Pandas.\n"
         "• Real Projects: E-Commerce Customer Churn, Fintech Underwriting Risk, Quick-Commerce SLA Dashboards.\n"
         "• Outcome: Hosted NovyPro interactive Power BI portfolio + ATS-ready data storytelling.",
         0.8, 2.1, 5.7, 2.2, ACCENT_AMBER),
        ("AI AGENT DEVELOPMENT", "638 Active India Openings",
         "• Core Stack: LangGraph, CrewAI, Local Ollama runtime, Prompt Orchestration, Tool Calling.\n"
         "• Real Projects: Autonomous Customer Lead Qualifier, Multi-Agent Market Research Swarm, Document RAG.\n"
         "• Outcome: Live deployable agent state machines on GitHub with full architectural documentation.",
         6.8, 2.1, 5.7, 2.2, ACCENT_CYAN),
        ("FULL STACK AI DEVELOPMENT", "485 Active India Openings",
         "• Core Stack: Next.js 15, TypeScript, Tailwind CSS, FastAPI, PostgreSQL, pgvector.\n"
         "• Real Projects: Multi-tenant SaaS with streaming LLM response tokens, JWT auth, and Razorpay billing.\n"
         "• Outcome: Production-grade containerized web applications deployed live on Vercel/Docker.",
         0.8, 4.5, 5.7, 2.2, ACCENT_GREEN),
        ("PYTHON SYSTEM AUTOMATION", "211 Active India Openings",
         "• Core Stack: Playwright headless browser, Celery task queues, Redis, BeautifulSoup, REST APIs.\n"
         "• Real Projects: High-throughput job scraping pipelines, automated invoice reconcilers, alert bots.\n"
         "• Outcome: Automated asynchronous backend pipelines running in production environments.",
         6.8, 4.5, 5.7, 2.2, RGBColor(236, 72, 153))
    ]

    for (title, count, desc, cx, cy, cw, ch, accent) in tracks:
        add_card(slide8, cx, cy, cw, ch)
        t_box = slide8.shapes.add_textbox(Inches(cx + 0.25), Inches(cy + 0.2), Inches(cw - 0.5), Inches(ch - 0.4))
        tf = t_box.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_TITLE
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = count
        p1.font.name = FONT_MONO
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(4)

    add_footer(slide8, 8)

    # ==========================================
    # SLIDE 9: THE 2-MONTH SPRINT-TO-PLACEMENT ROADMAP
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "§ 08 — SPRINT ROADMAP", 
               "The 2-Month Sprint-to-Placement Journey: Step-by-Step",
               "A structured, milestone-driven curriculum designed to turn complete beginners into industry-ready candidates.")

    sprints = [
        ("WEEKS 1 – 2", "Production Foundations", 
         "• Professional Git branching & GitHub setup.\n"
         "• Linux Bash & clean developer environment.\n"
         "• Foundational tools: SQL / Python / APIs.\n"
         "• Milestone: Pass the Week 2 Architecture Diagnostic.", ACCENT_AMBER),
        ("WEEKS 3 – 4", "Real Corporate Datasets", 
         "• Zero toy datasets (No Titanic / Iris).\n"
         "• Dirty corporate data cleaning with real CSVs.\n"
         "• Multi-table joins & dynamic window functions.\n"
         "• Milestone: Build & optimize your first client pipeline.", ACCENT_CYAN),
        ("WEEKS 5 – 6", "Capstone Deployment", 
         "• Build end-to-end commercial capstone project.\n"
         "• Host interactive web dashboards on NovyPro.\n"
         "• Publish clean GitHub repos with architecture diagrams.\n"
         "• Milestone: Capstone Project Submission & Code Audit.", ACCENT_GREEN),
        ("WEEKS 7 – 8", "AI Interview & Placement", 
         "• Gemini AI Technical Mock Interview Simulator.\n"
         "• ATS Resume single-column rewrite & roast.\n"
         "• Direct application unlocking to 2,480+ roles.\n"
         "• Milestone: Guaranteed Paid Placement Interviews.", RGBColor(168, 85, 247))
    ]

    for idx, (pill, title, points, accent) in enumerate(sprints):
        cx = 0.8 + idx * 3.0
        cy = 2.1
        cw = 2.75
        ch = 4.6
        add_card(slide9, cx, cy, cw, ch)

        t_box = slide9.shapes.add_textbox(Inches(cx + 0.25), Inches(cy + 0.25), Inches(cw - 0.5), Inches(ch - 0.5))
        tf = t_box.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = pill
        p0.font.name = FONT_MONO
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = points
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(10)

    add_footer(slide9, 9)

    # ==========================================
    # SLIDE 10: EXCLUSIVE DBERT EDGE (GEMINI AI MOCK INTERVIEWS)
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "§ 09 — AI-POWERED ADVANTAGE", 
               "Built-in Gemini AI Mock Interview Engine",
               "Practice realistic technical and behavioral grilling on our portal before you ever meet hiring managers.")

    ai_features = [
        ("FEATURE 01", "Domain-Specific Technical Grilling",
         "Our native LMS engine uses Google Gemini AI to conduct live technical interview simulations tailored to your domain.\n\nWhether testing SQL join logic, window functions, prompt engineering trade-offs, or REST API architecture, the AI grills you with real-world startup scenarios.", ACCENT_CYAN),
        ("FEATURE 02", "Instant Scoring & Rubric Feedback",
         "Receive instant, objective diagnostic feedback on:\n\n• Technical Accuracy: Did you correctly identify edge cases?\n• Business Acumen: Did you explain the 'So What?' behind numbers?\n• Communication & STAR Structure: Situation, Task, Action, Result.\n• Specific improvement cues before round 1 with real founders.", ACCENT_AMBER),
        ("FEATURE 03", "The Confidence Multiplier",
         "Most students fail interviews due to freezing up under pressure and speaking in theoretical jargon.\n\nAfter completing 5+ rounds with our AI simulator, candidates walk into hiring manager interviews relaxed, articulate, and prepared to handle technical challenges with ease.", ACCENT_GREEN)
    ]

    for idx, (pill, title, desc, accent) in enumerate(ai_features):
        cx = 0.8 + idx * 4.0
        cy = 2.1
        cw = 3.7
        ch = 4.6
        add_card(slide10, cx, cy, cw, ch)

        t_card = slide10.shapes.add_textbox(Inches(cx + 0.3), Inches(cy + 0.3), Inches(cw - 0.6), Inches(ch - 0.6))
        tf = t_card.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = pill
        p0.font.name = FONT_MONO
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(12)

    add_footer(slide10, 10)

    # ==========================================
    # SLIDE 11: PORTFOLIO OVER PAPER (WHAT RECRUITERS SEE)
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "§ 10 — THE CANDIDATE DOSSIER", 
               "Portfolio Over Paper: Why DBERT Candidates Stand Out",
               "A stark comparison between what a typical applicant sends versus what a DBERT graduate delivers.")

    # Left: The 90% Typical Applicant (Red Card)
    add_card(slide11, 0.8, 2.1, 5.7, 4.6, CARD_BG, RGBColor(120, 30, 45))
    t_bad = slide11.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(5.1), Inches(4.1))
    tf_bad = t_bad.text_frame
    tf_bad.word_wrap = True

    pb0 = tf_bad.paragraphs[0]
    pb0.text = "THE 90% TYPICAL APPLICANT  •  REJECTED"
    pb0.font.name = FONT_MONO
    pb0.font.size = Pt(11)
    pb0.font.bold = True
    pb0.font.color.rgb = ACCENT_ROSE

    pb1 = tf_bad.add_paragraph()
    pb1.text = "Standard Job Board Applicant"
    pb1.font.name = FONT_TITLE
    pb1.font.size = Pt(20)
    pb1.font.bold = True
    pb1.font.color.rgb = TEXT_WHITE
    pb1.space_before = Pt(4)

    bad_points = [
        ("Format:", "Two-column graphic Canva PDF that breaks ATS parser."),
        ("Skill Claim:", "'Proficient in Python, SQL, C++, Java, Kotlin, HTML, CSS' (Recruiters know freshers master none)."),
        ("Projects:", "Titanic survival prediction, Iris flower classifier, generic sales table copy-pasted from YouTube."),
        ("Proof:", "Static PDF with zero clickable links or live proofs."),
        ("Interview:", "Freezes when asked simple business application questions like 'How would you measure customer churn?'"),
        ("Result:", "Ghosted in 6 seconds or automated rejection email.")
    ]

    for title, desc in bad_points:
        p = tf_bad.add_paragraph()
        r1 = p.add_run()
        r1.text = f"❌ {title} "
        r1.font.bold = True
        r1.font.color.rgb = ACCENT_ROSE
        r1.font.size = Pt(9.5)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = TEXT_MUTED
        r2.font.size = Pt(9.5)
        p.space_before = Pt(5)

    # Right: DBERT Graduate (Green Card)
    add_card(slide11, 6.8, 2.1, 5.7, 4.6, CARD_BG, RGBColor(20, 80, 50))
    t_good = slide11.shapes.add_textbox(Inches(7.1), Inches(2.35), Inches(5.1), Inches(4.1))
    tf_good = t_good.text_frame
    tf_good.word_wrap = True

    pg0 = tf_good.paragraphs[0]
    pg0.text = "THE DBERT COHORT GRADUATE  •  HIRED"
    pg0.font.name = FONT_MONO
    pg0.font.size = Pt(11)
    pg0.font.bold = True
    pg0.font.color.rgb = ACCENT_GREEN

    pg1 = tf_good.add_paragraph()
    pg1.text = "Vetted Candidate Dossier"
    pg1.font.name = FONT_TITLE
    pg1.font.size = Pt(20)
    pg1.font.bold = True
    pg1.font.color.rgb = TEXT_WHITE
    pg1.space_before = Pt(4)

    good_points = [
        ("Format:", "Clean ATS single-column layout engineered for 95%+ parsing."),
        ("Skill Proof:", "Mastery in core tool stack backed by real project impact (e.g. 'Reduced reporting query latency by 45%')."),
        ("Projects:", "120K order E-Commerce churn analysis, Fintech loan default modeling, or multi-agent LangGraph workflows."),
        ("Proof:", "Clickable NovyPro Power BI live link + documented GitHub repo."),
        ("Interview:", "Pre-tested through 5+ rounds on Gemini AI Mock Simulator."),
        ("Result:", "Direct hiring manager interview callbacks & guaranteed offers.")
    ]

    for title, desc in good_points:
        p = tf_good.add_paragraph()
        r1 = p.add_run()
        r1.text = f"✅ {title} "
        r1.font.bold = True
        r1.font.color.rgb = ACCENT_GREEN
        r1.font.size = Pt(9.5)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = TEXT_WHITE
        r2.font.size = Pt(9.5)
        p.space_before = Pt(5)

    add_footer(slide11, 11)

    # ==========================================
    # SLIDE 12: TRANSPARENT COMMERCIALS & THE GUARANTEE
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)
    add_header(slide12, "§ 11 — PRICING & GUARANTEE TERMS", 
               "Risk-Free Investment: Introductory Pricing & Placement Guarantee",
               "Zero salary deductions. Slashed introductory pricing. Backed by a full 100% money-back guarantee.")

    # Left Card: Commercials
    add_card(slide12, 0.8, 2.1, 5.7, 4.6)
    t_prc = slide12.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(5.1), Inches(4.1))
    tf_prc = t_prc.text_frame
    tf_prc.word_wrap = True

    pp0 = tf_prc.paragraphs[0]
    pp0.text = "TRANSPARENT FLAT COMMERCIALS"
    pp0.font.name = FONT_MONO
    pp0.font.size = Pt(11)
    pp0.font.bold = True
    pp0.font.color.rgb = ACCENT_AMBER

    pp1 = tf_prc.add_paragraph()
    pp1.text = "₹1,999 Introductory Launch Fee"
    pp1.font.name = FONT_TITLE
    pp1.font.size = Pt(22)
    pp1.font.bold = True
    pp1.font.color.rgb = TEXT_WHITE
    pp1.space_before = Pt(4)

    prc_points = [
        ("Regular Program Fee:", "₹7,999 (Slashed by 75% for introductory cohort)."),
        ("Program Duration:", "2 Months (Intensive weekend live sprints + async reviews)."),
        ("Zero Income Share (0% ISA):", "We never take a cut of your future salary. You keep 100% of your earnings."),
        ("No Hidden Fees:", "Includes portal access, AI mock interviews, curriculum, and placement support."),
        ("GST Invoice Compliance:", "Statutory tax invoicing and MSME vendor documentation provided."),
        ("Flexible Payment Options:", "UPI, NetBanking, Credit/Debit cards via secure Razorpay checkout.")
    ]

    for title, desc in prc_points:
        p = tf_prc.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r1.font.size = Pt(10)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = TEXT_MUTED
        r2.font.size = Pt(10)
        p.space_before = Pt(5)

    # Right Card: Guarantee Terms
    add_card(slide12, 6.8, 2.1, 5.7, 4.6)
    t_guar = slide12.shapes.add_textbox(Inches(7.1), Inches(2.35), Inches(5.1), Inches(4.1))
    tf_guar = t_guar.text_frame
    tf_guar.word_wrap = True

    pg0 = tf_guar.paragraphs[0]
    pg0.text = "100% MONEY-BACK PLACEMENT PROMISE"
    pg0.font.name = FONT_MONO
    pg0.font.size = Pt(11)
    pg0.font.bold = True
    pg0.font.color.rgb = ACCENT_GREEN

    pg1 = tf_guar.add_paragraph()
    pg1.text = "Guaranteed Placement Terms"
    pg1.font.name = FONT_TITLE
    pg1.font.size = Pt(22)
    pg1.font.bold = True
    pg1.font.color.rgb = TEXT_WHITE
    pg1.space_before = Pt(4)

    guar_points = [
        ("Clear Qualification Criteria:", "Maintain 80%+ sprint task completion and submit your verified Capstone Project."),
        ("The Placement Guarantee:", "Receive guaranteed verified paid internship placement within 60 days of graduation."),
        ("100% Money-Back Refund:", "If you fulfill the sprint criteria and do not secure a paid offer, receive an immediate full refund."),
        ("7-Day Unconditional Trial:", "Full 100% refund within the first 7 calendar days of the cohort if you feel the program isn't for you."),
        ("Stipend Range Protected:", "Guaranteed roles range between ₹10,000 and ₹35,000 / month."),
        ("Zero Fine Print:", "Simple, auditable, and contractually documented.")
    ]

    for title, desc in guar_points:
        p = tf_guar.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r1.font.size = Pt(10)
        r2 = p.add_run()
        r2.text = desc
        r2.font.color.rgb = TEXT_MUTED
        r2.font.size = Pt(10)
        p.space_before = Pt(5)

    add_footer(slide12, 12)

    # ==========================================
    # SLIDE 13: WHAT EVERY ENROLLED CANDIDATE RECEIVES
    # ==========================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13)
    add_header(slide13, "§ 12 — PROGRAM DELIVERABLES", 
               "What You Receive: The Complete Career Fast-Track Toolkit",
               "Everything included in your ₹1,999 enrollment to ensure your immediate career breakthrough.")

    deliverables = [
        ("DELIVERABLE 01", "2-Month Guided Engineering Sprints",
         "Live mentor-led workshops, code walkthroughs, and personal pull-request code reviews by senior developers.", ACCENT_AMBER),
        ("DELIVERABLE 02", "Exclusive 2,480+ Job Pool Pass",
         "Direct access to our curated Indian internship pipeline (1,174 Remote / 1,306 On-site) without 1,000-applicant queues.", ACCENT_CYAN),
        ("DELIVERABLE 03", "ATS Resume Rewrite & Live Roast",
         "Single-column ATS-engineered template with quantifiable STAR metrics, tailored directly to your chosen skill track.", ACCENT_GREEN),
        ("DELIVERABLE 04", "Gemini AI Mock Interview Engine",
         "Unlimited access to live AI interview simulations covering behavioral and technical rounds with instant diagnostic rubrics.", RGBColor(168, 85, 247)),
        ("DELIVERABLE 05", "Hosted Project Portfolio",
         "Interactive NovyPro Power BI dashboards, GitHub repository blueprints, and deployable live URLs that impress recruiters.", RGBColor(236, 72, 153)),
        ("DELIVERABLE 06", "Verifiable Credential & Referral",
         "Official MSME/GST recognized industry certificate and formal letter of recommendation from DBERT venture leadership.", ACCENT_AMBER)
    ]

    for idx, (pill, title, desc, accent) in enumerate(deliverables):
        col = idx % 3
        row = idx // 3
        cx = 0.8 + col * 4.0
        cy = 2.1 + row * 2.35
        cw = 3.7
        ch = 2.15
        add_card(slide13, cx, cy, cw, ch)

        t_box = slide13.shapes.add_textbox(Inches(cx + 0.25), Inches(cy + 0.2), Inches(cw - 0.5), Inches(ch - 0.4))
        tf = t_box.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = pill
        p0.font.name = FONT_MONO
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(4)

    add_footer(slide13, 13)

    # ==========================================
    # SLIDE 14: NEXT STEPS & CALL TO ACTION
    # ==========================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14)
    add_header(slide14, "§ 13 — BATCH ENROLLMENT", 
               "Secure Your Seat in Cohort 2026 — Limited to 35 Candidates",
               "We strictly cap each cohort to ensure high mentor attention, hands-on PR reviews, and guaranteed placements.")

    # 3 Steps
    steps = [
        ("STEP 01", "Diagnostic Assessment", 
         "Fill out our brief 3-minute technical background evaluation and select your target career track (Data Analytics, AI Agents, Full Stack, or Python).", ACCENT_AMBER),
        ("STEP 02", "Introductory Enrollment", 
         "Lock your guaranteed seat at the slashed introductory fee of ₹1,999 (regular ₹7,999). Covered by our 7-day unconditional money-back trial.", ACCENT_CYAN),
        ("STEP 03", "Squad Onboarding & Kickoff", 
         "Join your dedicated Discord engineering squad, access the LMS portal, and begin Week 1 production foundation sprints.", ACCENT_GREEN)
    ]

    for idx, (pill, title, desc, accent) in enumerate(steps):
        cx = 0.8 + idx * 4.0
        cy = 2.1
        cw = 3.7
        ch = 2.3
        add_card(slide14, cx, cy, cw, ch)

        t_box = slide14.shapes.add_textbox(Inches(cx + 0.25), Inches(cy + 0.25), Inches(cw - 0.5), Inches(ch - 0.5))
        tf = t_box.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = pill
        p0.font.name = FONT_MONO
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(8)

    # Large Bottom Banner
    add_card(slide14, 0.8, 4.65, 11.73, 2.05, CARD_BG_LIGHT, ACCENT_AMBER)
    t_cta = slide14.shapes.add_textbox(Inches(1.1), Inches(4.85), Inches(11.1), Inches(1.65))
    tf_cta = t_cta.text_frame
    tf_cta.word_wrap = True

    pc0 = tf_cta.paragraphs[0]
    pc0.text = "READY TO LAUNCH YOUR CAREER? ENROLL TODAY BEFORE SEATS CLOSE."
    pc0.font.name = FONT_TITLE
    pc0.font.size = Pt(18)
    pc0.font.bold = True
    pc0.font.color.rgb = TEXT_WHITE

    pc1 = tf_cta.add_paragraph()
    pc1.text = "👉 Visit: https://lms.dbert.in   |   Official Portal: https://dbert.in   |   Admissions: team@dbert.in"
    pc1.font.name = FONT_MONO
    pc1.font.size = Pt(12)
    pc1.font.bold = True
    pc1.font.color.rgb = ACCENT_AMBER
    pc1.space_before = Pt(8)

    pc2 = tf_cta.add_paragraph()
    pc2.text = "100% Placement Guarantee • ₹1,999 Introductory Offer • 7-Day Unconditional Refund Policy • Zero Future Salary Deductions (0% ISA)"
    pc2.font.name = FONT_BODY
    pc2.font.size = Pt(11)
    pc2.font.color.rgb = ACCENT_GREEN
    pc2.space_before = Pt(6)

    add_footer(slide14, 14)

    output_path = "guaranteed_internship_program_dbert.pptx"
    prs.save(output_path)
    print(f"Presentation generated successfully: {output_path}")

if __name__ == "__main__":
    create_deck()
