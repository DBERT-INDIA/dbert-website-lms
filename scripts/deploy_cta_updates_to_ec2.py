import subprocess
import sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_PORTAL = "/var/www/dbert-website-lms/apps/portal"

files_to_sync = [
    ("apps/portal/templates/portal_offer_letter.html", f"{REMOTE_PORTAL}/templates/portal_offer_letter.html"),
    ("apps/portal/templates/portal_offer_print.html", f"{REMOTE_PORTAL}/templates/portal_offer_print.html"),
    ("apps/portal/templates/stipend_tasks.html", f"{REMOTE_PORTAL}/templates/stipend_tasks.html"),
    ("apps/portal/templates/portal.html", f"{REMOTE_PORTAL}/templates/portal.html"),
    ("apps/portal/static/css/portal-offer.css", f"{REMOTE_PORTAL}/static/css/portal-offer.css"),
    ("apps/portal/app.py", f"{REMOTE_PORTAL}/app.py"),
]

print("=== DEPLOYING ENHANCED HIGH-VISIBILITY CTAs TO EC2 ===")
for local_f, remote_f in files_to_sync:
    print(f"Uploading {local_f} -> {remote_f}...")
    cmd = [
        "scp", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        local_f, f"{HOST}:{remote_f}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED to upload {local_f}: {res.stderr}")
        sys.exit(1)
    print("  ✓ Uploaded")

print("\nRestarting dbert-portal.service on EC2...")
restart_cmd = [
    "ssh", "-i", SSH_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "BatchMode=yes",
    HOST,
    "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"
]
res = subprocess.run(restart_cmd, capture_output=True, text=True)
print("Output:", res.stdout.strip())
if res.returncode != 0:
    print("Restart FAILED:", res.stderr)
    sys.exit(1)

print("\n[SUCCESS] EC2 dbert-portal.service restarted and active!")
