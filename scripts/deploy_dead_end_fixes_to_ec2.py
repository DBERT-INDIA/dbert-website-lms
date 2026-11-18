import subprocess
import sys
import os

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

def run_cmd(cmd, check=True):
    print(f"\n[RUNNING] {cmd}")
    res = subprocess.run(cmd, shell=True)
    if check and res.returncode != 0:
        print(f"[ERROR] Command failed with code {res.returncode}")
        sys.exit(res.returncode)
    return res.returncode

def main():
    print("==================================================")
    print("DEPLOYING DEAD-END FIXES & ₹1,999 FUNNEL TO EC2")
    print("==================================================")

    # 1. Upload Portal files
    portal_files = [
        ("apps/portal/app.py", f"{REMOTE_BASE}/apps/portal/app.py"),
        ("apps/portal/templates/portal.html", f"{REMOTE_BASE}/apps/portal/templates/portal.html"),
        ("apps/portal/templates/stipend_tasks.html", f"{REMOTE_BASE}/apps/portal/templates/stipend_tasks.html"),
        ("apps/portal/templates/post_detail.html", f"{REMOTE_BASE}/apps/portal/templates/post_detail.html"),
    ]

    for local_f, remote_f in portal_files:
        print(f"Uploading {local_f} -> {remote_f}")
        run_cmd(f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes "{local_f}" {HOST}:{remote_f}')

    # 2. Upload Website files
    website_files = [
        ("apps/website/src/components/layout/ProgramDetailTemplate.tsx", f"{REMOTE_BASE}/apps/website/src/components/layout/ProgramDetailTemplate.tsx"),
        ("apps/website/src/app/api/enroll/balance/route.ts", f"{REMOTE_BASE}/apps/website/src/app/api/enroll/balance/route.ts"),
    ]

    for local_f, remote_f in website_files:
        print(f"Uploading {local_f} -> {remote_f}")
        run_cmd(f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes "{local_f}" {HOST}:{remote_f}')

    # Upload new course enroll route directory
    run_cmd(f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no {HOST} "mkdir -p {REMOTE_BASE}/apps/website/src/app/api/courses/enroll"')
    run_cmd(f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes "apps/website/src/app/api/courses/enroll/route.ts" {HOST}:{REMOTE_BASE}/apps/website/src/app/api/courses/enroll/route.ts')

    # 3. Upload test script
    run_cmd(f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes "scripts/test_dead_ends_and_sync.py" {HOST}:{REMOTE_BASE}/scripts/test_dead_ends_and_sync.py')

    # 4. Remote build & restart
    remote_script = f"""
    set -e
    echo '=== RESTARTING PORTAL GUNICORN SERVICE ==='
    sudo systemctl restart dbert-portal.service
    sleep 2
    systemctl is-active dbert-portal.service

    echo '=== RUNNING POSTGRESQL TEST SUITE ==='
    cd {REMOTE_BASE}
    python3 scripts/test_dead_ends_and_sync.py

    echo '=== BUILDING WEBSITE STANDALONE NEXT.JS ==='
    cd {REMOTE_BASE}/apps/website
    export NODE_ENV=production
    npm run build
    cp -r public .next/standalone/ 2>/dev/null || true
    cp -r public .next/standalone/apps/website/ 2>/dev/null || true

    mkdir -p {REMOTE_BASE}/data
    rm -rf {REMOTE_BASE}/apps/website/.next/standalone/data
    ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/data

    echo '=== RESTARTING WEBSITE NODE SERVICE ==='
    sudo systemctl restart dbert-website.service
    sleep 2
    systemctl is-active dbert-website.service

    echo '=== DEPLOYMENT AND VERIFICATION COMPLETE ==='
    """

    run_cmd(f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no {HOST} "{remote_script}"')

if __name__ == "__main__":
    main()
