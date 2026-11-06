import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"
REMOTE_WEB_DIR = "/var/www/dbert-website-lms/apps/website"
REMOTE_DATA_DIR = "/var/www/dbert-website-lms/data"

files_to_scp = [
    ("data/balance_enrollments_1500.json", f"{REMOTE_DATA_DIR}/balance_enrollments_1500.json"),
    ("apps/website/src/app/api/enroll/lookup/route.ts", f"{REMOTE_WEB_DIR}/src/app/api/enroll/lookup/route.ts"),
    ("apps/website/src/app/enroll/1999/EnrollmentClient.tsx", f"{REMOTE_WEB_DIR}/src/app/enroll/1999/EnrollmentClient.tsx"),
    ("apps/website/src/app/enroll/1999/enroll.module.css", f"{REMOTE_WEB_DIR}/src/app/enroll/1999/enroll.module.css"),
    ("apps/website/src/data/certificates_registry.json", f"{REMOTE_WEB_DIR}/src/data/certificates_registry.json"),
    ("apps/website/src/data/directory_candidates.json", f"{REMOTE_WEB_DIR}/src/data/directory_candidates.json"),
    ("GEMINI.md", "/var/www/dbert-website-lms/GEMINI.md"),
    ("AGENTS.md", "/var/www/dbert-website-lms/AGENTS.md"),
    ("DOMAIN_MIGRATION_AND_GA4_CHANGELOG.md", "/var/www/dbert-website-lms/DOMAIN_MIGRATION_AND_GA4_CHANGELOG.md"),
]

print(f"Uploading {len(files_to_scp)} files to EC2...")

for local, remote in files_to_scp:
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
        print(f"Failed to scp {local}: {res.stderr}")
    else:
        print(f"  ✓ {os.path.basename(local)}")

print("\nExecuting remote standalone build & systemd restart on EC2...")
remote_cmd = """
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

ssh_cmd = [
    "ssh",
    "-i", PEM_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "BatchMode=yes",
    REMOTE_HOST,
    remote_cmd
]

res = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=180)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
print(f"Deployment Exit Code: {res.returncode}")
