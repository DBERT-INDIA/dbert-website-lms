#!/bin/bash
# ==============================================================================
# DBERT Ecosystem — Unified Production EC2 Provisioning & Deployment Script
# Hosts: https://dbert.in (Next.js :3001) & https://lms.dbert.in (Gunicorn :5001)
# ==============================================================================
set -Eeuo pipefail

REPO_DIR="/var/www/dbert-website-lms"
WEBSITE_DIR="$REPO_DIR/apps/website"
PORTAL_DIR="$REPO_DIR/apps/portal"
API_DIR="$REPO_DIR/dbert-api-package"
BACKUP_DIR="/var/www/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "===================================================================="
echo " Starting DBERT Production Deployment — $(date)"
echo " Repository: $REPO_DIR"
echo "===================================================================="

# ── 1. Permission and Directory Preparation ──────────────────────────────────
mkdir -p "$BACKUP_DIR"
mkdir -p /var/www/certbot
mkdir -p "$PORTAL_DIR/uploads"
sudo chown -R ubuntu:ubuntu "$REPO_DIR" 2>/dev/null || true
chmod -R 775 "$PORTAL_DIR/uploads" 2>/dev/null || true

# ── 2. System Packages Verification ──────────────────────────────────────────
echo "[*] Checking system packages (PostgreSQL, Nginx, Python3, Node.js, Certbot)..."
if ! command -v psql &> /dev/null; then
    echo "[!] Installing PostgreSQL..."
    sudo apt-get update -y -q
    sudo apt-get install -y postgresql postgresql-contrib -q
    sudo systemctl enable postgresql
    sudo systemctl start postgresql
fi

if ! command -v nginx &> /dev/null; then
    echo "[!] Installing Nginx..."
    sudo apt-get install -y nginx -q
    sudo systemctl enable nginx
    sudo systemctl start nginx
fi

if ! command -v node &> /dev/null; then
    echo "[!] Installing Node.js 20 LTS..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs -q
fi

if ! command -v certbot &> /dev/null; then
    echo "[!] Installing Certbot & Python3-certbot-nginx..."
    sudo apt-get install -y certbot python3-certbot-nginx -q
fi

# ── 3. PostgreSQL Database Setup ──────────────────────────────────────────────
echo "[*] Configuring PostgreSQL database..."
# Finding PRE-06 / R4-01 remediation: Secure dynamic password generation or ingestion
if [ -f "$PORTAL_DIR/.env" ] && grep -q '^DATABASE_URL=' "$PORTAL_DIR/.env"; then
    DB_PASS=$(grep '^DATABASE_URL=' "$PORTAL_DIR/.env" | sed -E 's|.*://[^:]+:([^@]+)@.*|\1|' || echo "")
fi
DB_PASS="${DB_PASS:-${DBERT_DB_PASSWORD:-$(openssl rand -hex 24)}}"

sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='dbert_user'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE USER dbert_user WITH PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "ALTER USER dbert_user WITH PASSWORD '$DB_PASS';" 2>/dev/null || true

sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='dbert_lms'" | grep -q 1 || {
    echo "[*] Creating database dbert_lms..."
    sudo -u postgres psql -c "CREATE DATABASE dbert_lms OWNER dbert_user;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE dbert_lms TO dbert_user;"
    if [ -f "$REPO_DIR/docs/POSTGRES_SCHEMA.sql" ]; then
        echo "[*] Applying initial PostgreSQL schema from docs/POSTGRES_SCHEMA.sql..."
        PGPASSWORD="$DB_PASS" psql -h localhost -U dbert_user -d dbert_lms -f "$REPO_DIR/docs/POSTGRES_SCHEMA.sql" || true
    fi
}

# ── 4. Setup DBERT LMS Portal (Python / Flask / Gunicorn) ─────────────────────
echo "[*] Setting up DBERT LMS Portal (apps/portal)..."
cd "$PORTAL_DIR"

if [ ! -f ".env" ]; then
    echo "[!] No .env found in apps/portal. Generating from .env.production.sample..."
    cp .env.production.sample .env
    # Inject dynamically generated secure password
    sed -i "s|DBERT_SECURE_PASSWORD_123|$DB_PASS|g" .env
    echo "[!] IMPORTANT: Update remaining secrets in $PORTAL_DIR/.env if needed."
fi

if [ ! -d ".venv" ]; then
    echo "[*] Creating Python virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install psycopg2-binary gunicorn -q

# Migrate data from SQLite to PostgreSQL if internship.db exists
if [ -f "internship.db" ]; then
    echo "[*] Migrating existing database records from SQLite to PostgreSQL..."
    PG_URL="postgresql://dbert_user:${DB_PASS}@localhost:5432/dbert_lms"
    python scripts/migrate_sqlite_to_postgres_data.py --sqlite internship.db --pg-url "$PG_URL" || true
    # Archive SQLite file to prevent accidental fallback (Finding R4-12)
    mv internship.db "$BACKUP_DIR/internship_${TIMESTAMP}.db" 2>/dev/null || true
fi
deactivate

# ── 5. Setup DBERT Main Website (Next.js / Node.js Standalone) ─────────────────
echo "[*] Setting up DBERT Main Website (apps/website)..."
cd "$WEBSITE_DIR"

if [ ! -f ".env" ]; then
    echo "[*] Generating .env for apps/website..."
    cat << EOF > .env
NEXT_PUBLIC_SITE_URL=https://dbert.in
NEXT_PUBLIC_LMS_URL=https://lms.dbert.in
NEXT_PUBLIC_GA_ID=G-GZ17KZ7MDW
PORT=3001
NODE_ENV=production
DATABASE_URL=postgresql://dbert_user:${DB_PASS}@localhost:5432/dbert_lms
JWT_SECRET=$(openssl rand -hex 32)
EOF
fi

if [ ! -d "node_modules" ]; then
    echo "[*] Installing npm dependencies..."
    npm install --production=false
fi

echo "[*] Pushing Prisma database schema to PostgreSQL..."
npx prisma db push --skip-generate || true

echo "[*] Compiling Next.js production standalone build..."
npm run build

echo "[*] Bundling static and public assets into standalone directory..."
mkdir -p .next/standalone/.next
cp -r public .next/standalone/public 2>/dev/null || true
cp -r .next/static .next/standalone/.next/static 2>/dev/null || true

# ── 5b. Setup DBERT REST API (FastAPI / Uvicorn) ──────────────────────────────
echo "[*] Setting up DBERT REST API (dbert-api-package)..."
cd "$API_DIR"

if [ ! -f ".env" ]; then
    echo "[*] Generating .env for dbert-api-package..."
    cp .env.production.sample .env
    sed -i "s|GENERATE_STRONG_DATABASE_PASSWORD|$DB_PASS|g" .env
    sed -i "s|dbert_prod_user|dbert_user|g" .env
    sed -i "s|dbert_production|dbert_lms|g" .env
    sed -i "s|localhost:5432|localhost:5432|g" .env
    sed -i "s|GENERATE_STRONG_RANDOM_SECRET_KEY_AT_LEAST_64_CHARACTERS|$(openssl rand -hex 32)|g" .env
    sed -i "s|GENERATE_LONG_SECURE_CRON_SECRET|$(openssl rand -hex 24)|g" .env
    sed -i "s|https://lms.dbert.in|https://lms.dbert.in,https://api.dbert.in|g" .env
fi

if [ ! -d ".venv" ]; then
    echo "[*] Creating Python virtual environment for FastAPI..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip -q
pip install -r backend/requirements.txt -q
deactivate

# ── 6. Install & Configure Systemd Services ──────────────────────────────────
echo "[*] Installing systemd daemons..."
sudo cp "$REPO_DIR/deploy/dbert-website.service" /etc/systemd/system/dbert-website.service
sudo cp "$REPO_DIR/deploy/dbert-portal.service" /etc/systemd/system/dbert-portal.service
sudo cp "$REPO_DIR/deploy/dbert-api.service" /etc/systemd/system/dbert-api.service

sudo systemctl daemon-reload
sudo systemctl enable dbert-website.service
sudo systemctl enable dbert-portal.service
sudo systemctl enable dbert-api.service

echo "[*] Restarting application services..."
sudo systemctl restart dbert-website.service
sudo systemctl restart dbert-portal.service
sudo systemctl restart dbert-api.service
sleep 3

# ── 7. Configure Nginx & SSL Bootstrap ───────────────────────────────────────
echo "[*] Configuring Nginx reverse proxy..."

# Generate bootstrap self-signed SSL cert if Let's Encrypt certificates are not yet present
if [ ! -f "/etc/letsencrypt/live/dbert.in/fullchain.pem" ]; then
    echo "[!] No Let's Encrypt certificate found. Generating temporary bootstrap cert so Nginx passes syntax check..."
    sudo mkdir -p /etc/letsencrypt/live/dbert.in
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/letsencrypt/live/dbert.in/privkey.pem \
        -out /etc/letsencrypt/live/dbert.in/fullchain.pem \
        -subj "/CN=dbert.in" 2>/dev/null
fi

if [ -d "/etc/nginx/sites-available" ]; then
    sudo cp "$REPO_DIR/deploy/dbert-unified-nginx.conf" /etc/nginx/sites-available/dbert-unified.conf
    sudo ln -sf /etc/nginx/sites-available/dbert-unified.conf /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
else
    sudo cp "$REPO_DIR/deploy/dbert-unified-nginx.conf" /etc/nginx/conf.d/dbert-unified.conf
fi

sudo nginx -t
sudo systemctl reload nginx

# ── 8. Health Verification ───────────────────────────────────────────────────
echo "===================================================================="
echo "[*] Running local service health checks..."

WEB_HTTP=$(curl -sf -o /dev/null -w "%{http_code}" http://127.0.0.1:3001 || echo "000")
LMS_HTTP=$(curl -sf -o /dev/null -w "%{http_code}" http://127.0.0.1:5001/health || echo "000")
API_HTTP=$(curl -sf -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/health || echo "000")

echo "  Website  (:3001)        -> HTTP $WEB_HTTP"
echo "  DBERT LMS (:5001/health) -> HTTP $LMS_HTTP"
echo "  FastAPI  (:8000/health) -> HTTP $API_HTTP"

if [ "$WEB_HTTP" = "200" ] && [ "$LMS_HTTP" = "200" ] && [ "$API_HTTP" = "200" ]; then
    echo "===================================================================="
    echo " [+] FULL UNIFIED DEPLOYMENT SUCCESSFUL!"
    echo "     Main Website : https://dbert.in (Port 3001)"
    echo "     DBERT LMS    : https://lms.dbert.in (Port 5001)"
    echo "     FastAPI API  : https://api.dbert.in (Port 8000)"
    echo "===================================================================="
    echo "Next Step: Obtain production SSL certificates via Certbot:"
    echo "  sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in -d api.dbert.in -d dbert.online -d www.dbert.online -d internship.dbert.online"
    echo "===================================================================="
else
    echo "[!] Services started but one or more health checks did not return 200."
    echo "    Check logs via:"
    echo "      sudo journalctl -u dbert-website.service -n 50 --no-pager"
    echo "      sudo journalctl -u dbert-portal.service -n 50 --no-pager"
    echo "      sudo journalctl -u dbert-api.service -n 50 --no-pager"
fi
