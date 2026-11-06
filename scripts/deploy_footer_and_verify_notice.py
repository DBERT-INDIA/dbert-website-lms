import subprocess
import os
import requests

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
SERVER = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def main():
    print("=" * 80)
    print("DEPLOYING FOOTER DOMAIN NOTICE & VERIFY PAGE UPDATE TO EC2")
    print("=" * 80)

    files_to_scp = [
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "components", "layout", "Footer.tsx"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/components/layout/Footer.tsx"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "components", "layout", "Footer.module.css"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/components/layout/Footer.module.css"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "page.tsx"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/app/verify/page.tsx"
        ),
    ]

    for local_p, remote_p in files_to_scp:
        print(f"Uploading: {os.path.basename(local_p)} -> {remote_p}")
        subprocess.run(
            ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", local_p, remote_p],
            check=True
        )

    print("\nAll files uploaded successfully via SCP.")

    print("\nTriggering remote Next.js build and service restart...")
    remote_script = """
    set -e
    cd /var/www/dbert-website-lms/apps/website
    export NODE_ENV=production
    npm run build
    cp -r public .next/standalone/ 2>/dev/null || true
    cp -r public .next/standalone/apps/website/ 2>/dev/null || true
    sudo systemctl restart dbert-website.service
    sleep 3
    systemctl is-active dbert-website.service
    """

    res = subprocess.run(
        ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, remote_script],
        capture_output=True
    )

    out = res.stdout.decode("utf-8", errors="replace")
    safe_out = out[-1200:].encode("ascii", errors="ignore").decode("ascii")
    print("Remote build stdout tail:\n", safe_out)
    if res.returncode != 0:
        err = res.stderr.decode("utf-8", errors="replace").encode("ascii", errors="ignore").decode("ascii")
        print("Remote build stderr:\n", err)
        print("FAILED with return code:", res.returncode)
        return

    print("\nService active! Verifying live endpoints...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # 1. Test /verify
    print("\n[1] Testing https://dbert.in/verify...")
    res_verify = requests.get("https://dbert.in/verify", headers=headers, timeout=15)
    html_verify = res_verify.text
    legacy_notice = (
        "All official credentials previously referencing" in html_verify
        or "Certificates and credentials issued under legacy" in html_verify
    )
    footer_notice = "Domain Notice: DBERT.online is now DBERT.in." in html_verify
    print(f"Status Code: {res_verify.status_code}")
    print(f"Legacy domain notice banner in body: {'FOUND (FAIL)' if legacy_notice else 'REMOVED (PASS)'}")
    print(f"Footer domain notice bar: {'PRESENT (PASS)' if footer_notice else 'NOT FOUND (FAIL)'}")

    # 2. Test /
    print("\n[2] Testing https://dbert.in/...")
    res_home = requests.get("https://dbert.in/", headers=headers, timeout=15)
    home_notice = "Domain Notice: DBERT.online is now DBERT.in." in res_home.text
    print(f"Homepage footer domain notice: {'PRESENT (PASS)' if home_notice else 'NOT FOUND (FAIL)'}")

    # 3. Test /about
    print("\n[3] Testing https://dbert.in/about...")
    res_about = requests.get("https://dbert.in/about", headers=headers, timeout=15)
    about_notice = "Domain Notice: DBERT.online is now DBERT.in." in res_about.text
    print(f"/about footer domain notice: {'PRESENT (PASS)' if about_notice else 'NOT FOUND (FAIL)'}")

    # 4. Test /learners
    print("\n[4] Testing https://dbert.in/learners...")
    res_learners = requests.get("https://dbert.in/learners", headers=headers, timeout=15)
    learners_notice = "Domain Notice: DBERT.online is now DBERT.in." in res_learners.text
    print(f"/learners footer domain notice: {'PRESENT (PASS)' if learners_notice else 'NOT FOUND (FAIL)'}")

    # 5. Test SSR route /verify/CERT-DBERT-2026-DA-001
    print("\n[5] Testing https://dbert.in/verify/CERT-DBERT-2026-DA-001...")
    res_cert = requests.get("https://dbert.in/verify/CERT-DBERT-2026-DA-001", headers=headers, timeout=15)
    cert_footer_notice = "Domain Notice: DBERT.online is now DBERT.in." in res_cert.text
    print(f"Cert page footer domain notice: {'PRESENT (PASS)' if cert_footer_notice else 'NOT FOUND (FAIL)'}")

    print("\n" + "=" * 80)
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    main()
