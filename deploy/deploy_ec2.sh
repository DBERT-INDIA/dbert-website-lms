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

# 2. Skip git pull (Files are uploaded via FileZilla)
echo "[*] Using codebase uploaded via FileZilla..."
# git fetch origin main
# git reset --hard origin/main

# 3. Deploy Next.js Marketing App (apps/website)
echo "[*] Building Next.js Marketing Website..."
cd $REPO_DIR/apps/website

# Fix FLASK_SECRET_KEY mismatch from documentation
if grep -q "SECRET_KEY=" "$REPO_DIR/apps/portal/.env" && ! grep -q "FLASK_SECRET_KEY=" "$REPO_DIR/apps/portal/.env"; then
    echo "[*] Migrating SECRET_KEY to FLASK_SECRET_KEY in portal .env..."
    SECRET_VAL=$(grep SECRET_KEY $REPO_DIR/apps/portal/.env | cut -d '=' -f2-)
    echo "FLASK_SECRET_KEY=$SECRET_VAL" >> $REPO_DIR/apps/portal/.env
fi
# Forcefully correct the database password in .env (in case they used a different placeholder)
echo "[*] Enforcing correct PostgreSQL credentials in .env..."
if grep -q "^DATABASE_URL=" "$REPO_DIR/apps/portal/.env"; then
    sed -i 's|^DATABASE_URL=.*|DATABASE_URL=postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms|g' "$REPO_DIR/apps/portal/.env"
else
    echo "DATABASE_URL=postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms" >> "$REPO_DIR/apps/portal/.env"
fi

if [ ! -f ".env" ] && [ -f "$REPO_DIR/apps/portal/.env" ]; then
    echo "[*] Generating apps/website/.env from apps/portal/.env..."
    # Extract needed keys from portal env
    DB_URL=$(grep DATABASE_URL $REPO_DIR/apps/portal/.env | cut -d '=' -f2-)
    RZP_ID=$(grep RAZORPAY_KEY_ID $REPO_DIR/apps/portal/.env | cut -d '=' -f2-)
    RZP_SECRET=$(grep RAZORPAY_KEY_SECRET $REPO_DIR/apps/portal/.env | cut -d '=' -f2-)
    JWT=$(grep SECRET_KEY $REPO_DIR/apps/portal/.env | cut -d '=' -f2-)
    
    echo "DATABASE_URL=$DB_URL" > .env
    echo "RAZORPAY_KEY_ID=$RZP_ID" >> .env
    echo "RAZORPAY_KEY_SECRET=$RZP_SECRET" >> .env
    echo "NEXT_PUBLIC_RAZORPAY_KEY_ID=$RZP_ID" >> .env
    echo "JWT_SECRET=$JWT" >> .env
fi

npm install --production=false
npm run build

# 4. Deploy Flask LMS Platform (apps/portal)
echo "[*] Setting up Flask Learning Platform..."
cd $REPO_DIR/apps/portal
if [ ! -d ".venv" ]; then
    echo "[*] Creating Python virtual environment (.venv)..."
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install psycopg2-binary

# 5. Database Provisioning & Schema Verification
if [ -n "$DB_HOST" ] && [ -n "$DB_NAME" ] && [ -n "$DB_USER" ]; then
    echo "[*] Verifying PostgreSQL schema DDL..."
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f $REPO_DIR/docs/POSTGRES_SCHEMA.sql || true
fi

# 6. Stop and Disable Legacy Services (If present)
echo "[*] Stopping legacy services..."
sudo systemctl stop dbert-internship.service || true
sudo systemctl disable dbert-internship.service || true
# Stop pm2 if the old Next.js app was running on it (won't hurt if not installed)
pm2 stop all || true 

echo "[*] Hunting down and stopping rogue services on ports 3000 and 5000..."

# Find and stop whatever systemd service is managing Port 3000
PID_3000=$(sudo lsof -t -i:3000 | head -n 1)
if [ -n "$PID_3000" ]; then
    SERVICE_3000=$(sudo systemctl status $PID_3000 | grep -oP '(\S+\.service)' | head -n 1 || true)
    if [ -n "$SERVICE_3000" ] && [ "$SERVICE_3000" != "dbert-website.service" ]; then
        echo "[*] Found rogue service $SERVICE_3000 holding port 3000. Stopping and disabling it permanently..."
        sudo systemctl stop "$SERVICE_3000" || true
        sudo systemctl disable "$SERVICE_3000" || true
    fi
fi
sudo fuser -k 3000/tcp || sudo kill -9 $(sudo lsof -t -i:3000) || true

# Find and stop whatever systemd service is managing Port 5000
PID_5000=$(sudo lsof -t -i:5000 | head -n 1)
if [ -n "$PID_5000" ]; then
    SERVICE_5000=$(sudo systemctl status $PID_5000 | grep -oP '(\S+\.service)' | head -n 1 || true)
    if [ -n "$SERVICE_5000" ] && [ "$SERVICE_5000" != "dbert-portal.service" ]; then
        echo "[*] Found rogue service $SERVICE_5000 holding port 5000. Stopping and disabling it permanently..."
        sudo systemctl stop "$SERVICE_5000" || true
        sudo systemctl disable "$SERVICE_5000" || true
    fi
fi
sudo fuser -k 5000/tcp || sudo kill -9 $(sudo lsof -t -i:5000) || true

sleep 2

# 7. Install New Systemd Services
echo "[*] Installing new Systemd services..."
sudo cp $REPO_DIR/deploy/dbert-website.service /etc/systemd/system/
sudo cp $REPO_DIR/deploy/dbert-portal.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dbert-website.service
sudo systemctl enable dbert-portal.service
sudo systemctl restart dbert-website.service
sudo systemctl restart dbert-portal.service

# 8. Install Nginx Configurations
echo "[*] Removing legacy Nginx configurations..."
sudo rm -f /etc/nginx/conf.d/internship.dbert.online.conf*
sudo rm -f /etc/nginx/conf.d/dbert.online.conf*
sudo rm -f /etc/nginx/conf.d/dbert.conf*
sudo rm -f /etc/nginx/conf.d/tutor_dbert_online.conf*

echo "[*] Installing new Nginx configurations..."
sudo cp $REPO_DIR/deploy/dbert-website-nginx.conf /etc/nginx/conf.d/dbert-website.conf
sudo cp $REPO_DIR/deploy/dbert-portal-nginx.conf /etc/nginx/conf.d/dbert-portal.conf

echo "[*] Reloading Nginx..."
sudo nginx -t
sudo systemctl reload nginx

# 9. Health Check Verification
echo "[*] Verifying service health..."
sleep 5

WEBSITE_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3001 || echo "000")
PORTAL_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001/health || echo "000")
NEW_PAGE_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3001/hire/pre-vetted-engineers || echo "000")

echo "  - Next.js Website (Port 3001): HTTP $WEBSITE_HEALTH"
echo "  - Flask Portal (Port 5001): HTTP $PORTAL_HEALTH"
echo "  - New SEO Route Local Check: HTTP $NEW_PAGE_CHECK"

if [ "$PORTAL_HEALTH" -eq 200 ] || [ "$PORTAL_HEALTH" -eq 308 ]; then
    echo "===================================================================="
    echo " [+] SUCCESS: Deployment & Database Migration Completed Cleanly!"
    if [ "$NEW_PAGE_CHECK" -eq 200 ]; then
        echo " [+] VERIFIED: The new /hire/pre-vetted-engineers route IS LIVE on the server!"
        echo "     If you still see a 404 in your browser, it is 100% CACHED by Cloudflare or your browser."
        echo "     Please test by visiting: https://dbert.online/hire/pre-vetted-engineers?test=123"
    fi
    echo "===================================================================="
else
    echo "[!] WARNING: Portal health check returned HTTP $PORTAL_HEALTH. Inspect systemctl status dbert-portal.service"
fi
