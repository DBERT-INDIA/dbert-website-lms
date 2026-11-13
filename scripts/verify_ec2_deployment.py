import urllib.request
import json
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

def check_remote_dir_count():
    cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        REMOTE_HOST,
        "grep -c '\"certId\"' /var/www/dbert-website-lms/apps/website/src/data/directory_candidates.json"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("EC2 directory_candidates.json cert count:", res.stdout.strip())

def check_remote_1593_count():
    cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        REMOTE_HOST,
        "grep -c '\"certId\"' /var/www/dbert-website-lms/data/sheet_1593_provisional_registry.json"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("EC2 sheet_1593_provisional_registry.json cert count:", res.stdout.strip())

def check_web_endpoints():
    endpoints = [
        ("API Lookup (Sheet Candidate)", "https://dbert.in/api/enroll/lookup?q=renukanalawade3099@gmail.com"),
        ("Public Verify Route", "https://dbert.in/verify/CERT-DBERT-2026-DA-186"),
        ("Unlock Landing Page", "https://dbert.in/verify/unlock?certid=CERT-DBERT-2026-DA-186"),
    ]
    for name, url in endpoints:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
                body = resp.read().decode('utf-8')
                print(f"[OK {status}] {name}: {url} (Length: {len(body)} chars)")
        except Exception as e:
            print(f"[FAIL] {name}: {url} -> {e}")

if __name__ == "__main__":
    print("--- Checking EC2 State ---")
    check_remote_dir_count()
    check_remote_1593_count()
    print("\n--- Checking Live Web Endpoints ---")
    check_web_endpoints()
