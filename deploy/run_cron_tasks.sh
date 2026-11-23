#!/bin/bash
# ==============================================================================
# DBERT LMS — Automated Background Cron Jobs Runner
# ==============================================================================
set -euo pipefail

ENV_FILE="/var/www/dbert-website-lms/dbert-api-package/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "Environment file $ENV_FILE missing."
    exit 1
fi

CRON_SECRET=$(grep '^CRON_SECRET=' "$ENV_FILE" | cut -d '=' -f2- | tr -d '"' | tr -d "'")

# Call outbox processing (every 10 minutes)
curl -s -X POST "http://127.0.0.1:8000/api/v1/cron/process-outbox" \
  -H "X-Cron-Secret: $CRON_SECRET" > /dev/null || true

# Call clean tokens
curl -s -X POST "http://127.0.0.1:8000/api/v1/cron/clean-tokens" \
  -H "X-Cron-Secret: $CRON_SECRET" > /dev/null || true

# Call expire marketplace posts
curl -s -X POST "http://127.0.0.1:8000/api/v1/cron/expire-posts" \
  -H "X-Cron-Secret: $CRON_SECRET" > /dev/null || true

# Continuous Data Convergence: Sync balance submissions & verified certificates to PostgreSQL
/var/www/dbert-website-lms/apps/portal/.venv/bin/python /var/www/dbert-website-lms/scripts/sync_enrollments_to_postgres.py >> /var/log/dbert_sync.log 2>&1 || true
/var/www/dbert-website-lms/apps/portal/.venv/bin/python /var/www/dbert-website-lms/scripts/sync_verified_certificates_to_portal.py >> /var/log/dbert_sync.log 2>&1 || true
