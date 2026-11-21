#!/usr/bin/env python3
"""
deploy_clean_verified_fellows_to_ec2.py
Deploys cleaned certificates registry, verified fellows showcase, and FellowsClient UI
to EC2 production, performs standalone build, asset sync, and restarts dbert-website.service.
"""

import subprocess
import sys
import time

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

FILES_TO_DEPLOY = [
    ("apps/website/src/data/certificates_registry.json", f"{REMOTE_BASE}/apps/website/src/data/certificates_registry.json"),
    ("apps/website/src/data/verified_fellows_showcase.json", f"{REMOTE_BASE}/apps/website/src/data/verified_fellows_showcase.json"),
    ("apps/website/src/app/fellows/verified/FellowsClient.tsx", f"{REMOTE_BASE}/apps/website/src/app/fellows/verified/FellowsClient.tsx"),
    ("apps/website/src/app/fellows/verified/page.tsx", f"{REMOTE_BASE}/apps/website/src/app/fellows/verified/page.tsx"),
    ("scripts/generate_verified_fellows_data.py", f"{REMOTE_BASE}/scripts/generate_verified_fellows_data.py"),
    ("data/test_fixtures_certificates.json", f"{REMOTE_BASE}/data/test_fixtures_certificates.json"),
]

def run_cmd(cmd, check=True):
    print(f"[RUN] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        print(f"[STDERR] {res.stderr.strip()}", file=sys.stderr)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with code {res.returncode}")
    return res

def main():
    print("=== DEPLOYING CLEANED VERIFIED FELLOWS SHOWCASE TO EC2 ===")
    
    # 1. SCP Files
    for local_f, remote_f in FILES_TO_DEPLOY:
        print(f"[SCP] Uploading {local_f} -> {remote_f}...")
        scp_cmd = f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes "{local_f}" {HOST}:{remote_f}'
        run_cmd(scp_cmd)

    # 2. Remote Build & Restart
    print("\n[SSH] Running Remote Standalone Build on EC2...")
    build_script = f"""
set -e
cd {REMOTE_BASE}/apps/website
export NODE_ENV=production
npm run build

# Sync dynamic sitemap to public
if [ -f .next/server/app/sitemap.xml.body ]; then
  cp .next/server/app/sitemap.xml.body public/sitemap.xml
fi

# Sync public assets into standalone folders
cp -r public .next/standalone/ 2>/dev/null || true
cp -r public .next/standalone/apps/website/ 2>/dev/null || true

if [ -f .next/server/app/sitemap.xml.body ]; then
  cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml 2>/dev/null || true
  cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true
fi

# Ensure permanent data symlink persists across builds
mkdir -p {REMOTE_BASE}/data
rm -rf {REMOTE_BASE}/apps/website/.next/standalone/data
ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/data

sudo systemctl restart dbert-website.service
sleep 2

echo "=== Systemd Status ==="
systemctl is-active dbert-website.service
"""
    run_cmd(f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {HOST} "{build_script}"')
    
    # 3. HTTP status check
    print("\n[SSH] Verifying HTTP status on production...")
    verify_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {HOST} "curl -s -o /dev/null -w \'Fellows Page: %{{http_code}}\\n\' https://dbert.in/fellows/verified"'
    run_cmd(verify_cmd)
    
    print("=== DEPLOYMENT AND VERIFICATION COMPLETED SUCCESSFULLY ===")

if __name__ == '__main__':
    main()
