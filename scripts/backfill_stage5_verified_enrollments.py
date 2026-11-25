"""
scripts/backfill_stage5_verified_enrollments.py

Idempotent backfill script to reconcile `intern_accounts.signup_stage = 5`
for all candidates whose enrollment has `payment_status IN ('Verified', 'Accepted')`.

Usage:
  python scripts/backfill_stage5_verified_enrollments.py --dry-run
  python scripts/backfill_stage5_verified_enrollments.py --live
"""
import argparse
import os
import sys
from pathlib import Path


def load_env(env_path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if env_path.is_file():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill signup_stage=5 for Verified/Accepted enrollments.")
    parser.add_argument("--live", action="store_true", help="Execute UPDATE against database (default is dry-run).")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    env = load_env(repo_root / "apps" / "portal" / ".env")
    db_url = os.environ.get("DATABASE_URL") or env.get("DATABASE_URL")

    if not db_url:
        print("ERROR: DATABASE_URL not found in environment or apps/portal/.env", file=sys.stderr)
        return 1

    import psycopg2

    conn = psycopg2.connect(db_url)
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO dbert_internship, public;")

        cur.execute(
            """
            SELECT COUNT(DISTINCT ia.id)
            FROM intern_accounts ia
            JOIN enrollments e ON LOWER(ia.email) = LOWER(e.email)
            WHERE e.payment_status IN ('Verified', 'Accepted')
              AND COALESCE(ia.signup_stage, 0) < 5
            """
        )
        pending_count = cur.fetchone()[0]
        print(f"Eligible intern_accounts with signup_stage < 5 and Verified/Accepted enrollment: {pending_count}")

        if not args.live:
            print("DRY RUN: No rows modified. Pass --live to apply.")
            return 0

        cur.execute(
            """
            UPDATE intern_accounts ia
            SET signup_stage = 5,
                updated_at = NOW()::text
            FROM enrollments e
            WHERE LOWER(ia.email) = LOWER(e.email)
              AND e.payment_status IN ('Verified', 'Accepted')
              AND COALESCE(ia.signup_stage, 0) < 5
            """
        )
        updated = cur.rowcount
        conn.commit()
        print(f"LIVE UPDATE COMPLETE: Updated {updated} intern_accounts rows to signup_stage = 5.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
