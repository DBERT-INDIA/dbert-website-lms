# -*- coding: utf-8 -*-
"""
Tar-based high-speed deployment script for Article Deduplication, Sitemaps,
and Trust Mesh updates to production EC2.
"""

import tarfile
import subprocess
import os
import sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

FILES_TO_PACK = [
    "apps/portal/app.py",
    "apps/portal/routes/stipend.py",
    "apps/portal/templates/admin_articles.html",
    "apps/portal/templates/intern_articles.html",
    "data/published_articles.json",
    "apps/website/src/data/published_articles.json",
    "apps/website/next.config.js",
    "apps/website/src/lib/blog.ts",
    "apps/website/src/app/sitemap.ts",
    "apps/website/src/components/seo/ArticleSchema.tsx",
    "apps/website/src/app/blog/[slug]/page.tsx",
    "apps/website/src/app/verify/[certId]/CandidateProfileClient.tsx",
    "apps/website/src/app/verify/directory/DirectoryClient.tsx",
]

def main():
    print("="*80)
    print("PACKING AND DEPLOYING ARTICLE & TRUST MESH UPDATES TO EC2")
    print("="*80)

    tar_path = os.path.abspath("article_updates.tar.gz")
    print(f"\n[1/5] Creating tarball {tar_path} with {len(FILES_TO_PACK)} files...")
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in FILES_TO_PACK:
            if os.path.exists(f):
                tar.add(f, arcname=f)
                print(f"  + Added {f}")
            else:
                print(f"  ! Missing {f}")
                sys.exit(1)

    print(f"\n[2/5] Uploading tarball to EC2 /tmp/article_updates.tar.gz...")
    scp_cmd = f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no "{tar_path}" "{HOST}:/tmp/article_updates.tar.gz"'
    res = subprocess.run(scp_cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[SCP ERROR] {res.stderr}")
        sys.exit(1)
    print("  ✓ Tarball uploaded successfully.")

    print("\n[3/5] Extracting tarball into /var/www/dbert-website-lms...")
    extract_cmd = f'tar -xzf /tmp/article_updates.tar.gz -C {REMOTE_BASE}'
    ssh_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no "{HOST}" "{extract_cmd}"'
    res = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[SSH EXTRACT ERROR] {res.stderr}")
        sys.exit(1)
    print("  ✓ Files extracted on EC2.")

    print("\n[4/5] Restarting dbert-portal.service on EC2...")
    portal_restart = 'sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service'
    ssh_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no "{HOST}" "{portal_restart}"'
    res = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
    print(res.stdout.strip())

    print("\n[5/5] Rebuilding Next.js Standalone on EC2 and restarting dbert-website.service...")
    remote_build_script = """
set -e
cd /var/www/dbert-website-lms/apps/website
export NODE_ENV=production
npm run build
cp -r public .next/standalone/ 2>/dev/null || true
cp -r public .next/standalone/apps/website/ 2>/dev/null || true
mkdir -p /var/www/dbert-website-lms/data
rm -rf /var/www/dbert-website-lms/apps/website/.next/standalone/data
ln -s /var/www/dbert-website-lms/data /var/www/dbert-website-lms/apps/website/.next/standalone/data
sudo systemctl restart dbert-website.service
sleep 2
systemctl is-active dbert-website.service
"""
    ssh_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no "{HOST}" "{remote_build_script}"'
    res = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[BUILD ERROR] {res.stderr}")
        sys.exit(1)
    print(res.stdout.strip())

    # Clean local tar
    if os.path.exists(tar_path):
        os.remove(tar_path)

    print("\n" + "="*80)
    print("[SUCCESS] Production EC2 Deployment Completed!")
    print("="*80)

if __name__ == "__main__":
    main()
