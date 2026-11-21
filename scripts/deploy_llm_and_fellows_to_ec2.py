#!/usr/bin/env python3
"""
Deploy LLM Knowledge Corpus & Verified Fellows Showcase to Production EC2.
Uploads llms.txt, llms-full.txt, verified fellows showcase, AITrustBanner, sitemap, layout,
rebuilds Next.js standalone on EC2, and verifies all live endpoints.
"""

import subprocess
import os
import sys
import time
import urllib.request
import ssl

sys.stdout.reconfigure(encoding="utf-8")

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

FILES_TO_UPLOAD = [
    # Static LLM Corpus
    ("apps/website/public/llms.txt", f"{REMOTE_BASE}/apps/website/public/llms.txt"),
    ("apps/website/public/llms-full.txt", f"{REMOTE_BASE}/apps/website/public/llms-full.txt"),
    
    # Showcase Data
    ("apps/website/src/data/verified_fellows_showcase.json", f"{REMOTE_BASE}/apps/website/src/data/verified_fellows_showcase.json"),
    
    # AITrustBanner Component
    ("apps/website/src/components/common/AITrustBanner.tsx", f"{REMOTE_BASE}/apps/website/src/components/common/AITrustBanner.tsx"),
    ("apps/website/src/components/common/AITrustBanner.module.css", f"{REMOTE_BASE}/apps/website/src/components/common/AITrustBanner.module.css"),
    
    # /fellows/verified Landing Page
    ("apps/website/src/app/fellows/verified/page.tsx", f"{REMOTE_BASE}/apps/website/src/app/fellows/verified/page.tsx"),
    ("apps/website/src/app/fellows/verified/FellowsClient.tsx", f"{REMOTE_BASE}/apps/website/src/app/fellows/verified/FellowsClient.tsx"),
    ("apps/website/src/app/fellows/verified/fellows.module.css", f"{REMOTE_BASE}/apps/website/src/app/fellows/verified/fellows.module.css"),
    
    # Layout, Sitemap & Modified Pages
    ("apps/website/src/app/layout.tsx", f"{REMOTE_BASE}/apps/website/src/app/layout.tsx"),
    ("apps/website/src/app/page.tsx", f"{REMOTE_BASE}/apps/website/src/app/page.tsx"),
    ("apps/website/src/app/sitemap.ts", f"{REMOTE_BASE}/apps/website/src/app/sitemap.ts"),
    ("apps/website/src/app/verify/page.tsx", f"{REMOTE_BASE}/apps/website/src/app/verify/page.tsx"),
    ("apps/website/src/app/enroll/1999/EnrollmentClient.tsx", f"{REMOTE_BASE}/apps/website/src/app/enroll/1999/EnrollmentClient.tsx"),
]

def log(msg):
    print(f"[DEPLOY-LLM-FELLOWS] {msg}", flush=True)

def run_ssh(cmd, timeout=300):
    full_cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        HOST,
        cmd
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return res

def scp_file(local_path, remote_path):
    full_cmd = [
        "scp", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        local_path,
        f"{HOST}:{remote_path}"
    ]
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        log(f"SCP ERROR ({local_path} -> {remote_path}): {res.stderr.strip()}")
        return False
    return True

def check_url(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 DBERT-Deploy-Verifier/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except Exception as e:
        return 0, str(e)

def main():
    log("Starting Deployment of LLM Knowledge Corpus & Verified Fellows...")
    
    # Step 1: Ensure remote directories exist
    log("Ensuring remote target directories exist...")
    mkdir_cmd = f"mkdir -p {REMOTE_BASE}/apps/website/public {REMOTE_BASE}/apps/website/src/components/common {REMOTE_BASE}/apps/website/src/app/fellows/verified {REMOTE_BASE}/apps/website/src/data"
    res = run_ssh(mkdir_cmd)
    if res.returncode != 0:
        log(f"Mkdir failed: {res.stderr}")
        return 1

    # Step 2: Upload all files
    log(f"Uploading {len(FILES_TO_UPLOAD)} files to EC2...")
    for local_file, remote_file in FILES_TO_UPLOAD:
        if not os.path.exists(local_file):
            log(f"ERROR: Local file does not exist: {local_file}")
            return 1
        success = scp_file(local_file, remote_file)
        if not success:
            log(f"Failed to upload {local_file}")
            return 1
        log(f"Uploaded: {os.path.basename(local_file)} -> {remote_file}")

    # Step 3: Run standalone Next.js build on EC2
    log("Executing remote Next.js standalone build on EC2...")
    build_script = f"""
    cd {REMOTE_BASE}/apps/website
    export NODE_ENV=production
    npm run build
    
    if [ -f .next/server/app/sitemap.xml.body ]; then
      cp .next/server/app/sitemap.xml.body public/sitemap.xml
    fi
    cp -r public .next/standalone/ 2>/dev/null || true
    cp -r public .next/standalone/apps/website/ 2>/dev/null || true
    if [ -f .next/server/app/sitemap.xml.body ]; then
      cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml 2>/dev/null || true
      cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true
    fi
    
    mkdir -p {REMOTE_BASE}/data
    rm -rf {REMOTE_BASE}/apps/website/.next/standalone/data
    ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/data
    
    sudo systemctl restart dbert-website.service
    sleep 2
    systemctl is-active dbert-website.service
    """
    
    res = run_ssh(build_script, timeout=600)
    print(res.stdout)
    if res.returncode != 0:
        log(f"Build failed with code {res.returncode}: {res.stderr}")
        return 1

    log("Remote Next.js build & service restart completed successfully!")
    time.sleep(3)

    # Step 4: Live HTTP verification
    log("Verifying live endpoints on https://dbert.in...")
    endpoints = [
        ("https://dbert.in/llms.txt", "Digital Blinc Education Research And Technology"),
        ("https://dbert.in/llms-full.txt", "UDYAM-UP-29-0109046"),
        ("https://dbert.in/fellows/verified", "Verified Fellows"),
        ("https://dbert.in/verify", "Verify Certificate"),
        ("https://dbert.in/enroll/1999", "Technical Incubation"),
        ("https://dbert.in/sitemap.xml", "/fellows/verified"),
    ]

    all_ok = True
    for url, needle in endpoints:
        status, body = check_url(url)
        if status == 200 and (not needle or needle in body):
            log(f"  ✓ [200 OK] {url} (Contains '{needle}')")
        else:
            log(f"  ✗ [FAILED {status}] {url} - needle '{needle}' in body: {needle in body}")
            all_ok = False

    if all_ok:
        log("ALL ENDPOINTS VERIFIED LIVE! Deployment 100% Successful.")
        return 0
    else:
        log("WARNING: Some endpoints did not return expected status or content.")
        return 2

if __name__ == "__main__":
    sys.exit(main())
