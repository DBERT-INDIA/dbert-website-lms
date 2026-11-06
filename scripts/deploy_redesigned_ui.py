import subprocess
import os

ssh_key = r"C:\Users\user\.ssh\dbert-production-server.pem"
server = "ubuntu@3.26.237.171"
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
remote_base = "/var/www/dbert-website-lms"

print("=" * 80)
print("DEPLOYING EXECUTIVE REDESIGNED UI TO EC2 PRODUCTION (3.26.237.171)")
print("=" * 80)

# 1. SCP verify.module.css
css_local = os.path.join(base_dir, "apps", "website", "src", "app", "verify", "verify.module.css")
subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", css_local, f"{server}:{remote_base}/apps/website/src/app/verify/verify.module.css"], check=True)

# 2. SCP page.tsx
page_local = os.path.join(base_dir, "apps", "website", "src", "app", "verify", "page.tsx")
subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", page_local, f"{server}:{remote_base}/apps/website/src/app/verify/page.tsx"], check=True)

# 3. SCP [certId]/page.tsx
dynamic_page_local = os.path.join(base_dir, "apps", "website", "src", "app", "verify", "[certId]", "page.tsx")
subprocess.run(["scp", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", dynamic_page_local, f"{server}:{remote_base}/apps/website/src/app/verify/[certId]/page.tsx"], check=True)

print("All redesigned UI files uploaded to EC2 successfully!")

# 4. Build Next.js and restart service on EC2
print("\nBuilding Next.js on EC2 and restarting service...")
build_cmd = """
cd /var/www/dbert-website-lms/apps/website
export NODE_ENV=production
npm run build
sudo systemctl restart dbert-website.service
sleep 3
systemctl status dbert-website.service --no-pager
"""
build_res = subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, build_cmd], capture_output=True)
print("Build output:")
print(build_res.stdout.decode("utf-8", errors="ignore"))
if build_res.stderr:
    print("Build stderr:", build_res.stderr.decode("utf-8", errors="ignore"))

# 5. Test Live Public URLs
print("\n" + "=" * 80)
print("TESTING LIVE PUBLIC ENDPOINTS")
print("=" * 80)

test_cmd = """
echo "=== 1. SSR Route https://dbert.in/verify/CERT-DBERT-2026-DA-001 ==="
curl -s 'https://dbert.in/verify/CERT-DBERT-2026-DA-001' | grep -o 'Kushal Agarwal' || echo "Not found"

echo "=== 2. Check for MSME references (should be None in verify content) ==="
curl -s 'https://dbert.in/verify?certid=CERT-DBERT-2026-DA-001' | grep -o 'MSME' || echo "Zero MSME in verify page"

echo "=== 3. Next.js API Response ==="
curl -s 'https://dbert.in/api/verify?certid=CERT-DBERT-2026-DA-001'
"""
t_res = subprocess.run(["ssh", "-i", ssh_key, "-o", "StrictHostKeyChecking=no", server, test_cmd], capture_output=True)
print(t_res.stdout.decode("utf-8", errors="ignore"))
print("=" * 80)
print("DEPLOYMENT & TESTING COMPLETE!")
