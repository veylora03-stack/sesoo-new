#!/bin/bash
set -e

echo "=================================================="
echo "  Sesoo - Database & Media Restore"
echo "=================================================="
echo ""

# Load environment variables from .env.production
if [ -f .env.production ]; then
    set -a
    source .env.production
    set +a
fi

DB_USER="${DB_USER:-sesoo_user}"
DB_NAME="${DB_NAME:-sesoo_db}"

# Find latest backup files if no arguments given
if [ -z "$1" ]; then
    echo "No backup files specified. Finding latest..."
    DB_FILE=$(ls -t backups/db_*.sql 2>/dev/null | head -1)
    MEDIA_FILE=$(ls -t backups/media_*.tar.gz 2>/dev/null | head -1)
    
    if [ -z "$DB_FILE" ]; then
        echo "Error: No database backups found in backups/"
        exit 1
    fi
    echo "Latest DB backup: $DB_FILE"
    if [ -n "$MEDIA_FILE" ]; then
        echo "Latest Media backup: $MEDIA_FILE"
    else
        echo "No media backups found (will skip media restore)"
    fi
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

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore aborted."
    exit 0
fi

# Stop web service to prevent writes during restore
echo ""
echo "Stopping web service..."
docker compose stop web 2>/dev/null || true

# Restore database
echo "Restoring database..."
if [ -f "$DB_FILE" ]; then
    docker compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" < "$DB_FILE"
    echo "Database restored from $DB_FILE"
else
    echo "Error: Database file $DB_FILE not found!"
    docker compose start web 2>/dev/null || true
    exit 1
fi

# Restore media to Docker volume
if [ -n "$MEDIA_FILE" ] && [ -f "$MEDIA_FILE" ]; then
    echo "Restoring media to Docker volume..."
    # Create temp dir, extract, then copy into volume
    TMPDIR=$(mktemp -d)
    tar -xzf "$MEDIA_FILE" -C "$TMPDIR"
    
    # Copy into the container which has the volume mounted
    docker compose cp "$TMPDIR/." web:/app/media/
    
    rm -rf "$TMPDIR"
    echo "Media restored from $MEDIA_FILE"
else
    echo "No media file to restore (skipped)"
fi

# Restart web service
echo "Starting web service..."
docker compose start web

echo ""
echo "Restore completed successfully."
echo "Verify with: docker compose ps && docker compose logs web --tail=20"
