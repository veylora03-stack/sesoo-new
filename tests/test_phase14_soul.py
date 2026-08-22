import os
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase14SoulTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')
        try: call_command('load_site_content')
        except: pass
        self.base_dir = Path(settings.BASE_DIR)

    def test_premium_css(self):
        p = self.base_dir / 'static' / 'css' / 'master.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('--grad-hero', c)
        self.assertIn('.blob', c)
        self.assertIn('.hero', c)
        self.assertIn('.text-gradient', c)

    def test_premium_js(self):
        p = self.base_dir / 'static' / 'js' / 'premium.js'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('IntersectionObserver', c)
        self.assertIn('prefers-reduced-motion', c)

    def test_base_html(self):
        c = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')
        self.assertIn('master.css', c)
        self.assertIn('premium.js', c)

    def test_svgs(self):
        self.assertTrue((self.base_dir / 'static' / 'images' / 'hero-illustration.svg').exists())

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'class="hero"')
        self.assertContains(res, 'hero-title')
        self.assertContains(res, 'data-animate')
        self.assertContains(res, 'blob')
        self.assertContains(res, 'trust-bar')
        self.assertContains(res, 'چرا Sesoo')

    def test_other_pages(self):
        for url in ['/services/web-design/', '/about-us/', '/contact/', '/styleguide/']:
            self.assertEqual(self.client.get(url).status_code, 200)