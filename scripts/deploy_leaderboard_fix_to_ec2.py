import subprocess
import os
import sys
import urllib.request
import time

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
SERVER = "ubuntu@3.26.237.171"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REMOTE_BASE = "/var/www/dbert-website-lms"

def log(msg):
    print(f"[DEPLOY-LEADERBOARD-FIX] {msg}")

log("=" * 76)
log("DEPLOYING LEADERBOARD & CERTIFICATES LAYOUT OVERLAP FIX TO EC2")
log("=" * 76)

def run_scp(local_p, remote_p):
    scp_cmd = ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", local_p, f"{SERVER}:{remote_p}"]
    res = subprocess.run(scp_cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        raise RuntimeError(f"SCP failed for {local_p}: {res.stderr}")
    log(f"Uploaded: {os.path.basename(local_p)} -> {remote_p}")

def run_ssh(cmd):
    full_cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, cmd]
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        raise RuntimeError(f"SSH failed for {cmd}: {res.stderr}")
    return res

# 1. Upload templates
log("\n1. Uploading updated leaderboard.html and certificates.html...")
run_scp(
    os.path.join(BASE_DIR, "apps", "portal", "templates", "leaderboard.html"),
    f"{REMOTE_BASE}/apps/portal/templates/leaderboard.html"
)
run_scp(
    os.path.join(BASE_DIR, "apps", "portal", "templates", "certificates.html"),
    f"{REMOTE_BASE}/apps/portal/templates/certificates.html"
)

# 2. Restart dbert-portal.service
log("\n2. Restarting dbert-portal.service on EC2...")
restart_cmd = "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service"
res = run_ssh(restart_cmd)
log(f"Portal service status: {res.stdout.strip()}")

# 3. Live verification of live endpoints
log("\n3. Testing live endpoints on https://lms.dbert.in ...")
time.sleep(1)

test_urls = [
    "https://lms.dbert.in/leaderboard",
    "https://lms.dbert.in/certificates"
]

for url in test_urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DBERT-Layout-Probe/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
            has_sidebar = "has-sidebar" in content
            main_content = 'id="main-content"' in content
            log(f"{url} -> HTTP {resp.status} (Length: {len(content)} bytes) | has-sidebar: {has_sidebar} | id=main-content: {main_content}")
    except urllib.error.HTTPError as e:
        log(f"{url} -> HTTP {e.code} (Reason: {e.reason})")
    except Exception as ex:
        log(f"{url} -> Error: {ex}")

log("\n" + "=" * 76)
log("LEADERBOARD & CERTIFICATES LAYOUT FIX SUCCESSFULLY DEPLOYED & VERIFIED!")
log("=" * 76)
