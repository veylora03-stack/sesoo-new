#!/bin/bash
set -e

# Setup automated daily backups via host cron.
# Run this script once on the VPS after deployment.
#
# What it does:
#   Adds a cron job that runs backup every day at 2:00 AM

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CRON_LINE="0 2 * * * cd $PROJECT_DIR && docker compose run --rm backup >> backups/cron.log 2>&1"

echo "Setting up daily backup cron job..."
echo "Project dir: $PROJECT_DIR"
echo "Cron line: $CRON_LINE"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "docker compose run --rm backup"; then
    echo "Backup cron job already exists. Updating..."
    crontab -l 2>/dev/null | grep -v "docker compose run --rm backup" | { cat; echo "$CRON_LINE"; } | crontab -
else
    echo "Adding new backup cron job..."
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
fi

echo ""
echo "Cron job installed. Verify with: crontab -l"
echo "Backups will run daily at 2:00 AM."
echo "Logs: backups/cron.log"
