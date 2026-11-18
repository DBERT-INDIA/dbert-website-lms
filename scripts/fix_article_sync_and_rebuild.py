import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"

# 1. SCP app.py
print("Uploading fixed apps/portal/app.py...")
subprocess.run(["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "apps/portal/app.py", f"{HOST}:{REMOTE_BASE}/apps/portal/app.py"], check=True)

# 2. Remote execution
remote_cmds = """
cd /var/www/dbert-website-lms/apps/portal
# Remove erroneous nested dirs if they exist
rm -rf /var/www/dbert-website-lms/apps/data /var/www/dbert-website-lms/apps/apps

# Run fixed sync
.venv/bin/python -c "
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db, _sync_published_articles_registry
with get_db() as conn:
    _sync_published_articles_registry(conn)
    print('Sync completed!')
"

echo "Checking synced file length:"
cat /var/www/dbert-website-lms/data/published_articles.json | grep '"title"' | wc -l

# Rebuild website
cd /var/www/dbert-website-lms/apps/website
export NODE_ENV=production
npm run build
cp -r public .next/standalone/ 2>/dev/null || true
cp -r public .next/standalone/apps/website/ 2>/dev/null || true
mkdir -p /var/www/dbert-website-lms/data
rm -rf /var/www/dbert-website-lms/apps/website/.next/standalone/data
ln -s /var/www/dbert-website-lms/data /var/www/dbert-website-lms/apps/website/.next/standalone/data

sudo systemctl restart dbert-portal.service
sudo systemctl restart dbert-website.service
sleep 2
systemctl is-active dbert-portal.service
systemctl is-active dbert-website.service
"""

print("Executing sync, rebuild, and service restart on EC2...")
p = subprocess.run(["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", HOST, remote_cmds], capture_output=True, text=True)
print("STDOUT:\n", p.stdout)
if p.stderr:
    print("STDERR:\n", p.stderr)
