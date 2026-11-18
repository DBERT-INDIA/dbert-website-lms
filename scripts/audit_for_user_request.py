#!/usr/bin/env python3
"""
Inspect EC2 database for:
1. Applications under review
2. Rejected payments in enrollments
3. Users who logged in in the last 48 hours
4. Status of all 4 stipend gates
5. GitHub repositories / organization settings
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime, timedelta

DB_URL = "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms"

def main():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    now = datetime.now()
    since_48h = (now - timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S")

    # 1. Applications Under Review
    cur.execute("SELECT id, name, email, domain, created_at FROM applications WHERE status = 'Under Review'")
    under_review_apps = cur.fetchall()

    # 2. Rejected Payments in Enrollments
    cur.execute("""
        SELECT id, name, email, phone, amount, payment_status, utr, created_at, updated_at
        FROM enrollments
        WHERE payment_status = 'Rejected'
        ORDER BY updated_at DESC
    """)
    rejected_payments = cur.fetchall()

    # 3. Users logged in in last 48 hours
    cur.execute("""
        SELECT id, email, role, created_at, expires_at
        FROM user_sessions
        WHERE created_at >= %s
        ORDER BY created_at DESC
    """, (since_48h,))
    sessions_48h = cur.fetchall()

    unique_active_users = {}
    for s in sessions_48h:
        em = s["email"].lower().strip()
        if em not in unique_active_users:
            unique_active_users[em] = {
                "email": em,
                "role": s["role"],
                "last_login": s["created_at"],
                "session_count": 0
            }
        unique_active_users[em]["session_count"] += 1

    # 4. For active users in last 48h, check their full status (app, enrollment, gates)
    active_user_status = []
    for em, u in unique_active_users.items():
        # Account
        cur.execute("""
            SELECT id, name, email, domain, linkedin_url, github_url, upi_id_encrypted, signup_stage
            FROM intern_accounts
            WHERE LOWER(email) = %s
        """, (em,))
        acct = cur.fetchone()

        # Application
        cur.execute("""
            SELECT id, name, status, domain, created_at
            FROM applications
            WHERE LOWER(email) = %s
            ORDER BY id DESC LIMIT 1
        """, (em,))
        app = cur.fetchone()

        # Enrollment
        cur.execute("""
            SELECT id, payment_status, amount, utr, created_at, updated_at
            FROM enrollments
            WHERE LOWER(email) = %s
            ORDER BY id DESC LIMIT 1
        """, (em,))
        enr = cur.fetchone()

        # Certificate
        cur.execute("""
            SELECT id, cert_id, tier, course_title, issued_at
            FROM intern_certificates
            WHERE LOWER(email) = %s
            ORDER BY id DESC LIMIT 1
        """, (em,))
        cert = cur.fetchone()

        # Article
        art = None
        if acct:
            cur.execute("""
                SELECT id, title, status
                FROM intern_articles
                WHERE intern_id = %s
                ORDER BY id DESC LIMIT 1
            """, (acct["id"],))
            art = cur.fetchone()

        # Gates breakdown:
        # Gate 1: Course Certificate & Verification (tier in ('verified', 'dbert_verified'))
        # Gate 2: Internship Duration / Case Study (article published or joining_date passed)
        # Gate 3: Payout UPI Account (upi_id_encrypted present)
        # Gate 4: Public LinkedIn Experience (linkedin_url present)
        # Plus GitHub contribution check
        g1_cert_verified = bool(cert and cert.get("tier") in ("verified", "dbert_verified"))
        g2_case_study = bool(art and art.get("status") == "published")
        g3_upi_linked = bool(acct and acct.get("upi_id_encrypted"))
        g4_linkedin = bool(acct and acct.get("linkedin_url"))
        has_github = bool(acct and acct.get("github_url"))

        active_user_status.append({
            "email": em,
            "name": acct["name"] if acct else (app["name"] if app else "Unknown"),
            "role": u["role"],
            "last_login": u["last_login"],
            "app_status": app.get("status") if app else "No Application",
            "enr_status": enr.get("payment_status") if enr else "No Enrollment",
            "enr_amount": enr.get("amount") if enr else None,
            "enr_utr": enr.get("utr") if enr else None,
            "g1_cert_verified": g1_cert_verified,
            "g2_case_study": g2_case_study,
            "g3_upi_linked": g3_upi_linked,
            "g4_linkedin": g4_linkedin,
            "has_github": has_github,
            "github_url": acct.get("github_url") if acct else None,
            "linkedin_url": acct.get("linkedin_url") if acct else None
        })

    # 5. Check candidates with ALL 4 GATES COMPLETED across the whole system
    cur.execute("""
        SELECT ia.id, ia.name, ia.email, ia.domain, ia.linkedin_url, ia.github_url,
               ia.upi_id_encrypted,
               ic.tier, ic.cert_id,
               art.status as article_status, art.title as article_title,
               enr.payment_status as enr_payment_status, enr.amount as enr_amount, enr.joining_date
        FROM intern_accounts ia
        LEFT JOIN intern_certificates ic ON (ia.id = ic.intern_id OR LOWER(ia.email) = LOWER(ic.email))
        LEFT JOIN intern_articles art ON ia.id = art.intern_id
        LEFT JOIN enrollments enr ON LOWER(ia.email) = LOWER(enr.email)
        WHERE (ia.linkedin_url IS NOT NULL AND ia.linkedin_url != '')
          AND (ia.github_url IS NOT NULL AND ia.github_url != '')
          AND (ia.upi_id_encrypted IS NOT NULL AND ia.upi_id_encrypted != '')
          AND (ic.tier IN ('verified', 'dbert_verified'))
          AND (art.status = 'published')
    """)
    all_gates_completed = cur.fetchall()

    result = {
        "under_review_count": len(under_review_apps),
        "under_review_apps": [dict(r) for r in under_review_apps],
        "rejected_payments_count": len(rejected_payments),
        "rejected_payments": [dict(r) for r in rejected_payments],
        "active_users_48h_count": len(unique_active_users),
        "active_user_status": active_user_status,
        "all_gates_completed_count": len(all_gates_completed),
        "all_gates_completed": [dict(r) for r in all_gates_completed]
    }

    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    main()
