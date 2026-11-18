import subprocess
import os
import sys
import json
import time
import requests

sys.stdout.reconfigure(encoding='utf-8')

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"
REMOTE_WEB_DIR = "/var/www/dbert-website-lms/apps/website"
REMOTE_PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"

CERT_IDS = [
    "CERT-DBERT-2026-AIML-100",
    "CERT-DBERT-2026-DA-186",
    "CERT-DBERT-2026-DA-127",
    "CERT-DBERT-2026-DA-187",
    "CERT-DBERT-2026-AIML-064",
    "CERT-DBERT-2026-DA-086",
    "CERT-DBERT-2026-AIML-178"
]

files_to_scp = [
    ("apps/website/src/data/certificates_registry.json", f"{REMOTE_WEB_DIR}/src/data/certificates_registry.json"),
    ("apps/website/src/data/directory_candidates.json", f"{REMOTE_WEB_DIR}/src/data/directory_candidates.json"),
]

for cid in CERT_IDS:
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

print("\nExecuting remote build, DB sync & systemd restart on EC2...")
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

cd /var/www/dbert-website-lms
/var/www/dbert-website-lms/apps/portal/.venv/bin/python scripts/sync_verified_certificates_to_portal.py
sudo systemctl restart dbert-portal.service
sleep 2
systemctl is-active dbert-website.service
systemctl is-active dbert-portal.service
"""

ssh_cmd = [
    "ssh",
    "-i", PEM_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "BatchMode=yes",
    REMOTE_HOST,
    remote_cmd
]

res = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=300)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
print(f"Deployment Exit Code: {res.returncode}")

# Live HTTP verification for all 7 certificates
print("\n" + "="*80)
print("LIVE VERIFICATION: PROBING ALL 7 CERTIFICATES ON PRODUCTION EC2 (https://dbert.in)")
print("="*80)

with open("apps/website/src/data/certificates_registry.json", "r", encoding="utf-8") as f:
    reg = json.load(f)

all_ok = True
for cid in CERT_IDS:
    rec = reg.get(cid, {})
    name = rec.get("holderName", "Unknown")
    verify_url = f"https://dbert.in/verify/{cid}"
    api_url = f"https://dbert.in/api/verify?certid={cid}"
    
    try:
        r = requests.get(verify_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        has_name = name.lower() in r.text.lower()
        has_verified = "verified" in r.text.lower()
        status_ok = r.status_code == 200 and has_name
        print(f"[{cid}] {name}: HTTP {r.status_code} | Name matched: {has_name} | Verified badge: {has_verified}")
        if not status_ok:
            all_ok = False
    except Exception as e:
        print(f"[{cid}] ERROR probing {verify_url}: {e}")
        all_ok = False

print(f"\nAll 7 certificates live verified on https://dbert.in: {all_ok}")
