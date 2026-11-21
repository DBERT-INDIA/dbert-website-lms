#!/usr/bin/env python3
"""
scripts/deploy_analytics_to_ec2.py
================================================================================
Automated Deployment Script for DBERT Universal Analytics & SEO Intelligence
================================================================================
"""

import os
import subprocess
import sys

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

FILES_TO_UPLOAD = [
    # Next.js frontend & API
    ("apps/website/src/components/analytics/TrafficAttributionTracker.tsx", f"{REMOTE_BASE}/apps/website/src/components/analytics/TrafficAttributionTracker.tsx"),
    ("apps/website/src/app/api/telemetry/traffic/route.ts", f"{REMOTE_BASE}/apps/website/src/app/api/telemetry/traffic/route.ts"),
    ("apps/website/src/app/layout.tsx", f"{REMOTE_BASE}/apps/website/src/app/layout.tsx"),
    # Portal backend & templates
    ("apps/portal/routes/admin.py", f"{REMOTE_BASE}/apps/portal/routes/admin.py"),
    ("apps/portal/templates/admin.html", f"{REMOTE_BASE}/apps/portal/templates/admin.html"),
    ("apps/portal/templates/admin_analytics.html", f"{REMOTE_BASE}/apps/portal/templates/admin_analytics.html"),
    # Scripts
    ("scripts/parse_nginx_traffic.py", f"{REMOTE_BASE}/scripts/parse_nginx_traffic.py"),
    ("scripts/ingest_gsc_data.py", f"{REMOTE_BASE}/scripts/ingest_gsc_data.py"),
    ("scripts/traffic_and_ranking_intelligence.py", f"{REMOTE_BASE}/scripts/traffic_and_ranking_intelligence.py"),
    # Data summaries
    ("data/traffic_analytics_summary.json", f"{REMOTE_BASE}/data/traffic_analytics_summary.json"),
    ("data/seo_keyword_intelligence.json", f"{REMOTE_BASE}/data/seo_keyword_intelligence.json"),
]

def run_cmd(cmd, check=True):
    print(f">> {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print(res.stderr.strip(), file=sys.stderr)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with code {res.returncode}")
    return res

def main():
    print("=== 1. UPLOADING FILES TO EC2 ===")
    for local_p, remote_p in FILES_TO_UPLOAD:
        if not os.path.exists(local_p):
            print(f"Skipping missing: {local_p}")
            continue
        # Ensure remote directory exists
        remote_dir = os.path.dirname(remote_p).replace('\\', '/')
        mkdir_cmd = f'ssh -i "{PEM_KEY}" -o StrictHostKeyChecking=no {REMOTE_HOST} "mkdir -p {remote_dir}"'
        run_cmd(mkdir_cmd)

        scp_cmd = f'scp -i "{PEM_KEY}" -o StrictHostKeyChecking=no "{local_p}" {REMOTE_HOST}:{remote_p}'
        run_cmd(scp_cmd)
        print(f"Uploaded: {local_p} -> {remote_p}")

    print("\n=== 2. RUNNING NGINX PARSING & GSC INGESTION ON EC2 ===")
    remote_analytics_cmd = (
        f'ssh -i "{PEM_KEY}" -o StrictHostKeyChecking=no {REMOTE_HOST} '
        f'"cd {REMOTE_BASE} && python3 scripts/parse_nginx_traffic.py && python3 scripts/ingest_gsc_data.py && python3 scripts/traffic_and_ranking_intelligence.py --summary"'
    )
    run_cmd(remote_analytics_cmd)

    print("\n=== 3. BUILDING NEXT.JS STANDALONE ON EC2 & RESTARTING SERVICES ===")
    build_and_restart_cmd = (
        f'ssh -i "{PEM_KEY}" -o StrictHostKeyChecking=no {REMOTE_HOST} '
        f'"bash -c \'cd {REMOTE_BASE}/apps/website && export NODE_ENV=production && npm run build && '
        f'if [ -f .next/server/app/sitemap.xml.body ]; then cp .next/server/app/sitemap.xml.body public/sitemap.xml; fi && '
        f'cp -r public .next/standalone/ 2>/dev/null || true && '
        f'cp -r public .next/standalone/apps/website/ 2>/dev/null || true && '
        f'if [ -f .next/server/app/sitemap.xml.body ]; then cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml 2>/dev/null || true; cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true; fi && '
        f'mkdir -p {REMOTE_BASE}/data && rm -rf {REMOTE_BASE}/apps/website/.next/standalone/data && ln -s {REMOTE_BASE}/data {REMOTE_BASE}/apps/website/.next/standalone/data && '
        f'sudo systemctl restart dbert-website.service && sudo systemctl restart dbert-portal.service && '
        f'sleep 2 && systemctl is-active dbert-website.service && systemctl is-active dbert-portal.service\'"'
    )
    run_cmd(build_and_restart_cmd)

    print("\n=== DEPLOYMENT AND VERIFICATION COMPLETE ===")

if __name__ == '__main__':
    main()
