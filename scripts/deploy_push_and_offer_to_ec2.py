#!/usr/bin/env python3
"""
scripts/deploy_push_and_offer_to_ec2.py
Deploys Web Push client CSP fixes, root service worker routing, offer letter routes,
and seeded test persona synchronizations to production EC2.
"""
import subprocess
import sys
import os

PEM_PATH = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"
REMOTE_PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"
REMOTE_WEBSITE_DIR = "/var/www/dbert-website-lms/apps/website"

FILES_TO_UPLOAD = [
    ("apps/portal/app.py", f"{REMOTE_PORTAL_DIR}/app.py"),
    ("apps/portal/templates/account_notifications.html", f"{REMOTE_PORTAL_DIR}/templates/account_notifications.html"),
    ("apps/portal/templates/admin_push_broadcast.html", f"{REMOTE_PORTAL_DIR}/templates/admin_push_broadcast.html"),
    ("apps/portal/templates/portal_offer_letter.html", f"{REMOTE_PORTAL_DIR}/templates/portal_offer_letter.html"),
    ("apps/portal/templates/portal_offer_print.html", f"{REMOTE_PORTAL_DIR}/templates/portal_offer_print.html"),
    ("apps/portal/static/js/dbert-push-client.js", f"{REMOTE_PORTAL_DIR}/static/js/dbert-push-client.js"),
    ("apps/portal/static/sw-push.js", f"{REMOTE_PORTAL_DIR}/static/sw-push.js"),
    ("apps/portal/static/css/portal-offer.css", f"{REMOTE_PORTAL_DIR}/static/css/portal-offer.css"),
    ("apps/portal/services/certificate_service.py", f"{REMOTE_PORTAL_DIR}/services/certificate_service.py"),
    ("apps/website/src/data/certificates_registry.json", f"{REMOTE_WEBSITE_DIR}/src/data/certificates_registry.json"),
    ("scripts/seed_ec2_test_personas.py", "/var/www/dbert-website-lms/scripts/seed_ec2_test_personas.py"),
    ("deploy/dbert-unified-nginx.conf", "/tmp/dbert-unified-nginx.conf"),
]

def run_ssh(cmd):
    full_cmd = [
        "ssh", "-i", PEM_PATH,
        "-o", "StrictHostKeyChecking=no",
        REMOTE_HOST,
        cmd
    ]
    print(f"\n[SSH RUN] {cmd}")
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    if res.stdout:
        print(f"[STDOUT]\n{res.stdout.strip()}")
    if res.stderr:
        print(f"[STDERR]\n{res.stderr.strip()}")
    if res.returncode != 0:
        print(f"[FAIL] Command exited with code {res.returncode}")
        sys.exit(res.returncode)
    return res.stdout

def scp_file(local_path, remote_path):
    cmd = [
        "scp", "-i", PEM_PATH,
        "-o", "StrictHostKeyChecking=no",
        local_path,
        f"{REMOTE_HOST}:{remote_path}"
    ]
    print(f"[SCP] {local_path} -> {remote_path}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[SCP ERROR] {res.stderr}")
        sys.exit(res.returncode)

def main():
    print("=" * 70)
    print("DBERT Production Deployment: Web Push CSP, Offer Letters & Personas")
    print("=" * 70)

    # 1. Upload files
    print("\n--- 1. Uploading Files to EC2 ---")
    for local_f, remote_f in FILES_TO_UPLOAD:
        scp_file(local_f, remote_f)

    # 2. Update Nginx with /sw-push.js location block if not present
    print("\n--- 2. Checking & Updating Nginx Config ---")
    run_ssh("sudo cp /tmp/dbert-unified-nginx.conf /etc/nginx/sites-available/dbert-unified.conf")

    # 3. Test Nginx and reload
    print("\n--- 3. Testing & Reloading Nginx ---")
    run_ssh("sudo nginx -t")
    run_ssh("sudo systemctl reload nginx.service")

    # 4. Run test personas seeding script on EC2
    print("\n--- 4. Seeding EC2 Personas in PostgreSQL ---")
    run_ssh("cd /var/www/dbert-website-lms && /var/www/dbert-website-lms/apps/portal/.venv/bin/python scripts/seed_ec2_test_personas.py")

    # 5. Restart LMS portal service
    print("\n--- 5. Restarting dbert-portal.service ---")
    run_ssh("sudo systemctl restart dbert-portal.service && sleep 2 && sudo systemctl is-active dbert-portal.service")

    print("\n" + "=" * 70)
    print("Deployment to Production EC2 Completed Successfully!")
    print("=" * 70)

if __name__ == "__main__":
    main()
