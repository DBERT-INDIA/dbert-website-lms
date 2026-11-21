#!/usr/bin/env python3
"""
Deploy GitHub Profile Enhancements & Interconnected Sitemaps / SEO to EC2.
Uploads modified website & portal files, rebuilds Next.js standalone, syncs sitemaps,
preserves data symlinks, and restarts systemd services.
"""

import subprocess
import sys
import time

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

FILES_TO_UPLOAD = [
    # Next.js Website files
    ("apps/website/src/app/sitemap.ts", f"{REMOTE_BASE}/apps/website/src/app/sitemap.ts"),
    ("apps/website/src/app/layout.tsx", f"{REMOTE_BASE}/apps/website/src/app/layout.tsx"),
    ("apps/website/src/app/about/team/page.tsx", f"{REMOTE_BASE}/apps/website/src/app/about/team/page.tsx"),
    ("apps/website/src/app/labs/opensource/page.tsx", f"{REMOTE_BASE}/apps/website/src/app/labs/opensource/page.tsx"),
    ("apps/website/src/components/layout/Footer.tsx", f"{REMOTE_BASE}/apps/website/src/components/layout/Footer.tsx"),
    ("apps/website/src/data/seo.config.ts", f"{REMOTE_BASE}/apps/website/src/data/seo.config.ts"),
    ("apps/website/src/data/directory_candidates.json", f"{REMOTE_BASE}/apps/website/src/data/directory_candidates.json"),
    # Flask LMS Portal files
    ("apps/portal/app.py", f"{REMOTE_BASE}/apps/portal/app.py"),
    ("apps/portal/templates/_footer_seo.html", f"{REMOTE_BASE}/apps/portal/templates/_footer_seo.html"),
]

def run_ssh(cmd, desc=""):
    print(f"\n[EXEC] {desc}...")
    full_cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        HOST, cmd
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FAIL] {desc} (code {res.returncode}):\n{res.stderr}")
        return False, res.stdout, res.stderr
    print(f"[OK] {desc}\n{res.stdout.strip()}")
    return True, res.stdout, res.stderr

def run_scp(local_path, remote_path):
    print(f"[SCP] {local_path} -> {remote_path}")
    full_cmd = [
        "scp", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        local_path, f"{HOST}:{remote_path}"
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FAIL] SCP for {local_path}:\n{res.stderr}")
        return False
    return True

def main():
    print("=================================================================")
    print("  DBERT: Deploying Interconnected Backlinks & Sitemaps to EC2    ")
    print("=================================================================")

    # Step 1: Upload all modified files
    print("\n--- Step 1: Uploading Modified Files ---")
    for local_f, remote_f in FILES_TO_UPLOAD:
        ok = run_scp(local_f, remote_f)
        if not ok:
            print(f"[ERROR] Failed uploading {local_f}. Aborting.")
            sys.exit(1)

    # Step 2: Build Next.js & Sync Sitemaps
    print("\n--- Step 2: Remote Standalone Build & Asset Sync ---")
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

# Restart Services
sudo systemctl restart dbert-website.service
sudo systemctl restart dbert-portal.service
sleep 2

echo "=== Systemd Status ==="
systemctl is-active dbert-website.service
systemctl is-active dbert-portal.service
"""

    ok, out, err = run_ssh(build_script, "Remote Build & Service Restart")
    if not ok:
        print(f"[ERROR] Build or restart failed: {err}")
        sys.exit(1)

    print("\n--- Step 3: Verifying Endpoints ---")
    verify_script = """
curl -s -o /dev/null -w "dbert.in Homepage: HTTP %{http_code}\\n" http://127.0.0.1:3000/
curl -s -o /dev/null -w "dbert.in Sitemap: HTTP %{http_code}\\n" http://127.0.0.1:3000/sitemap.xml
curl -s -o /dev/null -w "dbert.in Team: HTTP %{http_code}\\n" http://127.0.0.1:3000/about/team
curl -s -o /dev/null -w "dbert.in OpenSource: HTTP %{http_code}\\n" http://127.0.0.1:3000/labs/opensource
curl -s -o /dev/null -w "lms.dbert.in Sitemap: HTTP %{http_code}\\n" http://127.0.0.1:5001/sitemap.xml
curl -s -o /dev/null -w "lms.dbert.in Robots: HTTP %{http_code}\\n" http://127.0.0.1:5001/robots.txt
"""
    ok, out, err = run_ssh(verify_script, "Local Port HTTP Code Check")
    print(out)

    print("\n[SUCCESS] Deployment complete and verified!")

if __name__ == '__main__':
    main()
