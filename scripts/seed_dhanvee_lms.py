"""
Idempotent seed script for Dhanvee (dhanvee.info / dhanvee.online) on DBERT LMS.

Creates/approves the Dhanvee company account (careers@dhanvee.info, max_live_posts=20)
and upserts + publishes the 4 role-level internship posts covering all 7 hub cities.

Usage (from repo root or /var/www/dbert-website-lms on EC2):
    python3 scripts/seed_dhanvee_lms.py
"""
import os
import sys
import json
import secrets
from datetime import datetime, timedelta

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTAL_DIR = os.path.join(REPO_ROOT, "apps", "portal")
if PORTAL_DIR not in sys.path:
    sys.path.insert(0, PORTAL_DIR)
os.chdir(PORTAL_DIR)

from app import get_db, ensure_column, _post_slugify, now_str, row_to_dict, hash_password  # noqa: E402

DHANVEE_EMAIL = "careers@dhanvee.info"
DHANVEE_NAME = "Dhanvee"
DHANVEE_WEBSITE = "https://dhanvee.info"
DHANVEE_ABOUT = (
    "Dhanvee (dhanvee.info / dhanvee.online) is a People-First Fintech & P2P Lending Beta "
    "platform incubated with DBERT, offering plain-English lending journeys, an AI credit "
    "simulator, and structured 3-month engineering & growth internships across India."
)
HUB_CITIES_LABEL = "Bangalore, Chennai, Delhi NCR, Hyderabad, Mumbai, Pune, Remote"

DHANVEE_ROLES = [
    {
        "title": "Business Development Partner — Dhanvee (Fintech Beta)",
        "domain": "Digital Marketing",
        "description": (
            "Drive city-level borrower & lender community partnerships, campus outreach, and "
            "merchant/SME ecosystem onboarding for Dhanvee (dhanvee.info / dhanvee.online) "
            "across Bangalore, Chennai, Delhi NCR, Hyderabad, Mumbai, Pune, and Remote. "
            "This is a 3-month performance-based incubation internship aligned with DBERT Growth & Business Operations."
        ),
        "responsibilities": (
            "• Identify and onboard local borrower/lender community leads and partner networks.\n"
            "• Conduct product walkthroughs and gather structured beta feedback from early adopters.\n"
            "• Coordinate with the Dhanvee operations team to track city funnel conversion."
        ),
        "skills": "B2B/B2C Partnerships, Structured Communication, CRM & Funnel Tracking, Fintech Literacy",
        "eligibility": "Open to undergraduates, freshers, and DBERT fellows available for a 3-month sprint.",
    },
    {
        "title": "Machine Learning Analyst — Dhanvee (Fintech Beta)",
        "domain": "Data Analyst",
        "description": (
            "Analyze borrower/lender marketplace cohorts, build risk-explainability features, and "
            "evaluate credit-scoring prototypes with strict data hygiene for Dhanvee (dhanvee.info / dhanvee.online) "
            "across Bangalore, Chennai, Delhi NCR, Hyderabad, Mumbai, Pune, and Remote. "
            "This is a 3-month performance-based incubation internship aligned with DBERT Data & ML Analytics."
        ),
        "responsibilities": (
            "• Perform exploratory data analysis and cohort diagnostics on marketplace funnels.\n"
            "• Design interpretable scoring metrics and guard against data leakage.\n"
            "• Build executive dashboards and validation reports for model governance."
        ),
        "skills": "Python / Pandas, SQL, Scikit-Learn, SHAP / Explainable AI",
        "eligibility": "Open to learners with Python/SQL fundamentals and interest in explainable fintech analytics.",
    },
    {
        "title": "AI Agent Developer — Dhanvee (Fintech Beta)",
        "domain": "AI Agent Development",
        "description": (
            "Build grounded, citation-enforced LLM agents and workflow automations for onboarding "
            "support, document triage, and compliance-safe Q&A at Dhanvee (dhanvee.info / dhanvee.online) "
            "across Bangalore, Chennai, Delhi NCR, Hyderabad, Mumbai, Pune, and Remote. "
            "This is a 3-month performance-based incubation internship aligned with DBERT AI Agent Development."
        ),
        "responsibilities": (
            "• Architect RAG pipelines over verified Dhanvee policy and disclosure documents.\n"
            "• Implement tool-calling workflows with strict guardrails against unverified claims.\n"
            "• Evaluate agent accuracy, latency, and hallucination rates across test suites."
        ),
        "skills": "LLM Orchestration, RAG & Vector Search, TypeScript / Python, Prompt Evaluation",
        "eligibility": "Open to AI builders comfortable with Python/TypeScript and LLM tool-calling.",
    },
    {
        "title": "Python Developer — Dhanvee (Fintech Beta)",
        "domain": "Python Automation",
        "description": (
            "Develop idempotent backend services, settlement reconciliation scripts, and automated "
            "data pipelines powering Dhanvee operations (dhanvee.info / dhanvee.online) across "
            "Bangalore, Chennai, Delhi NCR, Hyderabad, Mumbai, Pune, and Remote. "
            "This is a 3-month performance-based incubation internship aligned with DBERT Python Automation & Backend."
        ),
        "responsibilities": (
            "• Build reliable API integrations and webhook processors with idempotency keys.\n"
            "• Write memory-safe streaming parsers for financial and operational CSV/JSON feeds.\n"
            "• Maintain automated test suites and clean environment-driven configuration."
        ),
        "skills": "Python 3.11+, FastAPI / REST APIs, PostgreSQL, Automated Testing",
        "eligibility": "Open to Python developers ready to ship production-tested backend automation.",
    },
]


def seed():
    ts = now_str()
    apply_by = (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d")
    expires_at = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        ensure_column(conn, "companies", "max_live_posts", "INTEGER DEFAULT 3")
        existing = conn.execute(
            "SELECT * FROM companies WHERE LOWER(email)=LOWER(?)", (DHANVEE_EMAIL,)
        ).fetchone()

        if existing:
            company = row_to_dict(existing)
            company_id = company["id"]
            conn.execute(
                "UPDATE companies SET name=?, website=?, about=?, is_approved=1, is_active=1, "
                "max_live_posts=20, updated_at=? WHERE id=?",
                (DHANVEE_NAME, DHANVEE_WEBSITE, DHANVEE_ABOUT, ts, company_id),
            )
            print(f"[company] Updated existing Dhanvee company id={company_id} ({DHANVEE_EMAIL})")
        else:
            temp_pwd = secrets.token_urlsafe(12)
            cur = conn.execute(
                "INSERT INTO companies (name, email, website, about, password_hash, "
                "is_approved, is_active, max_live_posts, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, 1, 1, 20, ?, ?)",
                (
                    DHANVEE_NAME,
                    DHANVEE_EMAIL,
                    DHANVEE_WEBSITE,
                    DHANVEE_ABOUT,
                    hash_password(temp_pwd),
                    ts,
                    ts,
                ),
            )
            company_id = cur.lastrowid
            print(f"[company] Created Dhanvee company id={company_id} ({DHANVEE_EMAIL}) | temp_pwd={temp_pwd}")

        seeded = []
        for role in DHANVEE_ROLES:
            slug = _post_slugify(role["title"])
            existing_post = conn.execute(
                "SELECT id FROM posts WHERE company_id=? AND title=? AND status != 'deleted'",
                (company_id, role["title"]),
            ).fetchone()

            if existing_post:
                post_id = existing_post["id"] if isinstance(existing_post, dict) else existing_post[0]
                conn.execute(
                    "UPDATE posts SET post_type='internship', domain=?, slug=?, description=?, "
                    "responsibilities=?, skills=?, location=?, work_mode='Hybrid / Remote', "
                    "stipend_min=NULL, stipend_max=NULL, pay_period='', is_unpaid=1, "
                    "duration='3 Months', openings=5, apply_by=?, certifications_json=?, "
                    "eligibility=?, status='published', published_at=COALESCE(published_at, ?), "
                    "expires_at=?, updated_at=? WHERE id=?",
                    (
                        role["domain"],
                        slug,
                        role["description"],
                        role["responsibilities"],
                        role["skills"],
                        HUB_CITIES_LABEL,
                        apply_by,
                        json.dumps([]),
                        role["eligibility"],
                        ts,
                        expires_at,
                        ts,
                        post_id,
                    ),
                )
                action = "updated"
            else:
                cur = conn.execute(
                    "INSERT INTO posts (company_id, post_type, domain, title, slug, description, "
                    "responsibilities, skills, location, work_mode, stipend_min, stipend_max, "
                    "pay_period, is_unpaid, duration, openings, apply_by, certifications_json, "
                    "eligibility, status, published_at, expires_at, created_at, updated_at) "
                    "VALUES (?, 'internship', ?, ?, ?, ?, ?, ?, ?, 'Hybrid / Remote', "
                    "NULL, NULL, '', 1, '3 Months', 5, ?, ?, ?, 'published', ?, ?, ?, ?)",
                    (
                        company_id,
                        role["domain"],
                        role["title"],
                        slug,
                        role["description"],
                        role["responsibilities"],
                        role["skills"],
                        HUB_CITIES_LABEL,
                        apply_by,
                        json.dumps([]),
                        role["eligibility"],
                        ts,
                        expires_at,
                        ts,
                        ts,
                    ),
                )
                post_id = cur.lastrowid
                action = "created"

            url = f"https://lms.dbert.in/internships/{slug}-{post_id}"
            seeded.append((post_id, role["title"], url, action))

        conn.commit()

    for pid, title, url, action in seeded:
        print(f"[post:{action}] id={pid} | {title} -> {url}")


if __name__ == "__main__":
    seed()
