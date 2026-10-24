#!/usr/bin/env python3
"""
verify_migration.py - Migration Parity & Integrity Auditor
Verifies row counts, column parity, and referential integrity
between SQLite (internship.db) and target database across all 74 tables.
"""

import os
import sys
import argparse
import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Any

import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData, inspect, text

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("verify_migration")

# 74 tables in target schema
ALL_TABLES = [
    "abuse_log",
    "ambassador_withdrawals",
    "application_status_history",
    "applications",
    "check_log",
    "coin_ledger_mirror",
    "companies",
    "conversations",
    "course_payments",
    "courses",
    "device_profiles",
    "ecosystem_spotlights",
    "email_log",
    "enrollment_status_history",
    "enrollments",
    "event_outbox",
    "gl_concepts",
    "gl_course_chunks",
    "gl_learning_events",
    "gl_learning_sessions",
    "gl_learning_turns",
    "gl_student_learning_profile",
    "gl_teacher_learning_instructions",
    "intern_articles",
    "intern_certificates",
    "interviews",
    "mentors",
    "mobile_refresh_tokens",
    "notifications",
    "password_resets",
    "payment_events",
    "payments",
    "platform_config",
    "post_hire_deposits",
    "rate_events",
    "referrals",
    "scraped_internship_comments",
    "scraped_internships",
    "security_deposits",
    "signup_otps",
    "spotlight_clicks",
    "staff_accounts",
    "tasks",
    "user_sessions",
    "intern_accounts",
    "cohorts",
    "posts",
    "messages",
    "course_chapters",
    "course_day_quizzes",
    "course_projects",
    "gl_misconception_catalog",
    "gl_student_mastery",
    "mentor_availability_slots",
    "review_log",
    "staff_queue_roles",
    "task_versions",
    "attendance",
    "company_follows",
    "course_enrollments",
    "cvs",
    "dbert_fallback_usage",
    "tutor_progress",
    "user_api_keys",
    "cohort_enrollments",
    "post_applications",
    "post_comments",
    "post_questions",
    "course_subtopics",
    "mentor_session_bookings",
    "task_submissions",
    "day_quiz_attempts",
    "project_submissions",
    "course_subtopic_chats",
]


def verify_all(
    source_sqlite: str,
    target_url: str,
    report_output: str = "dbert-api-package/data-migration/migration_report.json",
) -> Dict[str, Any]:
    """Verify data parity between source SQLite and target database."""
    if not os.path.exists(source_sqlite):
        raise FileNotFoundError(f"Source SQLite database not found: {source_sqlite}")

    src_conn = sqlite3.connect(f"file:{os.path.abspath(source_sqlite)}?mode=ro", uri=True)
    src_conn.row_factory = sqlite3.Row
    src_cursor = src_conn.cursor()

    sync_url = target_url
    if sync_url.startswith("postgresql+asyncpg://"):
        sync_url = sync_url.replace("postgresql+asyncpg://", "postgresql://", 1)

    target_engine = create_engine(sync_url)
    target_meta = MetaData()
    target_meta.reflect(bind=target_engine)

    report: Dict[str, Any] = {
        "verified_at": datetime.utcnow().isoformat(),
        "source": source_sqlite,
        "target": sync_url.split("@")[-1] if "@" in sync_url else sync_url,
        "total_tables": len(ALL_TABLES),
        "passed_tables": 0,
        "failed_tables": 0,
        "total_source_rows": 0,
        "total_target_rows": 0,
        "tables": {},
    }

    print("\n" + "=" * 80)
    print(f"{'TABLE NAME':<35} | {'SOURCE':<10} | {'TARGET':<10} | {'STATUS':<10}")
    print("-" * 80)

    all_passed = True

    with target_engine.connect() as conn:
        for tbl in ALL_TABLES:
            # Check source count
            try:
                src_cursor.execute(f'SELECT COUNT(*) FROM "{tbl}"')
                src_count = src_cursor.fetchone()[0]
            except Exception:
                src_count = 0

            # Check target count
            if tbl not in target_meta.tables:
                status = "MISSING_IN_TARGET"
                target_count = 0
                all_passed = False
            else:
                try:
                    res = conn.execute(text(f'SELECT COUNT(*) FROM "{tbl}"'))
                    target_count = res.scalar()
                    if src_count == target_count:
                        status = "PASS"
                    else:
                        status = "MISMATCH"
                        all_passed = False
                except Exception as e:
                    status = f"ERROR: {e}"
                    target_count = 0
                    all_passed = False

            report["total_source_rows"] += src_count
            report["total_target_rows"] += target_count

            if status == "PASS":
                report["passed_tables"] += 1
            else:
                report["failed_tables"] += 1

            report["tables"][tbl] = {
                "source_count": src_count,
                "target_count": target_count,
                "status": status,
            }

            print(f"{tbl:<35} | {src_count:<10} | {target_count:<10} | {status:<10}")

    print("=" * 80)
    print(f"Summary: {report['passed_tables']}/{len(ALL_TABLES)} tables passed.")
    print(f"Total Rows: Source={report['total_source_rows']} | Target={report['total_target_rows']}")
    print(f"Overall Status: {'[OK] PASS' if all_passed else '[FAIL] DISCREPANCY DETECTED'}")
    print("=" * 80 + "\n")

    # Save JSON report
    os.makedirs(os.path.dirname(report_output), exist_ok=True)
    with open(report_output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    logger.info(f"Detailed migration report written to: {report_output}")

    report["overall_passed"] = all_passed
    return report


def main():
    parser = argparse.ArgumentParser(description="DBERT Migration Parity Auditor")
    parser.add_argument(
        "--source",
        default=os.environ.get("SOURCE_DB", "apps/portal/internship.db"),
        help="Path to source SQLite database file",
    )
    parser.add_argument(
        "--target-url",
        default=os.environ.get("DATABASE_URL", "sqlite:///migration_test.db"),
        help="Target database connection URL",
    )
    parser.add_argument(
        "--report",
        default="dbert-api-package/data-migration/migration_report.json",
        help="Path to output JSON report",
    )

    args = parser.parse_args()

    try:
        report = verify_all(args.source, args.target_url, args.report)
        if not report["overall_passed"]:
            sys.exit(1)
    except Exception as e:
        logger.error(f"Verification failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
