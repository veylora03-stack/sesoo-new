#!/bin/bash
#
# Sesoo — Database & Media Restore
#
# Usage:
#   bash deploy/restore.sh                                    # Restore latest matched backup pair
#   bash deploy/restore.sh backups/db_FILE.sql                # Restore specific DB + latest media
#   bash deploy/restore.sh backups/db_FILE.sql backups/media_FILE.tar.gz  # Restore specific pair
#
# What this does:
#   1. Stops the web service (prevents writes during restore)
#   2. Drops and recreates the database (guarantees clean restore, not append)
#   3. Loads the SQL dump into the fresh database
#   4. Restores media files into the Docker volume
#   5. Restarts web and verifies health via polling
#
# Safety:
#   - Trap ensures web is restarted on any failure
#   - User confirmation required before proceeding
#   - Backup file integrity checked before restore
#   - Timestamp pairing validated when auto-finding latest backups

set -euo pipefail

WORKDIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKDIR"

# ─── Environment ───────────────────────────────────────────────────────────────
if [ -f .env.production ]; then
    set -a
    source .env.production
    set +a
fi

DB_USER="${DB_USER:-sesoo_user}"
DB_NAME="${DB_NAME:-sesoo_db}"

RESTORE_TMPDIR=""
WEB_STOPPED=0

# ─── Cleanup on failure ────────────────────────────────────────────────────────
cleanup() {
    local exit_code=$?
    # Remove temp directory
    if [ -n "$RESTORE_TMPDIR" ] && [ -d "$RESTORE_TMPDIR" ]; then
        rm -rf "$RESTORE_TMPDIR"
    fi
    # Always restart web if it was stopped, regardless of success/failure
    if [ "$WEB_STOPPED" = "1" ]; then
        echo ""
        echo "Restarting web service..."
        docker compose start web >/dev/null 2>&1 || echo "Warning: web restart failed — check manually"
    fi
    exit "$exit_code"
}
trap cleanup EXIT INT TERM

# ─── Header ────────────────────────────────────────────────────────────────────
echo "=================================================="
echo "  Sesoo — Database & Media Restore"
echo "=================================================="
echo ""

# ─── Locate backup files ───────────────────────────────────────────────────────
if [ -z "${1:-}" ]; then
    echo "No backup files specified. Finding latest matched pair..."
    DB_FILE=$(ls -t backups/db_*.sql 2>/dev/null | head -1)
    MEDIA_FILE=$(ls -t backups/media_*.tar.gz 2>/dev/null | head -1)

    if [ -z "$DB_FILE" ]; then
        echo "Error: No database backups found in backups/"
        exit 1
    fi

    # Validate timestamp pairing
    DB_TS=$(echo "$DB_FILE" | sed -n 's/.*db_\([0-9]\{8\}_[0-9]\{6\}\)\.sql$/\1/p')
    if [ -n "$MEDIA_FILE" ] && [ -n "$DB_TS" ]; then
        MEDIA_TS=$(echo "$MEDIA_FILE" | sed -n 's/.*media_\([0-9]\{8\}_[0-9]\{6\}\)\.tar\.gz$/\1/p')
        if [ -n "$MEDIA_TS" ] && [ "$DB_TS" != "$MEDIA_TS" ]; then
            echo "WARNING: Timestamp mismatch!"
            echo "  DB:     $DB_FILE  (timestamp: $DB_TS)"
            echo "  Media:  $MEDIA_FILE  (timestamp: $MEDIA_TS)"
            echo ""
            echo "Restoring mismatched backups can produce inconsistent state."
            echo "To proceed, specify matching files explicitly:"
            echo "  bash deploy/restore.sh <db_file.sql> <media_file.tar.gz>"
            exit 1
        fi
    fi

    echo "DB backup:    $DB_FILE"
    [ -n "$MEDIA_FILE" ] && echo "Media backup: $MEDIA_FILE"
else
    DB_FILE="$1"
    MEDIA_FILE="${2:-}"
fi

# ─── Validate files ────────────────────────────────────────────────────────────
if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database backup not found: $DB_FILE"
    exit 1
fi

DB_SIZE=$(wc -c < "$DB_FILE" | tr -d ' ')
if [ "$DB_SIZE" -lt 100 ]; then
    echo "Error: Database backup appears empty or corrupt ($DB_SIZE bytes)"
    exit 1
fi

if [ -n "$MEDIA_FILE" ] && [ ! -f "$MEDIA_FILE" ]; then
    echo "Error: Media backup not found: $MEDIA_FILE"
    exit 1
fi

# ─── Confirm ───────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║  WARNING: This will DESTROY and recreate the    ║"
echo "║  current database and overwrite media files.     ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "  Database dump: $DB_FILE ($DB_SIZE bytes)"
echo "  Media archive: ${MEDIA_FILE:-none}"
echo ""
read -p "Type 'yes' to confirm restore: " CONFIRM
[ "$CONFIRM" != "yes" ] && echo "Aborted." && exit 0

# ─── Step 1: Stop web (prevent writes) ─────────────────────────────────────────
echo ""
echo "[1/5] Stopping web service..."
docker compose stop web >/dev/null 2>&1 || true
WEB_STOPPED=1
echo "      Web stopped."

# ─── Step 2: Clean database restore ────────────────────────────────────────────
echo ""
echo "[2/5] Restoring database (drop + recreate + load)..."

# Create a temporary SQL script for the operations
RESTORE_TMPDIR=$(mktemp -d)
SQL_FILE="$RESTORE_TMPDIR/clean_restore.sql"
cat > "$SQL_FILE" << SQLEOF
-- Terminate all active connections to the target database
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = '${DB_NAME}'
  AND pid <> pg_backend_pid();

-- Drop and recreate the database for a clean restore
DROP DATABASE IF EXISTS ${DB_NAME};
CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
SQLEOF

# Execute SQL as postgres superuser via the db container
docker compose exec -T db psql -U postgres -q < "$SQL_FILE"

# Load the dump into the fresh database
cat "$DB_FILE" | docker compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" -q

echo "      Database restored ($(numfmt --to=iec "$DB_SIZE" 2>/dev/null || echo "${DB_SIZE} bytes"))."

# ─── Step 3: Restore media ────────────────────────────────────────────────────
echo ""
echo "[3/5] Restoring media..."
if [ -n "$MEDIA_FILE" ] && [ -f "$MEDIA_FILE" ]; then
    MEDIA_RESTORE_DIR="$RESTORE_TMPDIR/media"
    mkdir -p "$MEDIA_RESTORE_DIR"
    tar -xzf "$MEDIA_FILE" -C "$MEDIA_RESTORE_DIR"

    # Copy extracted media into the web container's /app/media volume
    docker compose cp "$MEDIA_RESTORE_DIR/." web:/app/media/

    MEDIA_COUNT=$(find "$MEDIA_RESTORE_DIR" -type f | wc -l | tr -d ' ')
    echo "      Media restored ($MEDIA_COUNT files)."
else
    echo "      No media archive — skipped."
fi

# Clean up temp files early (trap will handle if we fail before this)
rm -rf "$RESTORE_TMPDIR"
RESTORE_TMPDIR=""

# ─── Step 4: Start web ────────────────────────────────────────────────────────
echo ""
echo "[4/5] Starting web service..."
docker compose start web >/dev/null 2>&1
WEB_STOPPED=0
echo "      Web started."

# ─── Step 5: Health check with polling ────────────────────────────────────────
echo ""
echo "[5/5] Waiting for web health check..."
HEALTHY=0
for i in $(seq 1 30); do
    sleep 2
    STATUS_CODE=$(curl -so /dev/null -w '%{http_code}' http://localhost/healthz/ 2>/dev/null || echo "000")
    if [ "$STATUS_CODE" = "200" ]; then
        HEALTHY=1
        break
    fi
    echo "      Attempt $i/30 — status: $STATUS_CODE"
done

if [ "$HEALTHY" = "1" ]; then
    echo ""
    echo "=================================================="
    echo "  ✅ Restore completed successfully"
    echo "=================================================="
    echo "  Database:  restored"
    echo "  Media:     restored"
    echo "  Health:    OK"
    echo "=================================================="
else
    echo ""
    echo "=================================================="
    echo "  ⚠️  Restore completed but health check failed"
    echo "=================================================="
    echo "  The web service started but did not respond"
    echo "  to /healthz/ within 60 seconds."
    echo ""
    echo "  Check logs: docker compose logs web --tail 50"
    echo "=================================================="
    exit 1
fi
