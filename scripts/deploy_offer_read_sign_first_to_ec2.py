import subprocess
import sys
import time

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_PORTAL_DIR = "/var/www/dbert-website-lms/apps/portal"

def run_ssh(cmd):
    full_cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        HOST,
        cmd
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr

def scp_file(local_path, remote_path):
    cmd = [
        "scp", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        local_path,
        f"{HOST}:{remote_path}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr

def main():
    print("--- 1. Uploading modified files to /tmp on EC2 ---")
    files_to_upload = [
        ("apps/portal/app.py", "/tmp/app.py"),
        ("apps/portal/templates/portal_offer_letter.html", "/tmp/portal_offer_letter.html"),
        ("apps/portal/static/css/portal-offer.css", "/tmp/portal-offer.css"),
    ]

    for local, remote in files_to_upload:
        code, out, err = scp_file(local, remote)
        if code != 0:
            print(f"FAILED uploading {local}: {err}")
            sys.exit(1)
        print(f"Uploaded {local} -> {remote}")

    print("\n--- 2. Moving files into production directory ---")
    remote_copy_cmd = (
        f"sudo cp /tmp/app.py {REMOTE_PORTAL_DIR}/app.py && "
        f"sudo cp /tmp/portal_offer_letter.html {REMOTE_PORTAL_DIR}/templates/portal_offer_letter.html && "
        f"sudo cp /tmp/portal-offer.css {REMOTE_PORTAL_DIR}/static/css/portal-offer.css && "
        "rm -f /tmp/app.py /tmp/portal_offer_letter.html /tmp/portal-offer.css"
    )
    code, out, err = run_ssh(remote_copy_cmd)
    if code != 0:
        print(f"FAILED copying files: {err}")
        sys.exit(1)
    print("Copied files to production portal directory.")

    print("\n--- 3. Restarting dbert-portal.service ---")
    restart_cmd = "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"
    code, out, err = run_ssh(restart_cmd)
    print(f"Service status: {out.strip()} {err.strip()}")
    if "active" not in out:
        print("ERROR: dbert-portal service is not active!")
        sys.exit(1)

    print("\n--- 4. Live Verification of /portal/offer endpoint on EC2 ---")
    verify_cmd = """python3 -c "
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://lms.dbert.in/portal/offer', headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, context=ctx)
    print('HTTP status:', resp.getcode())
except urllib.error.HTTPError as e:
    print('HTTP status:', e.code)
    # Expected redirect 302 to /#signin when unauthenticated
" """
    code, out, err = run_ssh(verify_cmd)
    print(f"Live verification output: {out.strip()} {err.strip()}")
    print("\nDeployment completed successfully!")

if __name__ == "__main__":
    main()
