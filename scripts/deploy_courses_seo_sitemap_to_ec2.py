import subprocess
import os
import sys
import tarfile
import tempfile
import ssl
import json
import urllib.request
import time

sys.stdout.reconfigure(encoding="utf-8")

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

def log(msg):
    print(f"[DEPLOY] {msg}", flush=True)

def run_ssh(cmd, timeout=360):
    full_cmd = [
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        HOST,
        cmd
    ]
    log(f"Running remote SSH command:\n{cmd.strip()}")
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    if res.returncode != 0:
        log(f"SSH ERROR (Exit {res.returncode}):\n{res.stderr.strip()}")
    else:
        log(f"SSH OK:\n{res.stdout.strip()}")
    return res

def scp_file(local_path, remote_path):
    full_cmd = [
        "scp", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        local_path,
        f"{HOST}:{remote_path}"
    ]
    log(f"SCP: {local_path} -> {remote_path}")
    res = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        log(f"SCP ERROR (Exit {res.returncode}):\n{res.stderr.strip()}")
        return False
    return True

def create_payload_tarball():
    tar_path = os.path.join(tempfile.gettempdir(), "dbert_courses_seo_payload.tar.gz")
    log(f"Packaging deployment tarball at {tar_path}...")
    
    with tarfile.open(tar_path, "w:gz") as tar:
        # 1. Add apps/website/src
        src_dir = os.path.join("apps", "website", "src")
        log(f"Adding {src_dir}...")
        tar.add(src_dir, arcname="src")

        # 2. Add public sitemap, reports, and static assets
        pub_sitemap = os.path.join("apps", "website", "public", "sitemap.xml")
        if os.path.exists(pub_sitemap):
            log(f"Adding {pub_sitemap}...")
            tar.add(pub_sitemap, arcname="public/sitemap.xml")

        pub_reports = os.path.join("apps", "website", "public", "reports")
        if os.path.exists(pub_reports):
            log(f"Adding {pub_reports}...")
            tar.add(pub_reports, arcname="public/reports")

        root_sitemap = os.path.join("apps", "website", "sitemap.xml")
        if os.path.exists(root_sitemap):
            log(f"Adding {root_sitemap}...")
            tar.add(root_sitemap, arcname="sitemap.xml")

        # 3. Add portal sitemap
        portal_sitemap = os.path.join("apps", "portal", "sitemap.xml")
        if os.path.exists(portal_sitemap):
            log(f"Adding {portal_sitemap}...")
            tar.add(portal_sitemap, arcname="portal_sitemap.xml")

    size_mb = os.path.getsize(tar_path) / (1024 * 1024)
    log(f"Tarball created successfully ({size_mb:.2f} MB)")
    return tar_path

def main():
    log("=" * 80)
    log("STARTING PRODUCTION EC2 DEPLOYMENT: SITEMAPS, 9-DOMAIN COURSES, SEO & LEAD CAPTURE")
    log("=" * 80)

    # Step 1: Package
    tar_path = create_payload_tarball()

    # Step 2: Upload tarball to EC2 /tmp
    remote_tar = "/tmp/dbert_courses_seo_payload.tar.gz"
    if not scp_file(tar_path, remote_tar):
        log("Failed to upload payload tarball to EC2!")
        sys.exit(1)

    # Step 3: Remote Extraction, Build, Standalone Sync & Service Restart
    remote_script = f"""
    set -e
    echo "[EC2] Extracting website payload..."
    cd {REMOTE_BASE}/apps/website
    tar -xzf {remote_tar}

    if [ -f {remote_tar} ]; then
        echo "[EC2] Syncing portal sitemap..."
        if [ -f portal_sitemap.xml ]; then
            cp portal_sitemap.xml {REMOTE_BASE}/apps/portal/sitemap.xml
            rm -f portal_sitemap.xml
        fi
        rm -f {remote_tar}
    fi

    echo "[EC2] Running production Next.js standalone build..."
    export NODE_ENV=production
    npm run build

    echo "[EC2] Syncing generated sitemap and static assets to standalone..."
    if [ -f .next/server/app/sitemap.xml.body ]; then
        cp .next/server/app/sitemap.xml.body public/sitemap.xml
        cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml 2>/dev/null || true
        cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true
    fi

    cp -r public .next/standalone/ 2>/dev/null || true
    cp -r public .next/standalone/apps/website/ 2>/dev/null || true

    echo "[EC2] Ensuring permanent data symlink persists..."
    mkdir -p {REMOTE_BASE}/data
    rm -rf {REMOTE_BASE}/apps/website/.next/standalone/data
    ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/data
    rm -rf {REMOTE_BASE}/apps/website/.next/standalone/apps/website/data 2>/dev/null || true
    ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/apps/website/data 2>/dev/null || true

    echo "[EC2] Restarting dbert-website.service and dbert-portal.service..."
    sudo systemctl restart dbert-website.service
    sudo systemctl restart dbert-portal.service
    sleep 3
    systemctl is-active dbert-website.service
    systemctl is-active dbert-portal.service
    """

    res = run_ssh(remote_script)
    if res.returncode != 0:
        log("Remote build or service restart failed!")
        sys.exit(res.returncode)

    # Clean up local tarball
    try:
        os.remove(tar_path)
    except Exception:
        pass

    log("=" * 80)
    log("STEP 4: LIVE PRODUCTION VERIFICATION (HTTPS)")
    log("=" * 80)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    def check_url(url, expected_snippets=None, min_status=200, max_status=200):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) DBERT-Verification/2.0'})
            with urllib.request.urlopen(req, timeout=20, context=ctx) as response:
                status = response.status
                body = response.read().decode('utf-8', errors='replace')
                if not (min_status <= status <= max_status):
                    log(f"FAIL: {url} returned status {status}")
                    return False
                if expected_snippets:
                    for snippet in expected_snippets:
                        if snippet not in body:
                            log(f"FAIL: {url} missing expected snippet '{snippet}'")
                            return False
                log(f"PASS [HTTP {status}]: {url}")
                return True
        except Exception as e:
            log(f"ERROR: {url} -> {e}")
            return False

    verifications = [
        # 1. Sitemaps
        ("https://dbert.in/sitemap.xml", ["<?xml", "https://dbert.in/courses/ai-agent-development", "https://dbert.in/verify/directory/cybersecurity", "https://dbert.in/internships/full-stack-development/bengaluru"]),
        ("https://lms.dbert.in/sitemap.xml", ["<?xml", "https://lms.dbert.in/"]),
        
        # 2. Dynamic Course Pages (All 9 Domains)
        ("https://dbert.in/courses/ai-agent-development", ["AI Agent & Multi-Agent Systems Engineering", "Structure 1: Fellowship", "Structure 2: Paid Course"]),
        ("https://dbert.in/courses/full-stack-development", ["Full Stack Web & AI Systems Engineering", "Next.js 16", "2-Month Fellowship"]),
        ("https://dbert.in/courses/data-analytics", ["Data Analytics & Automated Corporate BI", "Power BI", "SQL"]),
        ("https://dbert.in/courses/cybersecurity", ["Cybersecurity & Threat Defense Engineering", "OWASP Top 10", "Burp Suite"]),
        ("https://dbert.in/courses/devops-cloud", ["DevOps & Cloud Systems Engineering", "Docker", "Kubernetes", "AWS"]),
        ("https://dbert.in/courses/mobile-app-development", ["Mobile App Development (Flutter & React Native)", "Flutter", "SQLite"]),
        ("https://dbert.in/courses/python-automation", ["Python Automation & Web Extraction Engineering", "Playwright", "Celery"]),
        ("https://dbert.in/courses/ui-ux-design", ["UI/UX Design & Venture Product Prototyping", "Figma", "Auto-Layout"]),
        ("https://dbert.in/courses/generative-ai", ["Generative AI & LLM Systems Engineering", "LoRA / QLoRA", "PyTorch"]),

        # 3. Dynamic Single-Segment & Geo Internship Pages
        ("https://dbert.in/internships/bengaluru", ["Software & AI Internships in Bengaluru", "Manyata Tech Park"]),
        ("https://dbert.in/internships/ai-agent-development", ["AI Agent & LLM Systems Internships", "LangGraph"]),
        ("https://dbert.in/internships/full-stack-development/bengaluru", ["Full Stack Web Development Intern (Bengaluru)", "Outer Ring Road", "5000"]),
        ("https://dbert.in/internships/data-analytics/bengaluru", ["Data Analytics", "Bengaluru", "Register for Data Analytics"]),

        # 4. Canonical Domain Directories
        ("https://dbert.in/verify/directory/cybersecurity", ["Pre-Vetted Cybersecurity Engineers", "OWASP Top 10"]),
        ("https://dbert.in/verify/directory/ai-agent-development", ["Pre-Vetted AI Agent Developers", "LangGraph"]),

        # 5. Core Incubation, Verification Gates & Intelligence Report
        ("https://dbert.in/enroll/1999", ["1,999", "1,500"]),
        ("https://dbert.in/verify/directory", ["Pre-Vetted Software & AI Engineers"]),
        ("https://dbert.in/dbert-online", ["dbert.in"]),
        ("https://dbert.in/reports/growth-intelligence-2026.html", ["DBERT Growth & Marketing Intelligence Audit", "2,834", "10,759"])
    ]

    all_passed = True
    for url, snippets in verifications:
        if not check_url(url, snippets):
            all_passed = False

    # 6. Test Lead Ingestion API (POST /api/leads/capture)
    log("\n[TEST] Testing POST /api/leads/capture on live production...")
    try:
        lead_payload = {
            "name": "Production Verification Robot",
            "email": "telemetry-verify@dbert.in",
            "phone": "9999988888",
            "college": "IIT Delhi",
            "domain": "ai-agent-development",
            "programInterest": "fellowship",
            "city": "Bengaluru"
        }
        lead_req = urllib.request.Request(
            "https://dbert.in/api/leads/capture",
            data=json.dumps(lead_payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "DBERT-DeployTest/2.0"}
        )
        with urllib.request.urlopen(lead_req, timeout=15, context=ctx) as lead_res:
            res_body = json.loads(lead_res.read().decode("utf-8"))
            if lead_res.status == 201 and res_body.get("success") is True:
                log(f"PASS [HTTP 201]: Lead capture verified! Lead ID: {res_body.get('leadId')}")
            else:
                log(f"FAIL: Lead capture unexpected response: {res_body}")
                all_passed = False
    except Exception as e:
        log(f"ERROR testing lead capture API: {e}")
        all_passed = False

    log("=" * 80)
    if all_passed:
        log("🎉 PRODUCTION EC2 DEPLOYMENT 100% SUCCESSFUL & VERIFIED!")
    else:
        log("⚠️ DEPLOYMENT FINISHED WITH WARNINGS ON SOME ENDPOINTS.")
    log("=" * 80)

if __name__ == "__main__":
    main()
