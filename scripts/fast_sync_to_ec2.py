import subprocess
import tarfile
import os
import sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"
ARCHIVE_NAME = "remediation_sync.tar.gz"

FILES_TO_SYNC = [
    "DBERT_Website_LMS_Phase_by_Phase_Fix_Plan.md",
    "apps/portal/.env.production.sample",
    "apps/portal/app.py",
    "apps/portal/services/database/adapter.py",
    "apps/portal/tests/test_postgres_enforcement.py",
    "apps/website/src/app/api/consultation/route.ts",
    "apps/website/src/app/api/contact/route.ts",
    "apps/website/src/app/api/demo-request/route.ts",
    "apps/website/src/app/api/enroll/balance/route.ts",
    "apps/website/src/app/api/enroll/lookup/route.ts",
    "apps/website/src/app/api/payments/create-order/route.ts",
    "apps/website/src/app/api/payments/verify/route.ts",
    "apps/website/src/app/api/payments/webhook/route.ts",
    "apps/website/src/app/api/startups/register/route.ts",
    "dbert-api-package/backend/api/v1/applications/router.py",
    "dbert-api-package/backend/api/v1/auth/router.py",
    "dbert-api-package/backend/api/v1/enrollments/router.py",
    "dbert-api-package/backend/api/v1/learning/router.py",
    "dbert-api-package/backend/api/v1/payments/router.py",
    "dbert-api-package/backend/core/config.py",
    "dbert-api-package/backend/core/database.py",
    "dbert-api-package/backend/schemas/portal.py",
    "dbert-api-package/tests/test_remediation_security.py",
    "scripts/check_services_health.py",
    "scripts/fix_ec2_env_and_services.py",
    "scripts/inspect_ec2_portal.py",
    "scripts/remote_exec.py",
    "scripts/test_api_security_live.py",
    "scripts/verify_production_live.py",
]

def main():
    print(f"1. Creating archive {ARCHIVE_NAME} with {len(FILES_TO_SYNC)} files...")
    with tarfile.open(ARCHIVE_NAME, "w:gz") as tar:
        for f in FILES_TO_SYNC:
            if os.path.exists(f):
                tar.add(f, arcname=f)
                print(f"  Added: {f}")
            else:
                print(f"  Skipped (not found): {f}")
                
    print("2. Uploading archive to EC2 via SCP...")
    scp_cmd = ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", ARCHIVE_NAME, f"{HOST}:{REMOTE_BASE}/"]
    res = subprocess.run(scp_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("SCP failed:\n", res.stderr)
        return 1
    print("  Uploaded archive successfully.")

    print("3. Extracting archive on EC2...")
    extract_cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", HOST, f"cd {REMOTE_BASE} && tar -xzf {ARCHIVE_NAME} && rm -f {ARCHIVE_NAME}"]
    res2 = subprocess.run(extract_cmd, capture_output=True, text=True)
    if res2.returncode != 0:
        print("Remote extraction failed:\n", res2.stderr)
        return 1
    print("  Extracted archive successfully on EC2.")
    
    if os.path.exists(ARCHIVE_NAME):
        os.remove(ARCHIVE_NAME)
    print("4. Done! All remediation files synced in 1 atomic operation.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
