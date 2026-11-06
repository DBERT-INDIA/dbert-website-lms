import subprocess
import os
import sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

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
    print(f"Syncing {len(FILES_TO_SYNC)} files to EC2 ({HOST}:{REMOTE_BASE})...")
    for rel_path in FILES_TO_SYNC:
        local_path = os.path.abspath(rel_path)
        if not os.path.exists(local_path):
            print(f"Warning: Local file not found: {local_path}")
            continue
        
        remote_path = f"{REMOTE_BASE}/{rel_path.replace(os.sep, '/')}"
        remote_dir = os.path.dirname(remote_path).replace("\\", "/")
        
        # Ensure remote dir exists
        mkdir_cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", HOST, f"mkdir -p '{remote_dir}'"]
        subprocess.run(mkdir_cmd, check=True)
        
        # SCP file
        scp_cmd = ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", local_path, f"{HOST}:{remote_path}"]
        res = subprocess.run(scp_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Failed to copy {rel_path}: {res.stderr}")
            return 1
        else:
            print(f"  [Synced] {rel_path} -> {remote_path}")
            
    print("\nAll files successfully synced to EC2.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
