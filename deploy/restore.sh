#!/bin/bash
#
# Sesoo - Database & Media Restore
#
# Usage:
#   bash deploy/restore.sh                                    # Restore latest matched backup pair
#   bash deploy/restore.sh backups/db_FILE.sql                # Restore specific DB + latest media
#   bash deploy/restore.sh backups/db_FILE.sql backups/media_FILE.tar.gz  # Restore specific pair
#
# Safety:
#   - Trap ensures web is restarted on any failure
#   - User confirmation required before proceeding
#   - Backup file integrity checked before DB is touched
#   - DB identifiers validated (no SQL/shell injection possible)
#   - Passwords never logged, echoed, or written to temp files
#   - Timestamp pairing validated when auto-finding latest backups

set -euo pipefail

WORKDIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKDIR"

# --- Environment ---
if [ -f .env.production ]; then
    set -a
    source .env.production
    set +a
fi

DB_USER="${DB_USER:-sesoo_user}"
DB_NAME="${DB_NAME:-sesoo_db}"
DB_PASSWORD="${DB_PASSWORD:-}"

RESTORE_TMPDIR=""
WEB_STOPPED=0

# --- Validate DB identifiers ---
# Prevent SQL/shell injection via DB_NAME or DB_USER.
# PostgreSQL identifiers must match: [A-Za-z_][A-Za-z0-9_]*
IDENT_RE='^[A-Za-z_][A-Za-z0-9_]*$'
if ! echo "$DB_NAME" | grep -qE "$IDENT_RE"; then
    echo "Error: Invalid DB_NAME identifier: $DB_NAME"
    echo "  Must match: $IDENT_RE"
    exit 1
fi
if ! echo "$DB_USER" | grep -qE "$IDENT_RE"; then
    echo "Error: Invalid DB_USER identifier: $DB_USER"
    echo "  Must match: $IDENT_RE"
    exit 1
fi

# --- Cleanup on failure ---
cleanup() {
    local exit_code=$?
    if [ -n "$RESTORE_TMPDIR" ] && [ -d "$RESTORE_TMPDIR" ]; then
        rm -rf "$RESTORE_TMPDIR"
    fi
    if [ "$WEB_STOPPED" = "1" ]; then
        echo ""
        echo "Restarting web service..."
        docker compose start web >/dev/null 2>&1 || echo "Warning: web restart failed - check manually"
    fi
    exit "$exit_code"
}
trap cleanup EXIT INT TERM

# --- Header ---
echo "=================================================="
echo "  Sesoo - Database & Media Restore"
echo "=================================================="
echo ""

# --- Locate backup files ---
if [ -z "${1:-}" ]; then
    echo "No backup files specified. Finding latest matched pair..."
    DB_FILE=$(ls -t backups/db_*.sql 2>/dev/null | head -1)
    MEDIA_FILE=$(ls -t backups/media_*.tar.gz 2>/dev/null | head -1)

    if [ -z "$DB_FILE" ]; then
        echo "Error: No database backups found in backups/"
        exit 1
    fi

    DB_TS=$(echo "$DB_FILE" | sed -n 's/.*db_\([0-9]\{8\}_[0-9]\{6\}\)\.sql$/\1/p')
    if [ -n "$MEDIA_FILE" ] && [ -n "$DB_TS" ]; then
        MEDIA_TS=$(echo "$MEDIA_FILE" | sed -n 's/.*media_\([0-9]\{8\}_[0-9]\{6\}\)\.tar\.gz$/\1/p')
        if [ -n "$MEDIA_TS" ] && [ "$DB_TS" != "$MEDIA_TS" ]; then
            echo "WARNING: Timestamp mismatch!"
            echo "  DB:     $DB_FILE  (timestamp: $DB_TS)"
            echo "  Media:  $MEDIA_FILE  (timestamp: $MEDIA_TS)"
            echo ""
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

# --- Validate backup files BEFORE touching the database ---
if [ ! -f "$DB_FILE" ]; then
    echo "Error: Database backup not found: $DB_FILE"
    exit 1
fi

DB_SIZE=$(wc -c < "$DB_FILE" | tr -d ' ')
if [ "$DB_SIZE" -lt 100 ]; then
    echo "Error: Database backup appears empty or corrupt ($DB_SIZE bytes)"
    exit 1
fi

# Sanity-check: file must look like a SQL dump
if ! grep -qiE '(CREATE TABLE|CREATE INDEX|COPY |SET )' "$DB_FILE"; then
    echo "Error: Database backup does not look like a valid SQL dump"
    echo "  File contains no SQL statements. Aborting to protect the database."
    exit 1
fi

if [ -n "$MEDIA_FILE" ] && [ ! -f "$MEDIA_FILE" ]; then
    echo "Error: Media backup not found: $MEDIA_FILE"
    exit 1
fi

# --- Confirm ---
echo ""
echo "  WARNING: This will DESTROY and recreate the"
echo "  current database and overwrite media files."
echo ""
echo "  Database dump: $DB_FILE ($DB_SIZE bytes)"
echo "  Media archive: ${MEDIA_FILE:-none}"
echo ""
read -p "Type 'yes' to confirm restore: " CONFIRM
[ "$CONFIRM" != "yes" ] && echo "Aborted." && exit 0

# --- Step 1: Stop web (prevent writes) ---
echo ""
echo "[1/5] Stopping web service..."
docker compose stop web >/dev/null 2>&1 || true
WEB_STOPPED=1
echo "      Web stopped."

# --- Step 2: Clean database reset ---
echo ""
echo "[2/5] Resetting database..."

# Connect to the maintenance database (postgres) for DROP/CREATE operations.
# sesoo_user was created by the Docker postgres image via POSTGRES_USER,
# which grants it superuser privileges including DROP and CREATE DATABASE.
# We connect as DB_USER to the maintenance database, NOT the target database.
RESTORE_TMPDIR=$(mktemp -d)
SQL_FILE="$RESTORE_TMPDIR/maintenance.sql"
cat > "$SQL_FILE" << SQLEOF
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = '${DB_NAME}'
  AND pid <> pg_backend_pid();
DROP DATABASE IF EXISTS ${DB_NAME};
CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
SQLEOF

# PGPASSWORD is set only in the subprocess environment, never logged
PGPASSWORD="$DB_PASSWORD" docker compose exec -T db \
    psql -U "$DB_USER" -d postgres -q < "$SQL_FILE"

echo "      Database reset."

# --- Step 3: Load SQL dump ---
echo ""
echo "[3/5] Loading SQL dump..."
PGPASSWORD="$DB_PASSWORD" cat "$DB_FILE" | docker compose exec -T db \
    psql -U "$DB_USER" -d "$DB_NAME" -q

echo "      Database restored."

# --- Step 4: Restore media ---
echo ""
echo "[4/5] Restoring media..."
if [ -n "$MEDIA_FILE" ] && [ -f "$MEDIA_FILE" ]; then
    MEDIA_RESTORE_DIR="$RESTORE_TMPDIR/media"
    mkdir -p "$MEDIA_RESTORE_DIR"
    tar -xzf "$MEDIA_FILE" -C "$MEDIA_RESTORE_DIR"

    docker compose cp "$MEDIA_RESTORE_DIR/." web:/app/media/

    MEDIA_COUNT=$(find "$MEDIA_RESTORE_DIR" -type f | wc -l | tr -d ' ')
    echo "      Media restored ($MEDIA_COUNT files)."
else
    echo "      No media archive - skipped."
fi

rm -rf "$RESTORE_TMPDIR"
RESTORE_TMPDIR=""

# --- Step 5: Start web and health check ---
echo ""
echo "[5/5] Starting web service..."
docker compose start web >/dev/null 2>&1
WEB_STOPPED=0
echo "      Web started."

echo ""
echo "Waiting for web health check..."
HEALTHY=0
for i in $(seq 1 30); do
    sleep 2
    STATUS_CODE=$(curl -so /dev/null -w '%{http_code}' http://localhost/healthz/ 2>/dev/null || echo "000")
    if [ "$STATUS_CODE" = "200" ]; then
        HEALTHY=1
        break
    fi
    echo "      Attempt $i/30 - status: $STATUS_CODE"
done

if [ "$HEALTHY" = "1" ]; then
    echo ""
    echo "=================================================="
    echo "  Restore completed successfully"
    echo "=================================================="
    echo "  Database:  restored"
    echo "  Media:     restored"
    echo "  Health:    OK"
    echo "=================================================="
else
    echo ""
    echo "=================================================="
    echo "  Restore completed but health check failed"
    echo "=================================================="
    echo "  The web service started but did not respond"
    echo "  to /healthz/ within 60 seconds."
    echo ""
    echo "  Check logs: docker compose logs web --tail 50"
    echo "=================================================="
    exit 1
fi
