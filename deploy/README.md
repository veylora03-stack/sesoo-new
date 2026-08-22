# Automated Backup System

This directory contains scripts to manage automated backups for the database and media files.

## Taking a Backup

To manually trigger a backup of the database and media folder:

```bash
bash deploy/backup.sh
```

Backups will be saved in the `backups/` directory at the root of the project.

- Database backups: `backups/db_YYYYMMDD_HHMMSS.sql`
- Media backups: `backups/media_YYYYMMDD_HHMMSS.tar.gz`

Older backups (older than 30 days) are automatically cleaned up (Retention Policy).

## Restoring from Backup

To restore the **latest** backup (interactive — asks for confirmation):

```bash
bash deploy/restore.sh
```

To restore specific backup files:

```bash
bash deploy/restore.sh backups/db_20260822_020000.sql backups/media_20260822_020000.tar.gz
```

**WARNING:** This will overwrite the current database and media folder. You will be asked for confirmation before proceeding.

The restore process:
1. Stops the web service to prevent writes during restore
2. Restores the database using `psql`
3. Restores media files to the Docker volume
4. Restarts the web service and verifies health

## Setting up Automated Daily Backups (Cron)

To schedule the backup script to run automatically every day at 2:00 AM:

```bash
bash deploy/cron-setup.sh
```

This adds a cron job: `0 2 * * * cd /path/to/project && docker compose run --rm backup`

### Architecture

```
Host cron (2AM daily)
    ↓
docker compose run --rm backup
    ↓
postgres:16-alpine container
    ├── pg_dump → backups/db_YYYYMMDD.sql
    └── tar media volume → backups/media_YYYYMMDD.tar.gz
```

- Backup uses the official `postgres:16-alpine` image (includes `pg_dump`)
- Media is backed up directly from the Docker volume
- No Docker-in-Docker — host cron runs the backup service

## Cleanup

To remove unnecessary cache and temporary files:

```bash
bash deploy/cleanup.sh
```

This removes:
- `__pycache__/` and `*.pyc`
- `*.log`
- `.DS_Store` and `Thumbs.db`
- Editor swap files
