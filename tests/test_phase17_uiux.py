import os
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase17UIUXTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')
        try: call_command('load_site_content')
        except: pass
        self.base_dir = Path(settings.BASE_DIR)

    def test_master_css_exists_and_content(self):
        p = self.base_dir / 'static' / 'css' / 'master.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('--c-primary', c)
        self.assertIn('.hero', c)
        self.assertIn('@media', c)

    def test_base_html_only_master(self):
        c = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')
        self.assertIn('master.css', c)
        self.assertNotIn('premium.css', c)
        self.assertNotIn('polish.css', c)
        self.assertNotIn('scale.css', c)

    def test_home_html_structure(self):
        c = (self.base_dir / 'templates' / 'pages' / 'home.html').read_text(encoding='utf-8')
        self.assertIn('hero-chips', c)

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'hero-title')
        self.assertContains(res, 'trust-bar')
        self.assertContains(res, 'hero-chips')

    def test_other_pages(self):
        for url in ['/services/web-design/', '/about-us/', '/contact/', '/blog/', '/portfolio/', '/styleguide/']:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")