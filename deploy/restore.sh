#!/bin/bash
set -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <db_backup.sql> <media_backup.tar.gz>"
    exit 1
fi

DB_FILE=$1
MEDIA_FILE=$2
BACKUP_DIR="backups"

# Load environment variables if .env exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

DB_USER=${POSTGRES_USER:-postgres}
DB_NAME=${POSTGRES_DB:-sesoo_db}

echo "=================================================="
echo "WARNING: This will overwrite the current database and media folder!"
echo "Database file: $BACKUP_DIR/$DB_FILE"
echo "Media file: $BACKUP_DIR/$MEDIA_FILE"
echo "=================================================="
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore aborted."
    exit 0
fi

if [ ! -f "$BACKUP_DIR/$DB_FILE" ]; then
    echo "Error: Database backup file not found!"
    exit 1
fi

if [ ! -f "$BACKUP_DIR/$MEDIA_FILE" ]; then
    echo "Error: Media backup file not found!"
    exit 1
fi

echo "Restoring database..."
cat $BACKUP_DIR/$DB_FILE | docker compose exec -T db psql -U $DB_USER $DB_NAME
echo "Database restored."

echo "Restoring media..."
tar -xzf $BACKUP_DIR/$MEDIA_FILE
echo "Media restored."

echo "Restore completed successfully."