# Backup & Restore

## Backup

### Manual backup
```bash
bash deploy/backup.sh
```

### Automated daily backup (via host cron)
```bash
bash deploy/cron-setup.sh   # Run once after deployment
```

Adds a cron job that runs daily at 2:00 AM:
```
0 2 * * * cd /path/to/project && docker compose run --rm backup >> backups/cron.log 2>&1
```

### What backup does
- Uses `postgres:16-alpine` image (has `pg_dump` built-in)
- Dumps database to `backups/db_YYYYMMDD_HHMMSS.sql`
- Archives media volume to `backups/media_YYYYMMDD_HHMMSS.tar.gz`
- Validates dump is non-empty (rejects corrupt dumps)
- Cleans up backups older than 30 days

### Backup output
```
backups/
  db_20260822_145000.sql        # PostgreSQL dump
  media_20260822_145000.tar.gz  # Media volume archive
  cron.log                      # Cron execution log
```

## Restore

### Restore latest matched backup pair
```bash
bash deploy/restore.sh
```

### Restore specific files
```bash
bash deploy/restore.sh backups/db_FILE.sql backups/media_FILE.tar.gz
```

### What restore does
1. **Validates** backup files exist and are non-empty
2. **Checks timestamp pairing** — DB and media must share the same timestamp
3. **Asks for confirmation** — you must type `yes`
4. **Stops web** — prevents writes during restore
5. **Drops and recreates database** — guarantees clean restore (not append)
6. **Terminates active connections** — safely disconnects all clients
7. **Loads the SQL dump** — restores all data
8. **Restores media** — copies files into Docker volume
9. **Restarts web** — always restarts, even on failure (via trap)
10. **Polls health check** — waits up to 60 seconds for `/healthz/`

### Safety features
- **Trap handler**: web service is always restarted, even if restore fails mid-way
- **Timestamp validation**: prevents restoring mismatched DB/media pairs
- **File validation**: rejects empty or corrupt backup files
- **Confirmation prompt**: requires explicit `yes` before proceeding
- **Health polling**: waits for real readiness, not just a fixed delay

### ⚠️ Warning
Restore **destroys** the current database and overwrites media files. There is no undo.

## Architecture
```
Host cron (2AM daily)
    ↓
docker compose run --rm backup
    ↓
postgres:16-alpine container
    ├── pg_dump → backups/db_YYYYMMDD.sql
    └── tar media volume → backups/media_YYYYMMDD.tar.gz
```

## Scripts
| Script | Purpose |
|--------|---------|
| `backup.sh` | Wrapper to run backup service |
| `restore.sh` | Interactive database + media restore |
| `cron-setup.sh` | Install daily backup cron job |
| `cleanup.sh` | Remove cache and temp files |
| `run-migrations.sh` | Run migrations manually |
