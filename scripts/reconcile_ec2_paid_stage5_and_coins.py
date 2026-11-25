#!/usr/bin/env python3
"""
scripts/reconcile_ec2_paid_stage5_and_coins.py
Stage 3 Reconciliation Script:
1. Backs up affected intern_accounts rows to data/backup_stage5_reconcile_<ts>.json
2. Reconciles ONLY verified/accepted paid/enrolled interns (signup_stage < 5) -> signup_stage = 5
   (Leaves unselected/rejected rows untouched per approved plan.)
3. Idempotently credits 5,499 coins into coin_ledger_mirror (ledger_kind='referral',
   reason='stipend_release_5499') for interns with stipend_verified=1 and stipend_amount=5499
   who do not yet have that ledger entry.

Usage:
  python scripts/reconcile_ec2_paid_stage5_and_coins.py --dry-run
  python scripts/reconcile_ec2_paid_stage5_and_coins.py --apply
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import psycopg2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    args = parser.parse_args()

    portal_dir = Path("/var/www/dbert-website-lms/apps/portal")
    env_file = portal_dir / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()
    cur.execute("SET search_path TO dbert_internship, public;")

    # 1. Find paid/enrolled real interns with signup_stage < 5
    cur.execute("""
        SELECT ia.id, ia.email, ia.signup_stage, ia.account_status, a.status AS app_status, e.payment_status
        FROM intern_accounts ia
        LEFT JOIN applications a ON ia.application_id = a.id
        LEFT JOIN LATERAL (
            SELECT payment_status
            FROM enrollments e2
            WHERE LOWER(e2.email) = LOWER(ia.email)
              AND e2.payment_status IN ('Verified', 'Accepted')
            ORDER BY id DESC LIMIT 1
        ) e ON true
        WHERE LOWER(ia.email) NOT LIKE '%%@dbert.test'
          AND LOWER(ia.email) NOT LIKE '%%@test.com'
          AND (ia.signup_stage IS NULL OR ia.signup_stage < 5)
          AND (e.payment_status IN ('Verified', 'Accepted') OR a.status = 'Enrolled')
        ORDER BY ia.id
    """)
    stage5_targets = cur.fetchall()

    # 2. Find stipend_verified=1 & stipend_amount=5499 interns missing stipend_release_5499 in coin_ledger_mirror
    cur.execute("""
        SELECT ia.id, ia.email, ia.stipend_amount
        FROM intern_accounts ia
        WHERE LOWER(ia.email) NOT LIKE '%%@dbert.test'
          AND LOWER(ia.email) NOT LIKE '%%@test.com'
          AND ia.stipend_verified = 1
          AND COALESCE(ia.stipend_amount, 0) >= 5499
          AND NOT EXISTS (
              SELECT 1 FROM coin_ledger_mirror cl
              WHERE cl.intern_id = ia.id AND cl.reason = 'stipend_release_5499'
          )
        ORDER BY ia.id
    """)
    coin_targets = cur.fetchall()

    print(f"[{'APPLY' if args.apply else 'DRY-RUN'}] Paid/Enrolled interns to reconcile to signup_stage=5: {len(stage5_targets)}")
    print(f"[{'APPLY' if args.apply else 'DRY-RUN'}] stipend_verified=1 (5499) interns to credit in coin_ledger_mirror: {len(coin_targets)}")

    if not args.apply:
        conn.close()
        return

    # Backup affected rows
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("/var/www/dbert-website-lms/data")
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_file = backup_dir / f"backup_stage5_reconcile_{ts}.json"
    backup_payload = {
        "timestamp": ts,
        "stage5_targets": [
            {"id": r[0], "email": r[1], "old_signup_stage": r[2], "old_account_status": r[3], "app_status": r[4], "payment_status": r[5]}
            for r in stage5_targets
        ],
        "coin_targets": [{"id": r[0], "email": r[1], "stipend_amount": r[2]} for r in coin_targets],
    }
    backup_file.write_text(json.dumps(backup_payload, indent=2), encoding="utf-8")
    print(f"Backup written to {backup_file}")

    # Apply Stage 5 reconciliation
    for r in stage5_targets:
        cur.execute("UPDATE intern_accounts SET signup_stage = 5 WHERE id = %s", (r[0],))

    # Apply 5,499 coin credits
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for iid, email, amt in coin_targets:
        cur.execute(
            """
            INSERT INTO coin_ledger_mirror (intern_id, email, delta, ledger_kind, reason, event_ts, idem_key)
            VALUES (%s, %s, %s, 'referral', 'stipend_release_5499', %s, %s)
            ON CONFLICT (idem_key) DO NOTHING
            """,
            (iid, email.lower(), int(amt), now_str, f"stipend_release_5499_{iid}"),
        )

    conn.commit()
    conn.close()
    print(f"SUCCESS: Updated {len(stage5_targets)} interns to signup_stage=5 and credited {len(coin_targets)} stipend_release_5499 ledger entries.")


if __name__ == "__main__":
    main()
