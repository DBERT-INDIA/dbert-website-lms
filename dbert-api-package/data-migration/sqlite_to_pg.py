#!/usr/bin/env python3
"""
sqlite_to_pg.py - Comprehensive Data Migration Tool
Migrates all 74 tables from SQLite (internship.db) to PostgreSQL (or target DB)
with topological dependency ordering, type casting, batching, and sequence sync.
"""

import os
import sys
import argparse
import sqlite3
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData, Table, inspect, text, Boolean, DateTime, Integer, BigInteger, JSON, Float

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sqlite_to_pg")

# 74 Tables in strict topological order (dependencies first)
TABLES_IN_ORDER = [
    # 0 dependencies (base parent tables)
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
    # 1 dependency
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
    # 2 dependencies
    "attendance",
    "company_follows",
    "course_enrollments",
    "cvs",
    "dbert_fallback_usage",
    "tutor_progress",
    "user_api_keys",
    # 3+ dependencies
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


def parse_datetime(val: Any) -> Optional[datetime]:
    """Parse various SQLite date/datetime string formats into datetime objects."""
    if val is None or val == "":
        return None
    if isinstance(val, datetime):
        return val
    val_str = str(val).strip()
    # Try ISO format
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(val_str, fmt)
        except ValueError:
            pass
    # Try unix timestamp
    try:
        ts = float(val_str)
        if ts > 100000000000:  # milliseconds
            ts = ts / 1000.0
        return datetime.fromtimestamp(ts)
    except (ValueError, OSError):
        pass
    return None


def transform_value(val: Any, col_type: Any) -> Any:
    """Normalize SQLite value according to the target SQLAlchemy column type."""
    if val is None:
        return None

    # Handle boolean column types
    if isinstance(col_type, Boolean):
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, str):
            val_lower = val.lower().strip()
            return val_lower in ("1", "true", "t", "yes", "y")
        return bool(val)

    # Handle datetime column types
    if isinstance(col_type, DateTime):
        dt = parse_datetime(val)
        return dt if dt is not None else val

    # Handle JSON column types
    if isinstance(col_type, JSON):
        if isinstance(val, (dict, list)):
            return val
        if isinstance(val, str):
            try:
                return json.loads(val)
            except Exception:
                return val
        return val

    # Handle float / numeric types
    if isinstance(col_type, Float):
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    # Handle integer types
    if isinstance(col_type, (Integer, BigInteger)):
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    return val


def migrate_database(
    source_sqlite: str,
    target_url: str,
    batch_size: int = 1000,
    clean_target: bool = False,
    tables_to_migrate: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Execute end-to-end migration from SQLite to target database."""
    if not os.path.exists(source_sqlite):
        raise FileNotFoundError(f"Source SQLite database not found: {source_sqlite}")

    logger.info(f"Connecting to source SQLite: {source_sqlite}")
    src_conn = sqlite3.connect(f"file:{os.path.abspath(source_sqlite)}?mode=ro", uri=True)
    src_conn.row_factory = sqlite3.Row
    src_cursor = src_conn.cursor()

    # Normalize target URL for sync execution (e.g. asyncpg -> psycopg2 or psycopg)
    sync_url = target_url
    if sync_url.startswith("postgresql+asyncpg://"):
        sync_url = sync_url.replace("postgresql+asyncpg://", "postgresql://", 1)

    logger.info(f"Connecting to target database: {sync_url.split('@')[-1] if '@' in sync_url else sync_url}")
    target_engine = create_engine(sync_url)
    target_meta = MetaData()
    target_meta.reflect(bind=target_engine)
    is_postgres = target_engine.dialect.name == "postgresql"

    # Determine tables to process
    target_tables = TABLES_IN_ORDER
    if tables_to_migrate:
        target_tables = [t for t in TABLES_IN_ORDER if t in tables_to_migrate]

    # Clean target if requested
    if clean_target:
        logger.info("Cleaning existing target data (reverse topological order)...")
        with target_engine.begin() as conn:
            for tbl_name in reversed(TABLES_IN_ORDER):
                if tbl_name in target_meta.tables:
                    if is_postgres:
                        conn.execute(text(f'TRUNCATE TABLE "{tbl_name}" CASCADE;'))
                    else:
                        conn.execute(text(f'DELETE FROM "{tbl_name}";'))
        logger.info("Target database cleaned.")

    results = {}
    start_time = datetime.now()
    total_migrated_rows = 0

    for idx, table_name in enumerate(target_tables, 1):
        # Verify table exists in source
        src_cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        if not src_cursor.fetchone():
            logger.warning(f"[{idx}/{len(target_tables)}] Table '{table_name}' not found in SQLite source. Skipping.")
            results[table_name] = {"status": "skipped", "reason": "not_in_source", "rows": 0}
            continue

        # Verify table exists in target
        if table_name not in target_meta.tables:
            logger.warning(f"[{idx}/{len(target_tables)}] Table '{table_name}' not found in target schema. Skipping.")
            results[table_name] = {"status": "skipped", "reason": "not_in_target", "rows": 0}
            continue

        target_table = target_meta.tables[table_name]
        target_col_map = {c.name: c.type for c in target_table.columns}

        # Query source count
        src_cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        src_count = src_cursor.fetchone()[0]

        if src_count == 0:
            logger.info(f"[{idx}/{len(target_tables)}] '{table_name}': 0 rows (empty table).")
            results[table_name] = {"status": "success", "rows": 0}
            continue

        logger.info(f"[{idx}/{len(target_tables)}] Migrating '{table_name}' ({src_count} rows)...")

        # Read source data
        src_cursor.execute(f'SELECT * FROM "{table_name}"')
        rows = src_cursor.fetchall()

        # Batch insert
        inserted_for_table = 0
        batch = []
        with target_engine.begin() as conn:
            for row in rows:
                row_dict = dict(row)
                transformed = {}
                for col_name, raw_val in row_dict.items():
                    if col_name in target_col_map:
                        transformed[col_name] = transform_value(raw_val, target_col_map[col_name])

                batch.append(transformed)

                if len(batch) >= batch_size:
                    conn.execute(target_table.insert(), batch)
                    inserted_for_table += len(batch)
                    batch = []

            if batch:
                conn.execute(target_table.insert(), batch)
                inserted_for_table += len(batch)

            # Sequence synchronization for PostgreSQL
            if is_postgres:
                pk_cols = [c.name for c in target_table.primary_key.columns]
                if pk_cols and len(pk_cols) == 1:
                    pk_name = pk_cols[0]
                    try:
                        seq_sql = f"""
                            SELECT setval(
                                pg_get_serial_sequence('{table_name}', '{pk_name}'),
                                COALESCE((SELECT MAX("{pk_name}") FROM "{table_name}"), 1)
                            );
                        """
                        conn.execute(text(seq_sql))
                    except Exception as e:
                        logger.debug(f"Sequence sync skipped for {table_name}.{pk_name}: {e}")

        total_migrated_rows += inserted_for_table
        logger.info(f"[{idx}/{len(target_tables)}] '{table_name}' migrated: {inserted_for_table}/{src_count} rows.")
        results[table_name] = {"status": "success", "rows": inserted_for_table}

    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info(f"Migration completed in {elapsed:.2f}s! Total rows: {total_migrated_rows}")

    return {
        "success": True,
        "elapsed_seconds": elapsed,
        "total_rows": total_migrated_rows,
        "tables": results,
    }


def main():
    parser = argparse.ArgumentParser(description="DBERT SQLite to PostgreSQL Migration CLI")
    parser.add_argument(
        "--source",
        default=os.environ.get("SOURCE_DB", "apps/portal/internship.db"),
        help="Path to source SQLite database file",
    )
    parser.add_argument(
        "--target-url",
        default=os.environ.get("DATABASE_URL", "sqlite:///migration_test.db"),
        help="Target database connection URL (PostgreSQL or SQLite)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Batch insert chunk size",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Truncate target tables before migration",
    )
    parser.add_argument(
        "--tables",
        type=str,
        default=None,
        help="Comma-separated list of specific tables to migrate",
    )

    args = parser.parse_args()
    tables_list = [t.strip() for t in args.tables.split(",")] if args.tables else None

    try:
        report = migrate_database(
            source_sqlite=args.source,
            target_url=args.target_url,
            batch_size=args.batch_size,
            clean_target=args.clean,
            tables_to_migrate=tables_list,
        )
        print("\n=== MIGRATION SUMMARY ===")
        print(f"Total Rows Migrated: {report['total_rows']}")
        print(f"Elapsed Time: {report['elapsed_seconds']:.2f}s")
        print("Status: SUCCESS")
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
