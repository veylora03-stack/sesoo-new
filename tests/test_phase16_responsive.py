import os
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase16ResponsiveTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')
        try: call_command('load_site_content')
        except: pass
        self.base_dir = Path(settings.BASE_DIR)

    def test_base_html_fonts_and_finalize(self):
        c = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')
        self.assertIn('fonts.googleapis.com', c)
        self.assertIn('Vazirmatn', c)
        self.assertIn('Lalezar', c)
        self.assertIn('finalize.css', c)

    def test_finalize_css_content(self):
        p = self.base_dir / 'static' / 'css' / 'finalize.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8').replace(' ', '')
        self.assertIn('@media(max-width:991px)', c)
        self.assertIn('@media(max-width:639px)', c)
        self.assertIn('font-family', c)
        self.assertIn('.site-nav', c)
        self.assertIn('overflow-x', c)

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'class="hero"')
        self.assertContains(res, 'data-animate')
        self.assertContains(res, 'menu-toggle')

    def test_other_pages(self):
        for url in ['/services/web-design/', '/about-us/', '/contact/', '/blog/', '/portfolio/', '/styleguide/']:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")