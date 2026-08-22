#!/bin/bash
set -e

# Backup script for Sesoo
# This script runs the backup Docker Compose service.
#
# Usage:
#   bash deploy/backup.sh              # Run backup now
#
# For automated daily backups, add to host crontab:
#   0 2 * * * cd /path/to/project && docker compose run --rm backup >> backups/cron.log 2>&1
#
# The backup service:
#   - Uses postgres:16-alpine image (has pg_dump built-in)
#   - Connects to PostgreSQL via Docker network
#   - Dumps database to backups/db_YYYYMMDD_HHMMSS.sql
#   - Archives media from Docker volume to backups/media_YYYYMMDD_HHMMSS.tar.gz
#   - Cleans up backups older than 30 days

echo "[$(date)] Starting Sesoo backup..."
mkdir -p backups

docker compose run --rm backup

echo "[$(date)] Backup completed."
echo "Files in backups/:"
ls -lh backups/ 2>/dev/null | tail -5
