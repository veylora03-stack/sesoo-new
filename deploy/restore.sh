#!/bin/bash
set -e

echo "=================================================="
echo "  Sesoo - Database & Media Restore"
echo "=================================================="
echo ""

# Load environment variables
if [ -f .env.production ]; then
    set -a
    source .env.production
    set +a
fi

DB_USER="${DB_USER:-sesoo_user}"
DB_NAME="${DB_NAME:-sesoo_db}"

# Auto-find latest backup files if no arguments
if [ -z "$1" ]; then
    echo "No backup files specified. Finding latest..."
    DB_FILE=$(ls -t backups/db_*.sql 2>/dev/null | head -1)
    MEDIA_FILE=$(ls -t backups/media_*.tar.gz 2>/dev/null | head -1)
    
    if [ -z "$DB_FILE" ]; then
        echo "Error: No database backups found in backups/"
        exit 1
    fi
    echo "Latest DB backup: $DB_FILE"
    [ -n "$MEDIA_FILE" ] && echo "Latest Media backup: $MEDIA_FILE"
else
    DB_FILE="$1"
    MEDIA_FILE="$2"
fi

echo ""
echo "WARNING: This will overwrite the current database and media!"
echo "Database: $DB_FILE"
echo "Media: ${MEDIA_FILE:-none}"
echo ""
read -p "Are you sure? Type 'yes' to confirm: " CONFIRM
[ "$CONFIRM" != "yes" ] && echo "Aborted." && exit 0

# Restore database using postgres image (has psql)
echo ""
echo "Restoring database..."
docker compose run --rm -e PGPASSWORD="${POSTGRES_PASSWORD}" \
    -e PGHOST=db -e PGPORT=5432 \
    postgres:16-alpine \
    sh -c "psql -U $DB_USER -d $DB_NAME" < "$DB_FILE"
echo "Database restored."

# Restore media to Docker volume
if [ -n "$MEDIA_FILE" ] && [ -f "$MEDIA_FILE" ]; then
    echo "Restoring media to Docker volume..."
    TMPDIR=$(mktemp -d)
    tar -xzf "$MEDIA_FILE" -C "$TMPDIR"
    
    # Use web container to write to media_data volume
    docker compose cp "$TMPDIR/." web:/app/media/
    rm -rf "$TMPDIR"
    echo "Media restored."
else
    echo "No media file to restore (skipped)"
fi

echo ""
echo "Restore completed. Restart web if needed: docker compose restart web"
