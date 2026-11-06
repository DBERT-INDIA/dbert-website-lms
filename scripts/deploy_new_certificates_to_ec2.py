import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"
REMOTE_WEB_DIR = "/var/www/dbert-website-lms/apps/website"

files_to_scp = [
    ("apps/website/src/data/certificates_registry.json", f"{REMOTE_WEB_DIR}/src/data/certificates_registry.json"),
    ("apps/website/src/data/directory_candidates.json", f"{REMOTE_WEB_DIR}/src/data/directory_candidates.json"),
]

# Add the 9 PNG preview images
cert_ids = [
    "CERT-DBERT-2026-AIML-092",
    "CERT-DBERT-2026-DA-117",
    "CERT-DBERT-2026-FSD-070",
    "CERT-DBERT-2026-PA-023",
    "CERT-DBERT-2026-DA-124",
    "CERT-DBERT-2026-DA-077",
    "CERT-DBERT-2026-DA-183",
    "CERT-DBERT-2026-DA-109",
    "CERT-DBERT-2026-DA-184"
]

for cid in cert_ids:
    png_local = f"apps/website/public/certificates/previews/{cid}.png"
    if os.path.exists(png_local):
        files_to_scp.append((png_local, f"{REMOTE_WEB_DIR}/public/certificates/previews/{cid}.png"))

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

print("\nExecuting remote build & systemd restart on EC2...")
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
