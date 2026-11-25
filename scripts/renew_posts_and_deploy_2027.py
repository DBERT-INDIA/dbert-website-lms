"""Master deployment & verification script for the 2027 Posts, Blogs & ₹1,999 Funnel Plan.

1. Syncs & runs scripts/renew_posts_2027_pg.py on EC2 PostgreSQL.
2. Packages all modified portal + website files into a single tar.gz archive for 1-shot SCP upload.
3. Extracts files on EC2, restarts dbert-portal.service, runs Next.js standalone build + asset sync + data symlink, and restarts dbert-website.service.
4. Verifies HTTP 200 across key endpoints on dbert.in and lms.dbert.in.
"""

import os
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"
LOCAL_BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SSH_OPTS = f'-i "{PEM_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=20'


def run(cmd):
    print(f"\n>>> {cmd}", flush=True)
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {res.returncode}: {cmd}")


def verify_live():
    import glob
    blogs = sorted(glob.glob(os.path.join(LOCAL_BASE, "apps", "website", "src", "content", "blog", "*.mdx")))
    missing = [os.path.basename(b) for b in blogs if "enroll/1999" not in open(b, encoding="utf-8").read()]
    print(f"Local MDX blogs with /enroll/1999: {len(blogs) - len(missing)}/{len(blogs)}", flush=True)
    if missing:
        raise RuntimeError(f"Blogs missing /enroll/1999: {missing}")

    urls = [
        "https://dbert.in/sitemap.xml",
        "https://dbert.in/llms.txt",
        "https://dbert.in/enroll/1999",
        "https://dbert.in/internships",
        "https://dbert.in/internships/data-analytics",
        "https://dbert.in/internships/ai-agent-development/bengaluru",
        "https://dbert.in/internships/generative-ai/remote",
        "https://dbert.in/learners/courses/full-stack-development",
        "https://dbert.in/blog/paid-ai-internship-india-guide-2026",
        "https://dbert.in/blog/inside-dbert-engineering-sprints-rag-saas-security-qa-ocr-bots",
        "https://lms.dbert.in/internships",
        "https://lms.dbert.in/internships/generative-ai",
        "https://lms.dbert.in/internships/data-analytics",
        "https://lms.dbert.in/sitemap.xml",
    ]
    failed = 0
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "DBERT-Deploy-Verifier/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                print(f"  [{resp.status}] {u}", flush=True)
        except Exception as e:
            print(f"  [FAIL] {u} -> {e}", flush=True)
            failed += 1

    content_checks = [
        ("https://dbert.in/sitemap.xml", ["<loc>https://dbert.in/enroll/1999</loc>", "<priority>0.98</priority>", "/internships/generative-ai/remote", "/internships/ai-agent-development/bengaluru"]),
        ("https://dbert.in/blog/inside-dbert-engineering-sprints-rag-saas-security-qa-ocr-bots", ["/enroll/1999", "Verified Certificate", "5,000+ Stipend", "Placement Assistance"]),
        ("https://dbert.in/blog/equity-for-services", ["/enroll/1999", "Verified Certificate"]),
        ("https://dbert.in/internships/data-analytics", ["/internships/data-analytics/bengaluru", "/internships/data-analytics/mumbai", "/enroll/1999"]),
        ("https://dbert.in/learners/courses/full-stack-development", ["/enroll/1999", "/internships/full-stack-development/bengaluru", "Verified Certificate"]),
        ("https://lms.dbert.in/internships", ["dbert.in/enroll/1999", "Stipend"]),
        ("https://lms.dbert.in/sitemap.xml", ["langgraph-multi-agent-orchestration-intern-bengaluru-2027", "docker-multi-stage-container-engineering-intern-mumbai-2027"]),
    ]
    for url, needles in content_checks:
        req = urllib.request.Request(url, headers={"User-Agent": "DBERT-Audit/1.0"})
        body = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", errors="replace")
        for n in needles:
            ok = n in body
            tag = "OK" if ok else "MISS"
            print(f"  [{tag}] {url} -> {n}", flush=True)
            if not ok:
                failed += 1

    if failed:
        raise RuntimeError(f"{failed} checks failed verification!")
    print("\nALL DEPLOYMENTS AND VERIFICATIONS PASSED!", flush=True)


def main():
    if "--verify-only" in sys.argv:
        verify_live()
        return
    files_to_sync = [
        "scripts/renew_posts_2027_pg.py",
        "apps/portal/app.py",
        "apps/portal/templates/post_listings.html",
        "apps/website/src/data/geo_domains.config.ts",
        "apps/website/src/app/sitemap.ts",
        "apps/website/src/app/internships/page.tsx",
        "apps/website/src/app/internships/[role]/page.tsx",
        "apps/website/src/app/internships/[role]/[city]/page.tsx",
        "apps/website/src/app/learners/courses/page.tsx",
        "apps/website/src/app/learners/fellowship/page.tsx",
        "apps/website/src/app/blog/[slug]/page.tsx",
        "apps/website/src/components/blog/DynamicBlogReader.tsx",
        "apps/website/src/components/courses/FellowshipTrackTemplate.tsx",
        "apps/website/public/llms.txt",
        "apps/website/public/llms-full.txt",
    ]
    blog_dir = os.path.join(LOCAL_BASE, "apps", "website", "src", "content", "blog")
    for fname in sorted(os.listdir(blog_dir)):
        if fname.endswith(".mdx"):
            files_to_sync.append(f"apps/website/src/content/blog/{fname}")

    tar_path = os.path.join(tempfile.gettempdir(), "dbert_2027_funnel_bundle.tar.gz")
    print(f"=== 1. Bundling {len(files_to_sync)} files into {tar_path} ===", flush=True)
    with tarfile.open(tar_path, "w:gz") as tar:
        for rel in files_to_sync:
            full = os.path.join(LOCAL_BASE, rel.replace("/", os.sep))
            if not os.path.exists(full):
                raise FileNotFoundError(f"Missing local file: {full}")
            tar.add(full, arcname=rel)

    print("=== 2. Uploading bundle to EC2 via single SCP ===", flush=True)
    run(f'scp {SSH_OPTS} "{tar_path}" {REMOTE_HOST}:/tmp/dbert_2027_funnel_bundle.tar.gz')

    print("=== 3. Extracting bundle, syncing PostgreSQL, restarting portal & building Next.js standalone ===", flush=True)
    remote_cmd = (
        f"tar -xzf /tmp/dbert_2027_funnel_bundle.tar.gz -C {REMOTE_BASE} && "
        f"/var/www/dbert-website-lms/apps/portal/.venv/bin/python {REMOTE_BASE}/scripts/renew_posts_2027_pg.py && "
        "sudo systemctl restart dbert-portal.service && sleep 2 && systemctl is-active dbert-portal.service && "
        f"cd {REMOTE_BASE}/apps/website && "
        "export NODE_ENV=production && "
        "npm run build && "
        "if [ -f .next/server/app/sitemap.xml.body ]; then cp .next/server/app/sitemap.xml.body public/sitemap.xml; fi && "
        "cp -r public .next/standalone/ 2>/dev/null || true && "
        "cp -r public .next/standalone/apps/website/ 2>/dev/null || true && "
        "if [ -f .next/server/app/sitemap.xml.body ]; then "
        "  cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml 2>/dev/null || true; "
        "  cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true; "
        "fi && "
        f"mkdir -p {REMOTE_BASE}/data && "
        f"rm -rf {REMOTE_BASE}/apps/website/.next/standalone/data && "
        f"ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/data && "
        "sudo systemctl restart dbert-website.service && sleep 3 && systemctl is-active dbert-website.service"
    )
    run(f'ssh {SSH_OPTS} {REMOTE_HOST} "{remote_cmd}"')

    print("\n=== 4. Verify live URLs & content assertions ===", flush=True)
    verify_live()


if __name__ == "__main__":
    main()
