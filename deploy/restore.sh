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

# Validate backup files exist and are non-empty
if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database backup file not found: $DB_FILE"
    exit 1
fi

DB_SIZE=$(wc -c < "$DB_FILE")
if [ "$DB_SIZE" -lt 100 ]; then
    echo "Error: Database backup appears empty or corrupt ($DB_SIZE bytes)"
    exit 1
fi

if [ -n "$MEDIA_FILE" ] && [ ! -f "$MEDIA_FILE" ]; then
    echo "Error: Media backup file not found: $MEDIA_FILE"
    exit 1
fi

echo ""
echo "WARNING: This will overwrite the current database and media!"
echo "Database: $DB_FILE ($DB_SIZE bytes)"
echo "Media: ${MEDIA_FILE:-none}"
echo ""
read -p "Are you sure? Type 'yes' to confirm: " CONFIRM
[ "$CONFIRM" != "yes" ] && echo "Aborted." && exit 0

# --- Restore database ---
echo ""
echo "Stopping web service to prevent writes during restore..."
docker compose stop web 2>/dev/null || true

echo "Restoring database..."
cat "$DB_FILE" | docker compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" -q
echo "Database restored."

# --- Restore media ---
if [ -n "$MEDIA_FILE" ] && [ -f "$MEDIA_FILE" ]; then
    echo ""
    echo "Restoring media to Docker volume..."
    TMPDIR=$(mktemp -d)
    tar -xzf "$MEDIA_FILE" -C "$TMPDIR"

    # Copy media into the web container's /app/media (which IS the volume)
    docker compose cp "$TMPDIR/." web:/app/media/
    rm -rf "$TMPDIR"
    echo "Media restored."
else
    echo ""
    echo "No media file to restore (skipped)"
fi

# --- Restart services ---
echo ""
echo "Starting web service..."
docker compose start web

echo ""
echo "Waiting for web healthcheck..."
sleep 5

# Verify health
HEALTH=$(curl -sf http://localhost/healthz/ 2>/dev/null || echo '{"status":"unreachable"}')
echo "Health: $HEALTH"

echo ""
echo "Restore completed successfully."
