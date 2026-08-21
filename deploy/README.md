# Automated Backup System

This directory contains scripts to manage automated backups for the database and media files.

## Taking a Backup
To manually trigger a backup of the database and media folder:
```bash
./deploy/backup.sh
```
Backups will be saved in the `backups/` directory at the root of the project.
Logs are written to `backups/backup.log`.
Older backups (older than 30 days) are automatically cleaned up (Retention Policy).

## Restoring from Backup
To restore the database and media folder from existing backup files:
```bash
./deploy/restore.sh db_FILE.sql media_FILE.tar.gz
```
**WARNING:** This will overwrite your current database and media folder. You will be asked for confirmation before proceeding.

## Setting up Automated Daily Backups (Cron)
To schedule the backup script to run automatically every day at 2:00 AM:
```bash
./deploy/cron-setup.sh
```
This will add an idempotent cron job and configure `logrotate` to manage the backup logs.
## پاکسازی فایل‌های اضافی

برای حذف فایل‌های cache و اضافی:

```bash
./deploy/cleanup.sh
```

این اسکریپت حذف می‌کند:
- __pycache__/ و *.pyc
- *.log
- .DS_Store و Thumbs.db
- فایل‌های swap ادیتور

## توجه: nginx حذف شده

nginx دیگر استفاده نمی‌شود. به جای آن از Caddy استفاده می‌کنیم که SSL خودکار دارد.
