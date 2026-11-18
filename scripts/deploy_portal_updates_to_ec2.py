#!/usr/bin/env python3
"""
deploy_portal_updates_to_ec2.py
Deploys updated portal files for:
1. Universal BYOK Gemini API key resolution & pre-flight gating
2. Course-style full-page bounty guide (/tasks/<id>/guide)
3. Modal layout & sidebar offset fix on /stipend/tasks
4. Offer letter display and digital signing (/portal/offer, /portal/offer/sign, /portal/offer/print)
5. Syncs files to /var/www/dbert-website-lms/apps/portal and restarts dbert-portal.service
"""

import os
import subprocess
import sys
import time

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"

FILES_TO_DEPLOY = [
    # Services
    ("apps/portal/services/ai/stipend_evaluator.py", f"{REMOTE_PORTAL_DIR}/services/ai/stipend_evaluator.py"),
    ("apps/portal/services/ai/bounty_content_generator.py", f"{REMOTE_PORTAL_DIR}/services/ai/bounty_content_generator.py"),
    # Core app
    ("apps/portal/app.py", f"{REMOTE_PORTAL_DIR}/app.py"),
    # Templates
    ("apps/portal/templates/portal.html", f"{REMOTE_PORTAL_DIR}/templates/portal.html"),
    ("apps/portal/templates/task_guide.html", f"{REMOTE_PORTAL_DIR}/templates/task_guide.html"),
    ("apps/portal/templates/tasks_list.html", f"{REMOTE_PORTAL_DIR}/templates/tasks_list.html"),
    ("apps/portal/templates/account_gemini_key.html", f"{REMOTE_PORTAL_DIR}/templates/account_gemini_key.html"),
    ("apps/portal/templates/stipend_tasks.html", f"{REMOTE_PORTAL_DIR}/templates/stipend_tasks.html"),
    ("apps/portal/templates/portal_offer_letter.html", f"{REMOTE_PORTAL_DIR}/templates/portal_offer_letter.html"),
    ("apps/portal/templates/portal_offer_print.html", f"{REMOTE_PORTAL_DIR}/templates/portal_offer_print.html"),
    # Static CSS
    ("apps/portal/static/css/portal-offer.css", f"{REMOTE_PORTAL_DIR}/static/css/portal-offer.css"),
]

def run_cmd(cmd, check=True):
    print(f"[RUN] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        print(f"[STDERR] {res.stderr.strip()}", file=sys.stderr)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with returncode {res.returncode}: {cmd}")
    return res

def main():
    print("=== Deploying Portal Updates to Production EC2 ===")
    
    # 1. SCP each file
    for local_path, remote_path in FILES_TO_DEPLOY:
        if not os.path.exists(local_path):
            print(f"[SKIP] Local file not found: {local_path}")
            continue
        print(f"Uploading {local_path} -> {remote_path}...")
        scp_cmd = f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes "{local_path}" {HOST}:{remote_path}'
        run_cmd(scp_cmd)

    # 2. Ensure Phase 15 table exists on remote postgres
    print("Ensuring intern_offer_letters table exists on remote...")
    remote_script = (
        "python3 -c \\\"from services.database.adapter import get_db_adapter; "
        "conn = get_db_adapter(); "
        "conn.execute('''CREATE TABLE IF NOT EXISTS intern_offer_letters ("
        "id SERIAL PRIMARY KEY, "
        "offer_letter_id TEXT UNIQUE NOT NULL, "
        "intern_id INTEGER, "
        "enrollment_id INTEGER, "
        "email TEXT NOT NULL, "
        "name TEXT NOT NULL, "
        "domain TEXT NOT NULL, "
        "college TEXT, "
        "batch_start_date TEXT NOT NULL, "
        "batch_end_date TEXT NOT NULL, "
        "tenure_months INTEGER DEFAULT 2, "
        "stipend_amount INTEGER DEFAULT 5000, "
        "login_hours_per_week INTEGER DEFAULT 10, "
        "required_certifications INTEGER DEFAULT 2, "
        "required_bounty_tasks INTEGER DEFAULT 75, "
        "caution_deposit_amount INTEGER DEFAULT 499, "
        "caution_deposit_status TEXT DEFAULT 'VERIFIED', "
        "signature_name TEXT, "
        "accepted_at TEXT, "
        "pdf_unlocked INTEGER DEFAULT 0, "
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
        "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP); "
        "CREATE INDEX IF NOT EXISTS idx_offer_letters_email ON intern_offer_letters(email); "
        "CREATE INDEX IF NOT EXISTS idx_offer_letters_offer_id ON intern_offer_letters(offer_letter_id);'''); "
        "conn.commit(); "
        "print('intern_offer_letters table verified.');\\\""
    )
    ssh_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {HOST} "cd {REMOTE_PORTAL_DIR} && {remote_script}"'
    run_cmd(ssh_cmd, check=False)

    # 3. Restart dbert-portal.service
    print("Restarting dbert-portal.service...")
    restart_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {HOST} "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"'
    run_cmd(restart_cmd)

    # 4. Probe live endpoints
    print("Probing live endpoints...")
    probe_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {HOST} "curl -s -o /dev/null -w \'%{{http_code}}\' http://127.0.0.1:5001/portal/offer"'
    res_probe = run_cmd(probe_cmd, check=False)
    print(f"Direct Gunicorn /portal/offer HTTP status: {res_probe.stdout.strip()} (Expected: 302 redirect to signin)")

    probe_guide = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {HOST} "curl -s -o /dev/null -w \'%{{http_code}}\' http://127.0.0.1:5001/tasks/101/guide"'
    res_guide = run_cmd(probe_guide, check=False)
    print(f"Direct Gunicorn /tasks/101/guide HTTP status: {res_guide.stdout.strip()} (Expected: 302 redirect to signin)")

    print("=== Deployment Complete! ===")

if __name__ == "__main__":
    main()
