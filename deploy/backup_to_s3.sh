#!/bin/bash
# ==============================================================================
# DBERT LMS — Automated Daily PostgreSQL Database Backup to AWS S3
# ==============================================================================
set -euo pipefail

BACKUP_DIR="/var/www/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/dbert_lms_${TIMESTAMP}.sql.gz"
S3_BUCKET="${DBERT_BACKUP_S3_BUCKET:-dbert-db-backups}"

mkdir -p "$BACKUP_DIR"

echo "[$TIMESTAMP] Starting PostgreSQL database backup..."
sudo -u postgres pg_dump dbert_lms | gzip > "$BACKUP_FILE"
echo "[$TIMESTAMP] Backup created at $BACKUP_FILE ($(du -h "$BACKUP_FILE" | cut -f1))"

# If AWS CLI is configured and S3 bucket is accessible, upload to S3
if command -v aws &> /dev/null; then
    if aws s3 ls "s3://$S3_BUCKET" &> /dev/null; then
        echo "[$TIMESTAMP] Uploading backup to s3://$S3_BUCKET/daily/..."
        aws s3 cp "$BACKUP_FILE" "s3://$S3_BUCKET/daily/dbert_lms_${TIMESTAMP}.sql.gz"
        echo "[$TIMESTAMP] Successfully uploaded to S3."
    else
        echo "[$TIMESTAMP] AWS S3 bucket $S3_BUCKET not reachable or not yet created. Backup kept locally."
    fi
fi

# Retention: Remove local backups older than 14 days
find "$BACKUP_DIR" -type f -name "dbert_lms_*.sql.gz" -mtime +14 -delete
echo "[$TIMESTAMP] Local backup cleanup complete."
