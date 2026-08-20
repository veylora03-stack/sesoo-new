import re
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase19CompleteTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')
        try: call_command('load_site_content')
        except: pass
        self.base_dir = Path(settings.BASE_DIR)

    def test_home_html_structure(self):
        c = (self.base_dir / 'templates' / 'pages' / 'home.html').read_text(encoding='utf-8')
        self.assertIn('hero-chips', c)
        self.assertIn('cta-form', c)
        self.assertIn('persian-pattern', c)
        self.assertIn('parallax', c)
        wrapper_match = re.search(r'<div class="hero-media-wrapper">(.*?)</div>', c, re.DOTALL)
        if wrapper_match:
            self.assertNotIn('hero-chip', wrapper_match.group(1))

    def test_master_css_phase19(self):
        p = self.base_dir / 'static' / 'css' / 'master.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('persian-pattern', c)
        self.assertIn('arabesque-pattern', c)
        self.assertIn('cta-form', c)
        self.assertIn('loading-spinner', c)
        self.assertIn('parallax', c)

    def test_home_page_phase19(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'cta-form')
        self.assertContains(res, 'persian-pattern')
        self.assertContains(res, 'hero-chips')

    def test_other_pages_phase19(self):
        for url in ['/services/web-design/', '/about-us/', '/blog/', '/portfolio/', '/styleguide/']:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")