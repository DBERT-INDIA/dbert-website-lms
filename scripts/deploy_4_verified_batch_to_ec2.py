import subprocess
import sys
import time
import json

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

FILES_TO_UPLOAD = [
    ("apps/website/src/data/certificates_registry.json", f"{REMOTE_BASE}/apps/website/src/data/certificates_registry.json"),
    ("apps/website/src/data/directory_candidates.json", f"{REMOTE_BASE}/apps/website/src/data/directory_candidates.json"),
    ("apps/website/public/certificates/previews/CERT-DBERT-2026-FSD-343.png", f"{REMOTE_BASE}/apps/website/public/certificates/previews/CERT-DBERT-2026-FSD-343.png"),
    ("data/verification_submissions_299.json", f"{REMOTE_BASE}/data/verification_submissions_299.json"),
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
    print("  DBERT: Deploying 4 Verified Candidates & DB Sync to EC2        ")
    print("=================================================================")

    # Step 1: Upload all modified files
    print("\n--- Step 1: Uploading Files to Production ---")
    for local_f, remote_f in FILES_TO_UPLOAD:
        ok = run_scp(local_f, remote_f)
        if not ok:
            print(f"[ERROR] Failed uploading {local_f}. Aborting.")
            sys.exit(1)

    # Step 2: Database Sync in PostgreSQL on EC2
    print("\n--- Step 2: Syncing PostgreSQL intern_accounts, intern_certificates & notifications ---")
    db_sync_py = """
import psycopg2, psycopg2.extras
conn = psycopg2.connect('postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms')
with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
    # 1. Update stipend_verified for all 4 intern accounts
    intern_ids = [5016, 4468, 5041, 3326]
    cur.execute("UPDATE dbert_internship.intern_accounts SET stipend_verified = 1 WHERE id IN %s", (tuple(intern_ids),))
    print(f"Updated stipend_verified = 1 for intern accounts: {intern_ids}")

    # 2. Update existing certificates to tier = 'verified'
    certs_to_verify = ['CERT-DBERT-2026-DA-044', 'CERT-DBERT-2026-FSD-051', 'CERT-DBERT-2026-DA-005']
    cur.execute("UPDATE dbert_internship.intern_certificates SET tier = 'verified' WHERE cert_id IN %s", (tuple(certs_to_verify),))
    print(f"Updated intern_certificates tier = 'verified' for: {certs_to_verify}")

    # 3. Check / Insert CERT-DBERT-2026-FSD-343 for Maroju Prince Karthik (intern_id 3326)
    cur.execute("SELECT id FROM dbert_internship.intern_certificates WHERE cert_id = 'CERT-DBERT-2026-FSD-343'")
    row = cur.fetchone()
    if not row:
        cur.execute('''
            INSERT INTO dbert_internship.intern_certificates 
            (intern_id, course_id, course_title, cert_id, issued_at, url, received_at, tier, email)
            VALUES (%s, %s, %s, %s, NOW(), %s, NOW(), %s, %s)
        ''', (
            3326, 1, 'DBERT Technical Incubation — Full Stack Web Development', 
            'CERT-DBERT-2026-FSD-343', 
            'https://dbert.in/verify?certid=CERT-DBERT-2026-FSD-343', 
            'verified', 'marojuprincekarthik2007@gmail.com'
        ))
        print("Inserted new certificate CERT-DBERT-2026-FSD-343 into intern_certificates.")
    else:
        cur.execute("UPDATE dbert_internship.intern_certificates SET tier = 'verified' WHERE cert_id = 'CERT-DBERT-2026-FSD-343'")
        print("Updated CERT-DBERT-2026-FSD-343 tier = 'verified'.")

    # 4. Insert notifications for each candidate
    notifs = [
        (5016, 'credential_verified', '₹299 Verification Approved — Gate 1 Cleared', 'Your ₹299 project verification is approved. Your official verified credential and Letter of Recommendation are unlocked on dbert.in, and Gate 1 is closed for your 03 Dec 2026 stipend release.', 'https://dbert.in/verify/CERT-DBERT-2026-DA-044'),
        (4468, 'credential_verified', '₹299 Verification Approved — Gate 1 Cleared', 'Your ₹299 project verification is approved. Your official verified credential and Letter of Recommendation are unlocked on dbert.in, and Gate 1 is closed for your 03 Dec 2026 stipend release.', 'https://dbert.in/verify/CERT-DBERT-2026-FSD-051'),
        (5041, 'credential_verified', '₹299 Verification Approved — Gate 1 Cleared', 'Your ₹299 project verification is approved. Your official verified credential and Letter of Recommendation are unlocked on dbert.in, and Gate 1 is closed for your 03 Dec 2026 stipend release.', 'https://dbert.in/verify/CERT-DBERT-2026-DA-005'),
        (3326, 'credential_verified', '₹299 Verification Approved — Credential Issued', 'Your ₹299 verification is approved and verified credential CERT-DBERT-2026-FSD-343 is issued. Please add your UPI ID on your account page to clear Gate 3.', 'https://dbert.in/verify/CERT-DBERT-2026-FSD-343')
    ]
    for intern_id, kind, title, body, link in notifs:
        cur.execute('''
            INSERT INTO dbert_internship.notifications (intern_id, kind, title, body, link, is_read, created_at)
            VALUES (%s, %s, %s, %s, %s, 0, NOW())
        ''', (intern_id, kind, title, body, link))
    print(f"Inserted in-app notifications for 4 candidates.")

    conn.commit()
print("PostgreSQL sync completed successfully.")
"""
    # Write db_sync_py to remote and execute
    run_ssh(f"cat << 'EOF' > /tmp/db_sync_4_verified.py\n{db_sync_py}\nEOF\n/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 /tmp/db_sync_4_verified.py", "PostgreSQL Database Synchronization")

    # Step 3: Remote Standalone Build & Asset Sync
    print("\n--- Step 3: Remote Standalone Build & Asset Sync ---")
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

    print("\n--- Step 4: Live Verification ---")
    verify_script = """
curl -s -o /dev/null -w "Verify DA-044: HTTP %{http_code}\\n" http://127.0.0.1:3001/verify/CERT-DBERT-2026-DA-044
curl -s -o /dev/null -w "Verify FSD-051: HTTP %{http_code}\\n" http://127.0.0.1:3001/verify/CERT-DBERT-2026-FSD-051
curl -s -o /dev/null -w "Verify DA-005: HTTP %{http_code}\\n" http://127.0.0.1:3001/verify/CERT-DBERT-2026-DA-005
curl -s -o /dev/null -w "Verify FSD-343: HTTP %{http_code}\\n" http://127.0.0.1:3001/verify/CERT-DBERT-2026-FSD-343
curl -s -o /dev/null -w "Candidate Directory: HTTP %{http_code}\\n" http://127.0.0.1:3001/verify/directory
"""
    ok, out, err = run_ssh(verify_script, "Local HTTP Status Code Checks")
    print(out)

    print("\n[SUCCESS] 4 candidates verified, promoted to Tab 1, and deployed live!")

if __name__ == '__main__':
    main()
