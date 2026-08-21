from django.test import TestCase
from pathlib import Path
from django.conf import settings

class Phase28DeployTests(TestCase):
    def setUp(self):
        self.base_dir = Path(settings.BASE_DIR)

    def test_docker_compose_caddy(self):
        dc = self.base_dir / 'docker-compose.yml'
        self.assertTrue(dc.exists())
        c = dc.read_text(encoding='utf-8')
        self.assertIn('caddy', c)
        self.assertIn('postgres', c)
        self.assertIn('web', c)
        self.assertNotIn('image: nginx', c)
        
        lines = c.split('\n')
        in_services = False
        for line in lines:
            if line.startswith('services:'):
                in_services = True
            elif line.startswith('volumes:'):
                in_services = False
            if in_services and line.strip().startswith('nginx:'):
                self.fail("nginx service still exists in docker-compose.yml")

    def test_caddyfile(self):
        cf = self.base_dir / 'deploy' / 'Caddyfile'
        self.assertTrue(cf.exists())
        c = cf.read_text(encoding='utf-8')
        self.assertIn('reverse_proxy web:8000', c)

    def test_vps_setup(self):
        vs = self.base_dir / 'deploy' / 'vps-setup.sh'
        self.assertTrue(vs.exists())
        c = vs.read_text(encoding='utf-8')
        self.assertIn('docker-compose-plugin', c)

    def test_env_production_example(self):
        env = self.base_dir / '.env.production.example'
        self.assertTrue(env.exists())
        c = env.read_text(encoding='utf-8')
        self.assertIn('SITE_DOMAIN', c)

    def test_domain_ssl_gsc_doc(self):
        doc = self.base_dir / 'docs' / 'DOMAIN_SSL_GSC.md'
        self.assertTrue(doc.exists())
        c = doc.read_text(encoding='utf-8')
        self.assertIn('سرچ کنسول', c)
        self.assertIn('sitemap.xml', c)