#!/bin/bash
# ====================================================================
# DBERT Portal — Production EC2 Deployment Script
# Source of truth: GitHub main branch (NOT FileZilla)
# ====================================================================
set -Eeuo pipefail

REPO_DIR="/var/www/dbert-website-lms"
PORTAL_DIR="$REPO_DIR/apps/portal"
BACKUP_DIR="/var/www/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "===================================================================="
echo " DBERT Portal EC2 Deployment — $(date)"
echo "===================================================================="

# ── 0. Require that the production .env exists ──────────────────────────
if [ ! -f "$PORTAL_DIR/.env" ]; then
    echo "[FATAL] $PORTAL_DIR/.env not found. Create it with real secrets before deploying."
    exit 1
fi

# Source .env to read DATABASE_URL for pg_dump
set +u
source "$PORTAL_DIR/.env" 2>/dev/null || true
set -u

# ── 1. Backup current deployed SHA ──────────────────────────────────────
mkdir -p "$BACKUP_DIR"
cd "$REPO_DIR"
git rev-parse HEAD > "$BACKUP_DIR/dbert_previous_sha_${TIMESTAMP}.txt" 2>/dev/null || echo "unknown" > "$BACKUP_DIR/dbert_previous_sha_${TIMESTAMP}.txt"
echo "[*] Previous SHA saved to $BACKUP_DIR/dbert_previous_sha_${TIMESTAMP}.txt"

# ── 2. Backup PostgreSQL database ───────────────────────────────────────
if [ -n "${DATABASE_URL:-}" ]; then
    echo "[*] Backing up PostgreSQL database..."
    pg_dump "$DATABASE_URL" > "$BACKUP_DIR/dbert_pre_deploy_${TIMESTAMP}.sql"
    echo "[*] DB backup: $BACKUP_DIR/dbert_pre_deploy_${TIMESTAMP}.sql"
else
    echo "[WARNING] DATABASE_URL not set — skipping DB backup"
fi

# ── 3. Pull from GitHub ──────────────────────────────────────────────────
echo "[*] Pulling latest code from GitHub main..."
git fetch origin
git checkout main
git reset --hard origin/main
# Only remove untracked files NOT inside the portal dir (preserve .env, uploads, .venv)
git clean -fd --exclude=apps/portal/.env --exclude=apps/portal/.venv --exclude=apps/portal/uploads

DEPLOYED_SHA=$(git rev-parse HEAD)
echo "[*] Deployed SHA: $DEPLOYED_SHA"

# ── 4. Install Python dependencies ──────────────────────────────────────
echo "[*] Installing Python dependencies..."
cd "$PORTAL_DIR"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install psycopg2-binary -q
python -m compileall . -q

# ── 5. Install systemd + nginx configs ─────────────────────────────────
echo "[*] Installing systemd service..."
sudo cp "$REPO_DIR/deploy/dbert-portal.service" /etc/systemd/system/
sudo systemctl daemon-reload

echo "[*] Installing nginx config..."
sudo cp "$REPO_DIR/deploy/dbert-portal-nginx.conf" /etc/nginx/conf.d/dbert-portal.conf
sudo nginx -t

# ── 6. Restart portal service ───────────────────────────────────────────
echo "[*] Restarting dbert-portal.service..."
sudo systemctl restart dbert-portal.service
sleep 5
sudo systemctl status dbert-portal.service --no-pager

# ── 7. Health checks ────────────────────────────────────────────────────
echo "[*] Running health checks..."
HEALTH=$(curl -sf -o /dev/null -w "%{http_code}" http://127.0.0.1:5001/health || echo "000")
READY=$(curl -sf -o /dev/null -w "%{http_code}" http://127.0.0.1:5001/ready || echo "000")

echo "  /health → HTTP $HEALTH"
echo "  /ready  → HTTP $READY"

sudo systemctl reload nginx

if [ "$HEALTH" = "200" ] && [ "$READY" = "200" ]; then
    echo "===================================================================="
    echo " [+] DEPLOYMENT SUCCESS"
    echo "     SHA: $DEPLOYED_SHA"
    echo "     Gunicorn: 127.0.0.1:5001"
    echo "     DB backup: $BACKUP_DIR/dbert_pre_deploy_${TIMESTAMP}.sql"
    echo "===================================================================="
else
    echo "[FATAL] Health check failed. HEALTH=$HEALTH READY=$READY"
    echo "        Check: sudo journalctl -u dbert-portal.service -n 100 --no-pager"
    echo "        Rollback SHA: $(cat $BACKUP_DIR/dbert_previous_sha_${TIMESTAMP}.txt)"
    exit 1
fi
