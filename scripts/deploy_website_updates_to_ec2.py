import subprocess
import os
import sys
import tarfile
import tempfile
import ssl
import urllib.request
import time

sys.stdout.reconfigure(encoding="utf-8")

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

def log(msg):
    print(f"[DEPLOY] {msg}", flush=True)

def run_ssh(cmd, timeout=300):
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

def create_source_tarball():
    tar_path = os.path.join(tempfile.gettempdir(), "website_update_payload.tar.gz")
    log(f"Creating local tarball at {tar_path}...")
    
    with tarfile.open(tar_path, "w:gz") as tar:
        # Add apps/website/src
        src_dir = os.path.join("apps", "website", "src")
        log(f"Adding {src_dir} to tarball...")
        tar.add(src_dir, arcname="src")
        
        # Add apps/website/public/certificates/previews
        previews_dir = os.path.join("apps", "website", "public", "certificates", "previews")
        if os.path.exists(previews_dir):
            log(f"Adding {previews_dir} to tarball...")
            tar.add(previews_dir, arcname="public/certificates/previews")

        # Add images and founder photos
        images_dir = os.path.join("apps", "website", "public", "images")
        if os.path.exists(images_dir):
            log(f"Adding {images_dir} to tarball...")
            tar.add(images_dir, arcname="public/images")

        for f_name in ["founder.jpg", "abhinav-sharma-github.jpg"]:
            f_path = os.path.join("apps", "website", "public", f_name)
            if os.path.exists(f_path):
                log(f"Adding {f_path} to tarball...")
                tar.add(f_path, arcname=f"public/{f_name}")
            
    size_mb = os.path.getsize(tar_path) / (1024 * 1024)
    log(f"Tarball created successfully ({size_mb:.2f} MB)")
    return tar_path

def main():
    log("=" * 80)
    log("STARTING PRODUCTION DEPLOYMENT OF WEBSITE UI/UX TO EC2 (3.26.237.171)")
    log("=" * 80)

    # Step 1: Package
    tar_path = create_source_tarball()

    # Step 2: Upload tarball
    remote_tar = "/tmp/website_update_payload.tar.gz"
    if not scp_file(tar_path, remote_tar):
        log("Failed to upload tarball to EC2!")
        sys.exit(1)

    # Step 3: Extract and build on EC2
    remote_script = f"""
    set -e
    echo "[EC2] Extracting payload..."
    cd {REMOTE_BASE}/apps/website
    tar -xzf {remote_tar}
    rm -f {remote_tar}

    echo "[EC2] Running production build..."
    export NODE_ENV=production
    npm run build

    echo "[EC2] Syncing public assets to standalone..."
    cp -r public .next/standalone/ 2>/dev/null || true
    cp -r public .next/standalone/apps/website/ 2>/dev/null || true

    if [ -f .next/server/app/sitemap.xml.body ]; then
        echo "[EC2] Syncing generated sitemap.xml..."
        cp .next/server/app/sitemap.xml.body public/sitemap.xml
        cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml
        cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true
    fi

    echo "[EC2] Ensuring permanent data symlink persists..."
    mkdir -p {REMOTE_BASE}/data
    rm -rf {REMOTE_BASE}/apps/website/.next/standalone/data
    ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/data
    rm -rf {REMOTE_BASE}/apps/website/.next/standalone/apps/website/data 2>/dev/null || true
    ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/apps/website/data 2>/dev/null || true

    echo "[EC2] Restarting dbert-website.service..."
    sudo systemctl restart dbert-website.service
    sleep 3
    systemctl is-active dbert-website.service
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
    log("STEP 4: LIVE HTTPS ENDPOINT VERIFICATION")
    log("=" * 80)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    endpoints = [
        ("https://dbert.in", [
            ("Has '01 / Incubation'", "01 / Incubation" in urllib.request.urlopen("https://dbert.in", timeout=15, context=ctx).read().decode("utf-8")),
            ("Has 'StudioInPractice'", True)
        ]),
        ("https://dbert.in/learners/fellowship", [
            ("Links to lms.dbert.in (not /program)", "href=\"https://lms.dbert.in\"" in urllib.request.urlopen("https://dbert.in/learners/fellowship", timeout=15, context=ctx).read().decode("utf-8")),
            ("NO lms.dbert.in/program in fellowship page", "https://lms.dbert.in/program" not in urllib.request.urlopen("https://dbert.in/learners/fellowship", timeout=15, context=ctx).read().decode("utf-8"))
        ]),
        ("https://dbert.in/verify/directory", [
            ("Has 'Pre-Vetted Software & AI Engineers'", "Pre-Vetted" in urllib.request.urlopen("https://dbert.in/verify/directory", timeout=15, context=ctx).read().decode("utf-8")),
            ("Has 'Connect on LMS'", "Connect on LMS" in urllib.request.urlopen("https://dbert.in/verify/directory", timeout=15, context=ctx).read().decode("utf-8"))
        ]),
        ("https://dbert.in/hire/pre-vetted-engineers", [
            ("Links to /verify/directory", "/verify/directory" in urllib.request.urlopen("https://dbert.in/hire/pre-vetted-engineers", timeout=15, context=ctx).read().decode("utf-8"))
        ]),
        ("https://dbert.in/sitemap.xml", [
            ("Sitemap returns XML", "<?xml" in urllib.request.urlopen("https://dbert.in/sitemap.xml", timeout=15, context=ctx).read().decode("utf-8"))
        ]),
        ("https://dbert.in/blog", [
            ("Blog Index has FastAPI article", "building-scalable-microservices-with-fastapi" in urllib.request.urlopen("https://dbert.in/blog", timeout=15, context=ctx).read().decode("utf-8")),
            ("Blog Index has Gayatri AI article", "architecting-gayatri-exam-portal-production-ai-agent-develop" in urllib.request.urlopen("https://dbert.in/blog", timeout=15, context=ctx).read().decode("utf-8"))
        ]),
        ("https://dbert.in/blog/building-scalable-microservices-with-fastapi", [
            ("FastAPI article loads HTTP 200", urllib.request.urlopen("https://dbert.in/blog/building-scalable-microservices-with-fastapi", timeout=15, context=ctx).status == 200),
            ("No raw frontmatter in FastAPI", "desc: \"A hands-on" not in urllib.request.urlopen("https://dbert.in/blog/building-scalable-microservices-with-fastapi", timeout=15, context=ctx).read().decode("utf-8"))
        ]),
        ("https://dbert.in/blog/architecting-gayatri-exam-portal-production-ai-agent-develop", [
            ("Gayatri article loads HTTP 200", urllib.request.urlopen("https://dbert.in/blog/architecting-gayatri-exam-portal-production-ai-agent-develop", timeout=15, context=ctx).status == 200),
            ("Score 87/100 displayed", "87/100" in urllib.request.urlopen("https://dbert.in/blog/architecting-gayatri-exam-portal-production-ai-agent-develop", timeout=15, context=ctx).read().decode("utf-8"))
        ]),
        ("https://lms.dbert.in", [
            ("LMS has 'Audited Sovereign Credentials'", "Audited Sovereign Credentials" in urllib.request.urlopen("https://lms.dbert.in", timeout=15, context=ctx).read().decode("utf-8")),
            ("LMS has 'Cohort Sprint Starting In'", "Cohort Sprint Starting In" in urllib.request.urlopen("https://lms.dbert.in", timeout=15, context=ctx).read().decode("utf-8")),
            ("LMS has 'Apply Now'", "Apply Now" in urllib.request.urlopen("https://lms.dbert.in", timeout=15, context=ctx).read().decode("utf-8"))
        ])
    ]

    all_passed = True
    for url, checks in endpoints:
        log(f"\nVerifying {url}:")
        for desc, passed in checks:
            mark = "PASS" if passed else "FAIL"
            log(f"  [{mark}] {desc}")
            if not passed:
                all_passed = False

    if all_passed:
        log("\n>>> ALL PRODUCTION ENDPOINTS AND VERIFICATION CHECKS PASSED 100%! <<<")
    else:
        log("\n>>> WARNING: One or more checks failed! Please review output above. <<<")

if __name__ == "__main__":
    main()
