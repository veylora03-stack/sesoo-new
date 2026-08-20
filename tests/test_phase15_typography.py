import os
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase15TypographyTests(TestCase):
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

    def test_fonts_css_exists_and_content(self):
        p = self.base_dir / 'static' / 'css' / 'fonts.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('Vazirmatn', c)
        self.assertIn('Lalezar', c)
        self.assertIn('font-display', c)

    def test_scale_css_exists_and_content(self):
        p = self.base_dir / 'static' / 'css' / 'master.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('html', c)
        self.assertIn('font-size', c)
        self.assertIn('.hero-title', c)
        self.assertIn('.container', c)

    def test_base_html_includes_fonts_and_scale(self):
        c = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')
        # fonts.css should be before premium.css
        self.assertIn('master.css', c)
        # scale.css should be included
        pass

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'class="hero"')
        self.assertContains(res, 'hero-title')
        self.assertContains(res, 'data-animate')

    def test_other_pages(self):
        for url in ['/services/web-design/', '/about-us/', '/contact/', '/styleguide/']:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")