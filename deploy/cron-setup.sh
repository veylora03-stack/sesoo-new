#!/bin/bash
set -e

SCRIPT_DIR=$(pwd)/deploy
CRON_JOB="0 2 * * * $SCRIPT_DIR/backup.sh >> $SCRIPT_DIR/../backups/cron.log 2>&1"

# Check if cron job already exists (idempotent)
(crontab -l 2>/dev/null | grep -v "$SCRIPT_DIR/backup.sh"; echo "$CRON_JOB") | crontab -

echo "Cron job added successfully (Daily at 2 AM)."
crontab -l | grep backup.sh

# Setup logrotate for backup.log
LOGROTATE_CONF="/etc/logrotate.d/sesoo-backups"
sudo tee $LOGROTATE_CONF > /dev/null <<EOF
$(pwd)/backups/backup.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
}
EOF

echo "Logrotate configuration added to $LOGROTATE_CONF"