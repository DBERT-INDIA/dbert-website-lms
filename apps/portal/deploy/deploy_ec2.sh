#!/bin/bash
# ====================================================================
# DBERT Unified Platform — Automated EC2 Deployment & DB Migration Script
# ====================================================================

set -e # Exit immediately if a command exits with a non-zero status

REPO_DIR="/var/www/dbert-website-lms"
SQLITE_BACKUP="/var/www/backups/internship_backup_$(date +%Y%m%d_%H%M%S).db"

echo "===================================================================="
echo " Starting EC2 Unified Platform Deployment & Database Migration"
echo "===================================================================="

# 1. Navigate to codebase directory
cd $REPO_DIR

# 2. Pull latest clean codebase from GitHub
echo "[*] Pulling latest updates from GitHub (dbert-website-lms)..."
git fetch origin main
git reset --hard origin/main

# 3. Deploy Next.js Marketing App (apps/website)
echo "[*] Building Next.js Marketing Website..."
cd $REPO_DIR/apps/website
npm install --production=false
npm run build

# 4. Deploy Flask LMS Platform (apps/portal)
echo "[*] Setting up Flask Learning Platform..."
cd $REPO_DIR/apps/portal
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
pip install psycopg2-binary

# 5. Database Migration (SQLite -> PostgreSQL)
if [ -f "$REPO_DIR/apps/portal/internship.db" ]; then
    echo "[*] Backup existing SQLite database to $SQLITE_BACKUP..."
    mkdir -p /var/www/backups
    cp $REPO_DIR/apps/portal/internship.db $SQLITE_BACKUP

    echo "[*] Provisioning PostgreSQL DDL schema..."
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f $REPO_DIR/docs/POSTGRES_SCHEMA.sql

    echo "[*] Migrating 2,329 user accounts & 4,478 applications to PostgreSQL..."
    python3 scripts/migrate_sqlite_to_postgres_data.py \
        --sqlite $REPO_DIR/apps/portal/internship.db \
        --pg-url "postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:5432/$DB_NAME" \
        --schema dbert_internship
else
    echo "[!] No local internship.db file found. Skipping data migration."
fi

# 6. Restart Systemd Daemons
echo "[*] Restarting Systemd services..."
sudo systemctl daemon-reload
sudo systemctl restart dbert-website.service
sudo systemctl restart dbert-portal.service

# 7. Reload Nginx Reverse Proxy
echo "[*] Reloading Nginx configuration..."
sudo nginx -t
sudo systemctl reload nginx

# 8. Health Check Verification
echo "[*] Verifying service health..."
sleep 3

WEBSITE_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3000 || echo "000")
PORTAL_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5000/health || echo "000")

echo "  - Next.js Website (Port 3000): HTTP $WEBSITE_HEALTH"
echo "  - Flask Portal (Port 5000): HTTP $PORTAL_HEALTH"

if [ "$PORTAL_HEALTH" -eq 200 ]; then
    echo "===================================================================="
    echo " [+] SUCCESS: Deployment & Database Migration Completed Cleanly!"
    echo "===================================================================="
else
    echo "[!] WARNING: Portal health check returned HTTP $PORTAL_HEALTH. Inspect systemctl status dbert-portal.service"
fi
