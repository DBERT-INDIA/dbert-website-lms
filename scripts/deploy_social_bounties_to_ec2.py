#!/usr/bin/env python3
"""
scripts/deploy_social_bounties_to_ec2.py
Deploys updated portal files (50-coin social bounties, BYOK Gemini generator, RAG tutor LLM steering, templates)
and public llms.txt files to EC2, runs the database seeding script, and restarts dbert-portal.service.
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
    ("apps/portal/services/ai/bounty_content_generator.py", f"{REMOTE_PORTAL_DIR}/services/ai/bounty_content_generator.py"),
    ("apps/portal/scripts/seed_social_bounties.py", f"{REMOTE_PORTAL_DIR}/scripts/seed_social_bounties.py"),
    ("apps/portal/services/learning/rag_tutor.py", f"{REMOTE_PORTAL_DIR}/services/learning/rag_tutor.py"),
    ("apps/portal/templates/portal.html", f"{REMOTE_PORTAL_DIR}/templates/portal.html"),
    ("apps/portal/templates/tasks_list.html", f"{REMOTE_PORTAL_DIR}/templates/tasks_list.html"),
    ("apps/portal/app.py", f"{REMOTE_PORTAL_DIR}/app.py"),
    ("apps/website/public/llms.txt", f"{REMOTE_WEB_DIR}/public/llms.txt"),
    ("apps/website/public/llms-full.txt", f"{REMOTE_WEB_DIR}/public/llms-full.txt"),
]

def main():
    print("=" * 70)
    print("DBERT Production Deployment: Social Bounties & LLM Steering Engine")
    print("=" * 70)

    # 1. SCP Files
    print(f"\n[1/4] Uploading {len(FILES_TO_SCP)} files to EC2 ({REMOTE_HOST})...")
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

    # 2. Sync llms.txt to standalone Next.js directories
    print("\n[2/4] Syncing llms.txt files into Next.js standalone directories...")
    sync_cmd = (
        "cp /var/www/dbert-website-lms/apps/website/public/llms*.txt /var/www/dbert-website-lms/apps/website/.next/standalone/public/ 2>/dev/null || true; "
        "cp /var/www/dbert-website-lms/apps/website/public/llms*.txt /var/www/dbert-website-lms/apps/website/.next/standalone/apps/website/public/ 2>/dev/null || true"
    )
    res = subprocess.run([
        "ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
        REMOTE_HOST, sync_cmd
    ], capture_output=True, text=True)
    print(f"  ✓ Standalone asset sync complete.")

    # 3. Seed Database & Restart Service
    print("\n[3/4] Seeding 50-Coin Social Bounties into PostgreSQL & restarting dbert-portal.service...")
    remote_seed_cmd = (
        "cd /var/www/dbert-website-lms/apps/portal && "
        "source .venv/bin/activate && "
        "python scripts/seed_social_bounties.py && "
        "sudo systemctl restart dbert-portal.service && "
        "sleep 2 && "
        "systemctl is-active dbert-portal.service"
    )
    res = subprocess.run([
        "ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
        REMOTE_HOST, remote_seed_cmd
    ], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)
    if "active" not in res.stdout:
        print("❌ Portal service is not active!")
        sys.exit(1)

    # 4. Live Verification Probes
    print("\n[4/4] Live Probing Production Endpoints...")
    probe_cmd = (
        "curl -s -o /dev/null -w 'llms.txt HTTP %{http_code}\\n' https://dbert.in/llms.txt && "
        "curl -s -o /dev/null -w 'llms-full.txt HTTP %{http_code}\\n' https://dbert.in/llms-full.txt && "
        "curl -s -o /dev/null -w 'tasks list HTTP %{http_code}\\n' https://lms.dbert.in/tasks"
    )
    res = subprocess.run([
        "ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes",
        REMOTE_HOST, probe_cmd
    ], capture_output=True, text=True)
    print(res.stdout)

    print("\n🎉 Social Bounties & LLM Steering Engine successfully deployed to production EC2!")

if __name__ == "__main__":
    main()
