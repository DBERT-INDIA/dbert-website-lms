"""
scripts/deploy_stipend_system_to_ec2.py
Reliable automated deployment pipeline for Stipend Contribution & Verification Gating System.
Uses argument lists for subprocess to avoid Windows cmd quote escaping pitfalls.
"""
import os
import sys
import subprocess
import time

EC2_HOST = "ubuntu@3.26.237.171"
SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_BASE = "/var/www/dbert-website-lms"

SSH_BASE = [
    "ssh",
    "-i", SSH_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=15",
    "-o", "BatchMode=yes",
    EC2_HOST
]

SCP_BASE = [
    "scp",
    "-i", SSH_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "ConnectTimeout=15",
    "-o", "BatchMode=yes"
]

FILES_TO_UPLOAD = [
    # Services
    ("apps/portal/services/certificate_service.py", f"{REMOTE_BASE}/apps/portal/services/certificate_service.py"),
    ("apps/portal/services/ai/stipend_evaluator.py", f"{REMOTE_BASE}/apps/portal/services/ai/stipend_evaluator.py"),
    # Routes
    ("apps/portal/routes/stipend.py", f"{REMOTE_BASE}/apps/portal/routes/stipend.py"),
    ("apps/portal/routes/__init__.py", f"{REMOTE_BASE}/apps/portal/routes/__init__.py"),
    # Core app
    ("apps/portal/app.py", f"{REMOTE_BASE}/apps/portal/app.py"),
    # Templates
    ("apps/portal/templates/stipend_tasks.html", f"{REMOTE_BASE}/apps/portal/templates/stipend_tasks.html"),
    ("apps/portal/templates/_intern_sidebar.html", f"{REMOTE_BASE}/apps/portal/templates/_intern_sidebar.html"),
    ("apps/portal/templates/staff_task_queue.html", f"{REMOTE_BASE}/apps/portal/templates/staff_task_queue.html"),
    ("apps/portal/templates/admin_ambassador_payouts.html", f"{REMOTE_BASE}/apps/portal/templates/admin_ambassador_payouts.html"),
    # Migration & sync scripts
    ("scripts/migrate_stipend_schema_and_tasks.py", f"{REMOTE_BASE}/scripts/migrate_stipend_schema_and_tasks.py"),
    ("scripts/sync_verified_certificates_to_portal.py", f"{REMOTE_BASE}/scripts/sync_verified_certificates_to_portal.py"),
]


def run_ssh(remote_cmd, desc=""):
    print(f"\n[SSH EXEC] {desc or remote_cmd}")
    cmd = SSH_BASE + [remote_cmd]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.returncode != 0:
        print(f"[ERROR] Exit code {res.returncode}")
        if res.stderr:
            print(res.stderr.strip())
        return False
    return True


def run_scp(local_file, remote_file):
    print(f"[SCP] {local_file} -> {remote_file}")
    cmd = SCP_BASE + [local_file, f"{EC2_HOST}:{remote_file}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] SCP failed for {local_file}: {res.stderr.strip()}")
        return False
    return True


def deploy():
    print("=" * 70)
    print("DBERT LMS: Deploying Stipend System to Production EC2 (ubuntu@3.26.237.171)")
    print("=" * 70)

    # 1. Create remote dirs
    mkdir_cmd = f"mkdir -p {REMOTE_BASE}/apps/portal/services/ai {REMOTE_BASE}/apps/portal/routes {REMOTE_BASE}/apps/portal/uploads/stipend {REMOTE_BASE}/scripts"
    if not run_ssh(mkdir_cmd, "Creating remote directories on EC2"):
        return False

    # 2. Upload files
    print("\n[UPLOAD] Uploading portal files...")
    for local_path, remote_path in FILES_TO_UPLOAD:
        if not os.path.isfile(local_path):
            print(f"[WARN] Local file missing: {local_path}")
            continue
        if not run_scp(local_path, remote_path):
            return False
    print("[UPLOAD] All files uploaded successfully.")

    # 3. Run migration on EC2 using virtualenv python
    migrate_cmd = f"cd {REMOTE_BASE}/apps/portal && {REMOTE_BASE}/apps/portal/.venv/bin/python {REMOTE_BASE}/scripts/migrate_stipend_schema_and_tasks.py"
    if not run_ssh(migrate_cmd, "Running PostgreSQL schema migration & task seeding"):
        return False

    # 4. Run sync on EC2 using virtualenv python
    sync_cmd = f"cd {REMOTE_BASE}/apps/portal && {REMOTE_BASE}/apps/portal/.venv/bin/python {REMOTE_BASE}/scripts/sync_verified_certificates_to_portal.py"
    if not run_ssh(sync_cmd, "Syncing verified certificates to PostgreSQL"):
        return False

    # 5. Restart portal service
    restart_cmd = "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"
    if not run_ssh(restart_cmd, "Restarting dbert-portal.service on EC2"):
        return False

    # 6. Verify local service response on EC2
    probe_cmd = "curl -sI http://127.0.0.1:5001/stipend/tasks | head -n 5"
    if not run_ssh(probe_cmd, "Probing local port 5001 endpoint"):
        return False

    print("\n" + "=" * 70)
    print("SUCCESS: Stipend System successfully deployed and verified on EC2!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)
