import os
from django.test import TestCase
from django.conf import settings
from pathlib import Path

class Phase11DeployTests(TestCase):
    def setUp(self):
        self.base_dir = Path(settings.BASE_DIR)

    def test_dockerfile_exists_and_content(self):
        p = self.base_dir / 'Dockerfile'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('python:3.12-slim', c)
        self.assertIn('requirements/prod.txt', c)
        self.assertIn('deploy/entrypoint.sh', c)
        self.assertIn('EXPOSE 8000', c)

    def test_docker_compose_exists_and_content(self):
        p = self.base_dir / 'docker-compose.yml'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('postgres', c)
        self.assertIn('redis', c)
        self.assertIn('web', c)
        self.assertIn('caddy', c)
        self.assertIn('media_data', c)
        self.assertIn('media_data', c)
        self.assertIn('postgres_data', c)

    def test_dockerignore_exists_and_content(self):
        p = self.base_dir / '.dockerignore'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('.venv', c)
        self.assertIn('.env.production', c)
        self.assertIn('staticfiles/', c)

    def test_entrypoint_sh_exists_and_content(self):
        p = self.base_dir / 'deploy' / 'entrypoint.sh'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('manage.py migrate', c)
        self.assertIn('manage.py collectstatic', c)
        self.assertIn('gunicorn config.wsgi:application', c)
        self.assertNotIn('\r', c)

    def test_env_production_example_exists_and_content(self):
        p = self.base_dir / '.env.production.example'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('SECRET_KEY', c)
        self.assertIn('ALLOWED_HOSTS', c)
        self.assertIn('DB_ENGINE=postgresql', c)
        self.assertIn('DB_HOST=db', c)
        self.assertIn('REDIS_URL', c)

    def test_deploy_readme_exists(self):
        p = self.base_dir / 'deploy' / 'README.md'
        self.assertTrue(p.exists())

    def test_deploy_checklist_exists(self):
        p = self.base_dir / 'deploy' / 'DEPLOYMENT_CHECKLIST.md'
        self.assertTrue(p.exists())