#!/bin/bash
set -e

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups"
LOG_FILE="$BACKUP_DIR/backup.log"

# Load environment variables if .env exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

DB_USER=${POSTGRES_USER:-postgres}
DB_NAME=${POSTGRES_DB:-sesoo_db}

mkdir -p $BACKUP_DIR

echo "[$DATE] Starting backup..." >> $LOG_FILE

# Database backup
echo "[$DATE] Dumping database..." >> $LOG_FILE
if docker compose exec -T db pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/db_$DATE.sql; then
    echo "[$DATE] Database backup successful: db_$DATE.sql" >> $LOG_FILE
else
    echo "[$DATE] Database backup FAILED" >> $LOG_FILE
    exit 1
fi

# Media backup
echo "[$DATE] Archiving media folder..." >> $LOG_FILE
if tar -czf $BACKUP_DIR/media_$DATE.tar.gz media/; then
    echo "[$DATE] Media backup successful: media_$DATE.tar.gz" >> $LOG_FILE
else
    echo "[$DATE] Media backup FAILED" >> $LOG_FILE
    exit 1
fi

# Cleanup old backups (older than 30 days) - Retention Policy
echo "[$DATE] Cleaning up old backups (older than 30 days)..." >> $LOG_FILE
find $BACKUP_DIR/ -type f -mtime +30 -delete

echo "[$DATE] Backup completed successfully." >> $LOG_FILE
echo "Backup completed successfully. Check $LOG_FILE for details."