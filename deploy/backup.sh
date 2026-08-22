#!/bin/bash
set -e

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"
LOG_FILE="$BACKUP_DIR/backup.log"

# Load environment variables from .env.production
if [ -f .env.production ]; then
    set -a
    source .env.production
    set +a
fi

DB_USER="${DB_USER:-sesoo_user}"
DB_NAME="${DB_NAME:-sesoo_db}"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting backup..." | tee -a "$LOG_FILE"

# Database backup
echo "[$(date)] Dumping database..." | tee -a "$LOG_FILE"
if docker compose exec -T db pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_DIR/db_$DATE.sql"; then
    echo "[$(date)] Database backup: db_$DATE.sql ($(wc -c < "$BACKUP_DIR/db_$DATE.sql") bytes)" | tee -a "$LOG_FILE"
else
    echo "[$(date)] ERROR: Database backup FAILED" | tee -a "$LOG_FILE"
    exit 1
fi

# Media backup (copy from Docker volume via container)
echo "[$(date)] Backing up media..." | tee -a "$LOG_FILE"
# Create a temporary container to read the volume
if docker run --rm -v sesoo-web-new_media_data:/data:ro -v "$(pwd)/$BACKUP_DIR":/backup alpine \
    tar -czf "/backup/media_$DATE.tar.gz" -C /data . 2>/dev/null; then
    echo "[$(date)] Media backup: media_$DATE.tar.gz ($(wc -c < "$BACKUP_DIR/media_$DATE.tar.gz") bytes)" | tee -a "$LOG_FILE"
else
    echo "[$(date)] WARNING: Media volume backup failed, trying container cp..." | tee -a "$LOG_FILE"
    if docker compose cp web:/app/media/. - 2>/dev/null | tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" -C - .; then
        echo "[$(date)] Media backup (fallback): media_$DATE.tar.gz" | tee -a "$LOG_FILE"
    else
        echo "[$(date)] WARNING: Media backup failed entirely" | tee -a "$LOG_FILE"
        echo "[] > /dev/null" > "$BACKUP_DIR/media_$DATE.tar.gz.empty"
    fi
fi

# Cleanup old backups (older than 30 days)
echo "[$(date)] Cleaning up backups older than 30 days..." | tee -a "$LOG_FILE"
find "$BACKUP_DIR/" -type f -mtime +30 -delete 2>/dev/null || true

# Summary
echo "[$(date)] Backup completed successfully." | tee -a "$LOG_FILE"
echo "Files:"
ls -lh "$BACKUP_DIR/"*_$DATE* 2>/dev/null | tee -a "$LOG_FILE"
