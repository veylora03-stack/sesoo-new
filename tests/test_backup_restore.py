"""
Tests for backup and restore scripts.
"""
import subprocess
from django.test import TestCase
from pathlib import Path
from django.conf import settings


class BackupScriptTests(TestCase):

    def setUp(self):
        self.base_dir = Path(settings.BASE_DIR)
        self.backup_sh = self.base_dir / "deploy" / "backup.sh"

    def test_backup_script_exists(self):
        self.assertTrue(self.backup_sh.exists())

    def test_backup_script_syntax(self):
        rel = self.backup_sh.relative_to(self.base_dir).as_posix()
        result = subprocess.run(
            ["bash", "-n", rel],
            capture_output=True, text=True, cwd=str(self.base_dir)
        )
        self.assertEqual(result.returncode, 0, f"Syntax error: {result.stderr}")

    def test_backup_uses_docker_compose_run(self):
        content = self.backup_sh.read_text(encoding="utf-8")
        self.assertIn("docker compose run --rm backup", content)

    def test_backup_compose_has_validation(self):
        dc = (self.base_dir / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn("DB_SIZE", dc)

    def test_backup_compose_has_retention(self):
        dc = (self.base_dir / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn("mtime +30", dc)

    def test_backup_compose_has_pgpassword(self):
        dc = (self.base_dir / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn("PGPASSWORD", dc)


class RestoreScriptTests(TestCase):

    def setUp(self):
        self.base_dir = Path(settings.BASE_DIR)
        self.restore_sh = self.base_dir / "deploy" / "restore.sh"
        self.rc = self.restore_sh.read_text(encoding="utf-8") if self.restore_sh.exists() else ""

    def test_restore_exists(self):
        self.assertTrue(self.restore_sh.exists())

    def test_restore_syntax(self):
        rel = self.restore_sh.relative_to(self.base_dir).as_posix()
        result = subprocess.run(
            ["bash", "-n", rel],
            capture_output=True, text=True, cwd=str(self.base_dir)
        )
        self.assertEqual(result.returncode, 0, f"Syntax error: {result.stderr}")

    def test_has_trap(self):
        self.assertIn("trap", self.rc)

    def test_stops_web(self):
        self.assertIn("docker compose stop web", self.rc)

    def test_starts_web(self):
        self.assertIn("docker compose start web", self.rc)

    def test_drops_db(self):
        self.assertIn("DROP DATABASE", self.rc)

    def test_creates_db(self):
        self.assertIn("CREATE DATABASE", self.rc)

    def test_terminates_conns(self):
        self.assertIn("pg_terminate_backend", self.rc)

    def test_uses_psql(self):
        self.assertIn("psql", self.rc)

    def test_health_check(self):
        self.assertIn("healthz", self.rc)

    def test_timestamp_validation(self):
        self.assertIn("DB_TS", self.rc)

    def test_user_confirm(self):
        self.assertIn("read -p", self.rc)

    def test_file_validation(self):
        self.assertIn("wc -c", self.rc)

    def test_tmpdir_cleanup(self):
        self.assertIn("mktemp -d", self.rc)

    def test_error_handling(self):
        self.assertIn("pipefail", self.rc)

    def test_uses_project_db_user(self):
        self.assertNotIn("-U postgres", self.rc)
        self.assertIn('-U "$DB_USER"', self.rc)

    def test_connects_to_maintenance_db(self):
        self.assertIn("-d postgres", self.rc)

    def test_load_dump_connects_to_target(self):
        self.assertIn('-d "$DB_NAME"', self.rc)

    def test_identifier_validation(self):
        self.assertIn("IDENT_RE", self.rc)

    def test_sql_dump_sanity_check(self):
        self.assertIn("CREATE TABLE", self.rc)

    def test_validation_before_db_touch(self):
        lines = self.rc.splitlines()
        v = next((i for i, l in enumerate(lines) if "wc -c" in l), -1)
        d = next((i for i, l in enumerate(lines) if "DROP DATABASE" in l), -1)
        self.assertGreater(v, -1)
        self.assertGreater(d, -1)
        self.assertLess(v, d, "Validation must happen before DROP")

    def test_restore_uses_env_password(self):
        self.assertIn("DB_PASSWORD", self.rc)

    def test_media_restore_path(self):
        self.assertIn("web:/app/media/", self.rc)


class CronSetupTests(TestCase):

    def setUp(self):
        self.base_dir = Path(settings.BASE_DIR)
        self.cron_sh = self.base_dir / "deploy" / "cron-setup.sh"

    def test_exists(self):
        self.assertTrue(self.cron_sh.exists())

    def test_syntax(self):
        rel = self.cron_sh.relative_to(self.base_dir).as_posix()
        result = subprocess.run(
            ["bash", "-n", rel],
            capture_output=True, text=True, cwd=str(self.base_dir)
        )
        self.assertEqual(result.returncode, 0)

    def test_idempotent(self):
        c = self.cron_sh.read_text(encoding="utf-8")
        self.assertIn("crontab -l", c)
        self.assertIn("grep", c)


class ScriptPermissionsTests(TestCase):

    def setUp(self):
        self.base_dir = Path(settings.BASE_DIR)
        self.scripts = [
            "deploy/backup.sh", "deploy/restore.sh", "deploy/entrypoint.sh",
            "deploy/cron-setup.sh", "deploy/cleanup.sh", "deploy/run-migrations.sh",
        ]

    def test_all_exist(self):
        for s in self.scripts:
            self.assertTrue((self.base_dir / s).exists())

    def test_all_executable(self):
        for s in self.scripts:
            r = subprocess.run(
                ["git", "ls-files", "--stage", s],
                capture_output=True, text=True, cwd=str(self.base_dir)
            )
            self.assertIn("100755", r.stdout, f"{s} not executable")


class UserConsistencyTests(TestCase):

    def setUp(self):
        self.base_dir = Path(settings.BASE_DIR)
        self.dc = (self.base_dir / "docker-compose.yml").read_text(encoding="utf-8")

    def test_postgres_user_matches_db_user(self):
        self.assertIn("POSTGRES_USER: sesoo_user", self.dc)
        self.assertIn("DB_USER: sesoo_user", self.dc)

    def test_postgres_db_matches_db_name(self):
        self.assertIn("POSTGRES_DB: sesoo_db", self.dc)
        self.assertIn("DB_NAME: sesoo_db", self.dc)

    def test_restore_defaults_match_compose(self):
        rc = (self.base_dir / "deploy" / "restore.sh").read_text(encoding="utf-8")
        self.assertIn('DB_USER:-sesoo_user', rc)
        self.assertIn('DB_NAME:-sesoo_db', rc)
