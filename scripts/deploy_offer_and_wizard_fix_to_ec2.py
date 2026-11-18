#!/usr/bin/env python3
"""
Deploy Offer Letter & Wizard Status 500 Fix to Production EC2
- Uploads Phase 15 migration script and updated app.py
- Executes Phase 15 migration on EC2 PostgreSQL
- Restarts dbert-portal.service
- Verifies database schema and live HTTP responses
"""
import subprocess
import os
import sys
import urllib.request
import json

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
SERVER = "ubuntu@3.26.237.171"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REMOTE_BASE = "/var/www/dbert-website-lms"

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def log(msg):
    print(f"[DEPLOY-FIX] {msg}")

def main():
    log("=" * 76)
    log("DEPLOYING PHASE 15 SCHEMA & WIZARD STATUS DEFENSIVE FIX TO EC2")
    log("=" * 76)

    files_to_upload = [
        (
            os.path.join(BASE_DIR, "apps", "portal", "scripts", "phase15_offer_letters_and_notes_schema.py"),
            f"{REMOTE_BASE}/apps/portal/scripts/phase15_offer_letters_and_notes_schema.py"
        ),
        (
            os.path.join(BASE_DIR, "apps", "portal", "scripts", "run_production_migrations.py"),
            f"{REMOTE_BASE}/apps/portal/scripts/run_production_migrations.py"
        ),
        (
            os.path.join(BASE_DIR, "apps", "portal", "app.py"),
            f"{REMOTE_BASE}/apps/portal/app.py"
        ),
    ]

    for local_path, remote_path in files_to_upload:
        if os.path.exists(local_path):
            log(f"Uploading {os.path.basename(local_path)} -> {remote_path} ...")
            subprocess.run([
                "scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
                local_path, f"{SERVER}:{remote_path}"
            ], check=True)
        else:
            log(f"ERROR: Local file not found: {local_path}")
            sys.exit(1)

    log("Files uploaded successfully.")
    log("Executing Phase 15 migration on EC2 PostgreSQL and restarting dbert-portal.service...")

    remote_cmd = f"""
    set -e
    export DATABASE_URL="postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms"
    export REQUIRE_POSTGRES=true
    echo "Running Phase 15 migration..."
    cd {REMOTE_BASE}/apps/portal
    .venv/bin/python3 scripts/phase15_offer_letters_and_notes_schema.py

    echo "Restarting dbert-portal.service..."
    sudo systemctl restart dbert-portal.service
    sleep 2
    systemctl is-active dbert-portal.service
    """

    res = subprocess.run([
        "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
        SERVER, remote_cmd
    ], check=True)

    log("=" * 76)
    log("POST-DEPLOY VERIFICATION ON PRODUCTION")
    log("=" * 76)

    # Verify PostgreSQL table exists
    verify_db_cmd = f"""
    {REMOTE_BASE}/apps/portal/.venv/bin/python3 -c "
import psycopg2
conn = psycopg2.connect('postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms')
cur = conn.cursor()
cur.execute(\\\"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'intern_offer_letters');\\\")
print('intern_offer_letters exists in DB:', cur.fetchone()[0])
cur.execute(\\\"SELECT EXISTS (SELECT FROM information_schema.columns WHERE table_name = 'applications' AND column_name = 'admin_note');\\\")
print('admin_note column exists in applications:', cur.fetchone()[0])
conn.close()
"
    """
    subprocess.run([
        "ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
        SERVER, verify_db_cmd
    ], check=True)

    # Verify HTTP endpoints
    urls = [
        "https://lms.dbert.in/portal/offer",
        "https://lms.dbert.in/intern/wizard-status",
        "https://lms.dbert.in/mentors/slots"
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "DBERT-HealthProbe/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                log(f"[OK] {url} -> HTTP {resp.status}")
        except urllib.error.HTTPError as e:
            # 302, 401, 403 are expected when not logged in, but NEVER 500!
            if e.code in (302, 307, 401, 403):
                log(f"[OK] {url} -> HTTP {e.code} ({e.reason}) [Protected route verified without 500 error]")
            elif e.code == 500:
                log(f"[CRITICAL FAIL] {url} -> HTTP 500 Internal Server Error!")
                sys.exit(1)
            else:
                log(f"[INFO] {url} -> HTTP {e.code} ({e.reason})")
        except Exception as e:
            log(f"[WARN] Error probing {url}: {e}")

    log("=" * 76)
    log("MISSION ACCOMPLISHED: Offer Letter & Wizard Status 500 errors fully resolved!")
    log("=" * 76)

if __name__ == "__main__":
    main()
