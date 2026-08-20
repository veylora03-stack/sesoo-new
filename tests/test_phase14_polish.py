import os
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase14PolishTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')
        try:
            call_command('load_site_content')
        except Exception:
            pass
        self.base_dir = Path(settings.BASE_DIR)

    def test_polish_css_exists_and_content(self):
        p = self.base_dir / 'static' / 'css' / 'polish.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('overflow-x', c)
        self.assertIn('z-index', c)
        self.assertIn('prefers-reduced-motion', c)
        self.assertIn('.scroll-progress', c)
        self.assertIn('.back-to-top', c)
        self.assertIn('.particle', c)

    def test_base_html_includes_polish(self):
        c = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')
        self.assertIn('polish.css', c)
        self.assertIn('scroll-progress', c)
        self.assertIn('back-to-top', c)

    def test_home_page_polish(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'class="hero"')
        self.assertContains(res, 'data-animate')
        self.assertContains(res, 'blob')
        self.assertContains(res, 'trust-bar')
        self.assertContains(res, 'scroll-progress')
        self.assertContains(res, 'back-to-top')

    def test_other_pages(self):
        for url in ['/services/web-design/', '/about-us/', '/contact/', '/styleguide/']:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")