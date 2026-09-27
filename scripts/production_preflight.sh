#!/bin/bash
# Production pre-flight check for DBERT LMS Portal.
# Run on EC2 BEFORE restarting the service after a deployment.
# Exit code 0 = all clear; non-zero = do not start service.
set -euo pipefail

PORTAL_DIR="/var/www/dbert-website-lms/apps/portal"
ERRORS=0
WARNINGS=0

check() {
    local label="$1"; local result="$2"; local level="${3:-error}"
    if [ "$result" != "ok" ]; then
        echo "[$( echo $level | tr a-z A-Z )] $label — $result"
        [ "$level" = "error" ] && ERRORS=$((ERRORS+1)) || WARNINGS=$((WARNINGS+1))
    else
        echo "[OK]  $label"
    fi
}

echo "==== DBERT Portal Production Preflight ===="
echo "Date: $(date)"
echo ""

# Git state
cd /var/www/dbert-website-lms
SHA=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
echo "Git SHA   : $SHA"
echo "Git branch: $BRANCH"
[ "$BRANCH" = "main" ] || echo "[WARN] Not on main branch: $BRANCH"
echo ""

# Python
PY=$(python3 --version 2>&1 || echo "missing")
check "Python 3" "$(echo $PY | grep -q 'Python 3' && echo ok || echo "Not found: $PY")"

# venv
check ".venv exists" "$([ -d $PORTAL_DIR/.venv ] && echo ok || echo 'Virtual env missing')"

# Gunicorn
check "gunicorn installed" "$(source $PORTAL_DIR/.venv/bin/activate 2>/dev/null; which gunicorn > /dev/null 2>&1 && echo ok || echo 'not installed')"

# psycopg2
check "psycopg2 installed" "$(source $PORTAL_DIR/.venv/bin/activate 2>/dev/null; python3 -c 'import psycopg2' 2>/dev/null && echo ok || echo 'not installed')"

# .env
check ".env exists" "$([ -f $PORTAL_DIR/.env ] && echo ok || echo 'Missing .env file')"

if [ -f "$PORTAL_DIR/.env" ]; then
    source "$PORTAL_DIR/.env" 2>/dev/null || true

    check "REQUIRE_POSTGRES=true" "$([ '${REQUIRE_POSTGRES:-}' = 'true' ] && echo ok || echo "REQUIRE_POSTGRES=${REQUIRE_POSTGRES:-unset}")"
    check "DATABASE_URL is postgres" "$(echo '${DATABASE_URL:-}' | grep -qE '^postgres(ql)?://' && echo ok || echo 'DATABASE_URL missing or not postgres')"
    check "POSTGRES_SCHEMA set" "$([ -n '${POSTGRES_SCHEMA:-}' ] && echo ok || echo 'POSTGRES_SCHEMA not set')"
    check "FLASK_SECRET_KEY set" "$([ -n '${FLASK_SECRET_KEY:-}' ] && echo ok || echo 'FLASK_SECRET_KEY not set')"
    check "FLASK_DEBUG=false" "$([ '${FLASK_DEBUG:-}' != 'true' ] && echo ok || echo 'FLASK_DEBUG is true in production!')"

    # Check no hardcoded default key
    if echo '${FLASK_SECRET_KEY:-}' | grep -qi 'digitalblinc\|default\|changeme'; then
        echo "[ERROR] FLASK_SECRET_KEY looks like a default value"
        ERRORS=$((ERRORS+1))
    fi
fi

# No SQLite file in runtime path
check "No internship.db in portal dir" "$([ ! -f $PORTAL_DIR/internship.db ] && echo ok || echo 'internship.db exists — check REQUIRE_POSTGRES')"

# Systemd unit
check "systemd unit exists" "$([ -f /etc/systemd/system/dbert-portal.service ] && echo ok || echo 'Service file not installed')"

# Nginx
check "nginx config installed" "$([ -f /etc/nginx/conf.d/dbert-portal.conf ] && echo ok || echo 'Nginx config not installed')"
check "nginx config valid" "$(sudo nginx -t 2>&1 | grep -q 'successful' && echo ok || echo 'nginx -t failed')"

echo ""
echo "==== Summary: $ERRORS error(s), $WARNINGS warning(s) ===="
if [ $ERRORS -gt 0 ]; then
    echo "[FAIL] Preflight failed. Fix errors before deploying."
    exit 1
else
    echo "[PASS] Preflight passed."
    exit 0
fi
