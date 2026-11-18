#!/usr/bin/env python3
"""
scripts/deploy_web_push_to_ec2.py
Deploys real-time web push notification infrastructure, VAPID service, database schema,
routes, and templates to EC2 and restarts dbert-portal.service.
"""
import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"
REMOTE_PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"
REMOTE_WEB_DIR = "/var/www/dbert-website-lms/apps/website"

FILES_TO_SCP = [
    ("apps/portal/services/notifications/web_push_service.py", f"{REMOTE_PORTAL_DIR}/services/notifications/web_push_service.py"),
    ("apps/portal/scripts/phase16_web_push_schema.py", f"{REMOTE_PORTAL_DIR}/scripts/phase16_web_push_schema.py"),
    ("apps/portal/static/sw-push.js", f"{REMOTE_PORTAL_DIR}/static/sw-push.js"),
    ("apps/portal/static/js/dbert-push-client.js", f"{REMOTE_PORTAL_DIR}/static/js/dbert-push-client.js"),
    ("apps/portal/templates/account_notifications.html", f"{REMOTE_PORTAL_DIR}/templates/account_notifications.html"),
    ("apps/portal/templates/admin_push_broadcast.html", f"{REMOTE_PORTAL_DIR}/templates/admin_push_broadcast.html"),
    ("apps/portal/templates/_head.html", f"{REMOTE_PORTAL_DIR}/templates/_head.html"),
    ("apps/portal/templates/_intern_sidebar.html", f"{REMOTE_PORTAL_DIR}/templates/_intern_sidebar.html"),
    ("apps/portal/templates/_staff_sidebar.html", f"{REMOTE_PORTAL_DIR}/templates/_staff_sidebar.html"),
    ("apps/portal/routes/mentor.py", f"{REMOTE_PORTAL_DIR}/routes/mentor.py"),
    ("apps/portal/routes/ambassador.py", f"{REMOTE_PORTAL_DIR}/routes/ambassador.py"),
    ("apps/portal/routes/stipend.py", f"{REMOTE_PORTAL_DIR}/routes/stipend.py"),
    ("apps/portal/app.py", f"{REMOTE_PORTAL_DIR}/app.py"),
    ("apps/website/public/sw-push.js", f"{REMOTE_WEB_DIR}/public/sw-push.js"),
]

def run_ssh_command(cmd_str):
    ssh_cmd = [
        "ssh",
        "-i", PEM_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        REMOTE_HOST,
        cmd_str
    ]
    res = subprocess.run(ssh_cmd, capture_output=True, text=True)
    return res

def main():
    print("=" * 75)
    print("DBERT Production Deployment: Real-Time Omnichannel Web Push System")
    print("=" * 75)

    # 1. SCP Files
    print(f"\n[1/5] Uploading {len(FILES_TO_SCP)} files to EC2 ({REMOTE_HOST})...")
    for local, remote in FILES_TO_SCP:
        if not os.path.exists(local):
            print(f"  ❌ Missing local file: {local}")
            sys.exit(1)

        cmd = [
            "scp",
            "-i", PEM_KEY,
            "-o", "StrictHostKeyChecking=no",
            "-o", "BatchMode=yes",
            local,
            f"{REMOTE_HOST}:{remote}"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  ❌ Failed to scp {local}: {res.stderr}")
            sys.exit(1)
        else:
            print(f"  ✓ Uploaded: {local} -> {remote}")

    # 2. Sync sw-push.js into standalone Next.js directories
    print("\n[2/5] Syncing sw-push.js into Next.js standalone directories...")
    sync_cmd = (
        "cp /var/www/dbert-website-lms/apps/website/public/sw-push.js /var/www/dbert-website-lms/apps/website/.next/standalone/public/ 2>/dev/null || true; "
        "cp /var/www/dbert-website-lms/apps/website/public/sw-push.js /var/www/dbert-website-lms/apps/website/.next/standalone/apps/website/public/ 2>/dev/null || true"
    )
    res = run_ssh_command(sync_cmd)
    if res.returncode == 0:
        print("  ✓ Public assets synced.")
    else:
        print(f"  ⚠ Sync warning: {res.stderr}")

    # 3. Run Phase 16 Database Migration
    print("\n[3/5] Executing Phase 16 Web Push PostgreSQL schema migration...")
    mig_cmd = "cd /var/www/dbert-website-lms/apps/portal && .venv/bin/python scripts/phase16_web_push_schema.py"
    res = run_ssh_command(mig_cmd)
    print(res.stdout)
    if res.returncode != 0:
        print(f"  ❌ Migration error: {res.stderr}")
        sys.exit(1)

    # 4. Restart dbert-portal.service
    print("\n[4/5] Restarting dbert-portal.service...")
    restart_cmd = "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"
    res = run_ssh_command(restart_cmd)
    status = res.stdout.strip()
    if status == "active":
        print("  ✓ dbert-portal.service is active and healthy.")
    else:
        print(f"  ❌ dbert-portal.service status: {status}\n{res.stderr}")
        sys.exit(1)

    # 5. Live Endpoint Probes
    print("\n[5/5] Performing live endpoint health probes...")
    probe_cmd = (
        "curl -s http://127.0.0.1:5001/api/push/vapid-public-key && echo '' && "
        "curl -s -I http://127.0.0.1:5001/static/sw-push.js | head -n 3"
    )
    res = run_ssh_command(probe_cmd)
    print(res.stdout)

    print("\n" + "=" * 75)
    print("DEPLOYMENT COMPLETE: Real-Time Web Push Engine Live in Production")
    print("=" * 75)

if __name__ == "__main__":
    main()
