"""
routes/enrollment.py - Enrollment & Cohort Routing Blueprint
Fulfills Phase 23 (Monolith Modularization) of INTERNSHIPPORTAL4_LOCAL_AI_AGENT_MASTER_PLAN.md

Endpoints:
- POST /cohort/<int:cohort_id>/enroll
- POST /attendance/ping
"""
from flask import Blueprint, jsonify, request
from services.auth_service import AuthService
from app import (
    get_db, now_str, log_error, clean_text,
    current_intern
)

enrollment_bp = Blueprint("enrollment", __name__)


@enrollment_bp.route("/cohort/<int:cohort_id>/enroll", methods=["POST"])
def cohort_enroll(cohort_id):
    """Enrolls the logged-in intern into a cohort with atomic capacity enforcement."""
    with get_db() as conn:
        intern = AuthService.current_intern(conn)
    if not intern:
        return jsonify({"status": "error", "message": "Authentication required"}), 401

    try:
        with get_db() as conn:
            cohort = conn.execute("SELECT * FROM cohorts WHERE id=?", (cohort_id,)).fetchone()
            if not cohort:
                return jsonify({"status": "error", "message": "Cohort not found"}), 404

            already = conn.execute(
                "SELECT 1 FROM cohort_enrollments WHERE cohort_id=? AND intern_id=?",
                (cohort_id, intern["id"])
            ).fetchone()
            if already:
                return jsonify({"status": "error", "message": "Already enrolled in this cohort"}), 400

            cap_val = cohort["capacity"] if "capacity" in cohort.keys() else cohort["max_capacity"] if "max_capacity" in cohort.keys() else 0
            max_cap = int(cap_val or 0)
            cursor = conn.execute(
                """
                INSERT INTO cohort_enrollments (cohort_id, intern_id)
                SELECT ?, ?
                WHERE ? = 0 OR (SELECT COUNT(*) FROM cohort_enrollments WHERE cohort_id=?) < ?
                """,
                (cohort_id, intern["id"], max_cap, cohort_id, max_cap)
            )
            if cursor.rowcount == 0:
                return jsonify({"status": "error", "message": "This cohort is full"}), 400

            conn.commit()
            return jsonify({"status": "success", "message": "Successfully enrolled in cohort"})
    except Exception as e:
        log_error("cohort-enroll", e)
        return jsonify({"status": "error", "message": "Failed to enroll"}), 500





@enrollment_bp.route("/launchpad", methods=["GET"])
def launchpad_checkout():
    """Public landing page for DBERT Launchpad (2-month course track + AI tutor)."""
    from flask import render_template
    from app import PAID_PROGRAM_AMOUNT, UPI_ID
    return render_template("program.html", program_name="launchpad", title="DBERT Launchpad Program", paid_amount=PAID_PROGRAM_AMOUNT, upi_id=UPI_ID)


@enrollment_bp.route("/accelerate", methods=["GET"])
def accelerate_checkout():
    """Public landing page for DBERT Accelerate (Live Project Sprints)."""
    from flask import render_template
    from app import PAID_PROGRAM_AMOUNT, UPI_ID
    return render_template("program.html", program_name="accelerate", title="DBERT Accelerate Sprints", paid_amount=PAID_PROGRAM_AMOUNT, upi_id=UPI_ID)


@enrollment_bp.route("/internships/<page_slug>", methods=["GET"])
def seo_internship_landing(page_slug):
    """Public SEO landing pages targeting high-intent tech internship queries."""
    from flask import render_template, abort
    from app import PAID_PROGRAM_AMOUNT, UPI_ID

    seo_pages = {
        "ai-automation-internship": {
            "title": "AI Automation Internship — Remote & Virtual Cohort 2026",
            "meta_desc": "Apply for DBERT AI Automation Internship. Build multi-provider LLM pipelines, autonomous agents, and RAG systems with stipend opportunities.",
            "keyword": "AI Automation Internship",
            "domain": "Generative AI & Agent Engineering"
        },
        "data-analyst-internship-work-from-home": {
            "title": "Data Analyst Internship Work From Home — Paid Remote Track",
            "meta_desc": "Work from home data analyst internship. Master SQL, Python data pipelines, Power BI dashboards, and PostgreSQL schema architecture.",
            "keyword": "Data Analyst Internship Work From Home",
            "domain": "Data Analytics & Business Intelligence"
        },
        "virtual-remote-internships": {
            "title": "Virtual Remote Internships — Software & AI Development",
            "meta_desc": "Gain verified software engineering experience through virtual remote internships at DBERT Labs. Real code reviews & GitHub contributions.",
            "keyword": "Virtual Remote Internships",
            "domain": "Software Engineering & Web Development"
        },
        "paid-internships": {
            "title": "Paid Internships for Tech & AI Engineers — DBERT Fellowship",
            "meta_desc": "Apply for performance-based paid internships and stipends. Build production lab software and earn industry-recognized verified credentials.",
            "keyword": "Paid Internships for Students",
            "domain": "All Engineering Tracks"
        }
    }

    if page_slug not in seo_pages:
        abort(404)

    page_info = seo_pages[page_slug]
    return render_template(
        "seo_landing.html",
        page=page_info,
        page_slug=page_slug,
        paid_amount=PAID_PROGRAM_AMOUNT,
        upi_id=UPI_ID
    )


