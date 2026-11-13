#!/usr/bin/env python3
"""
mark_selected_and_report_48h.py
================================================================================
Updates:
1. All complete Under Review applications -> marked as 'Selected'.
2. All applications rejected due to payment verification not going through -> marked as 'Selected'.
3. Reports total selected intern applications updated in the last 48 hours.

Usage:
  python scripts/mark_selected_and_report_48h.py [--dry-run | --live]
================================================================================
"""

import os
import sys
import argparse
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_url():
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    env_path = "/var/www/dbert-website-lms/apps/portal/.env"
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("DATABASE_URL="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return "postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms"

def main():
    parser = argparse.ArgumentParser(description="Update Under Review and Payment Rejected applications to Selected.")
    parser.add_argument("--live", action="store_true", help="Execute live updates to PostgreSQL database.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate updates without committing.")
    args = parser.parse_args()

    is_live = args.live and not args.dry_run

    db_url = get_db_url()
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
    except Exception as e:
        print(f"Failed to connect to PostgreSQL: {e}")
        sys.exit(1)

    print("=" * 80)
    print("DBERT ADMISSIONS: APPLICATION SELECTION & 48-HOUR TELEMETRY AUDIT")
    print(f"Mode: {'LIVE COMMIT' if is_live else 'DRY RUN (NO CHANGES SAVED)'}")
    print("=" * 80)

    # 1. Complete Under Review Applications
    cur.execute("""
        SELECT id, name, email, phone, domain, college, course, semester, why_join, status, created_at, updated_at
        FROM applications
        WHERE status = 'Under Review'
          AND name IS NOT NULL AND name != ''
          AND email IS NOT NULL AND email != ''
          AND domain IS NOT NULL AND domain != ''
        ORDER BY id ASC;
    """)
    under_review_apps = cur.fetchall()
    print(f"\n1. Complete Under Review Applications Found: {len(under_review_apps)}")
    for a in under_review_apps[:10]:
        print(f"   - [ID {a['id']}] {a['name']} <{a['email']}> | Domain: {a['domain']} | Current: {a['status']}")
    if len(under_review_apps) > 10:
        print(f"   ... and {len(under_review_apps) - 10} more.")

    # 2. Applications with Rejected Payment Verification
    cur.execute("""
        SELECT DISTINCT a.id, a.name, a.email, a.phone, a.domain, a.status, a.created_at, a.updated_at,
               e.id as enr_id, e.payment_status, e.admin_note as enr_note
        FROM enrollments e
        JOIN applications a ON (e.application_id = a.id OR (e.application_id IS NULL AND LOWER(e.email) = LOWER(a.email) AND e.domain = a.domain))
        WHERE e.payment_status = 'Rejected'
          AND a.status != 'Selected'
        ORDER BY a.id ASC;
    """)
    payment_rejected_apps = cur.fetchall()
    print(f"\n2. Applications with Rejected Payment Verification (not currently Selected): {len(payment_rejected_apps)}")
    for a in payment_rejected_apps[:10]:
        print(f"   - [ID {a['id']}] {a['name']} <{a['email']}> | Domain: {a['domain']} | Current: {a['status']} | Enr Note: {a['enr_note']}")
    if len(payment_rejected_apps) > 10:
        print(f"   ... and {len(payment_rejected_apps) - 10} more.")

    # Combine unique application IDs to update
    to_update_dict = {}
    for a in under_review_apps:
        to_update_dict[a["id"]] = {
            "record": a,
            "reason": "Admin Batch Approval: Complete Under Review Profile Approved"
        }
    for a in payment_rejected_apps:
        if a["id"] not in to_update_dict:
            to_update_dict[a["id"]] = {
                "record": a,
                "reason": "Payment Re-Verification Reset: Re-opened to Selected for valid payment proof re-submission"
            }

    all_target_ids = list(to_update_dict.keys())
    print(f"\nTotal Unique Applications to Mark as 'Selected': {len(all_target_ids)}")

    if is_live and all_target_ids:
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        # Perform update
        cur.execute("""
            UPDATE applications
            SET status = 'Selected',
                reviewed_at = %s,
                updated_at = %s
            WHERE id = ANY(%s);
        """, (now_str, now_str, all_target_ids))
        updated_rows = cur.rowcount
        print(f"Successfully updated {updated_rows} applications to 'Selected' in applications table.")

        # Log status history
        history_records = [
            (aid, data["record"]["status"], "Selected", "system_admissions_batch", now_str, data["reason"])
            for aid, data in to_update_dict.items()
        ]
        cur.executemany("""
            INSERT INTO application_status_history (application_id, old_status, new_status, changed_by, changed_at, reason)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, history_records)
        print(f"Successfully logged {len(history_records)} audit history transitions.")

        conn.commit()
        print("Database transaction successfully committed.")
    elif not is_live:
        print("\n[DRY RUN]: No changes were written to the database. Use --live to execute.")

    # 3. Telemetry: Selected applications updated in the last 48 hours
    cur.execute("""
        SELECT id, name, email, phone, domain, status, reviewed_at, updated_at
        FROM applications
        WHERE status = 'Selected'
          AND updated_at::timestamp >= (NOW() - INTERVAL '48 hours')
        ORDER BY updated_at DESC;
    """)
    selected_48h = cur.fetchall()

    print("\n" + "=" * 80)
    print(f"TOTAL SELECTED INTERNS APPLICATIONS UPDATED IN LAST 48 HOURS: {len(selected_48h)}")
    print("=" * 80)

    # Domain breakdown of the 48-hour Selected cohort
    domain_counts = {}
    for a in selected_48h:
        dom = a["domain"] or "Undeclared"
        domain_counts[dom] = domain_counts.get(dom, 0) + 1

    print("\nDomain Distribution of 48-Hour Selected Cohort:")
    for dom, cnt in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  * {dom}: {cnt} candidates")

    # Sample listing of the most recently updated
    print("\nMost Recently Updated Selected Applications (Top 15):")
    for a in selected_48h[:15]:
        print(f"  * ID {a['id']}: {a['name']} <{a['email']}> | Domain: {a['domain']} | Updated: {a['updated_at']}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
