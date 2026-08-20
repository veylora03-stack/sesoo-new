import re
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase21HotfixTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')
        try: call_command('load_site_content')
        except: pass
        self.base_dir = Path(settings.BASE_DIR)

    def test_home_html_no_marquee(self):
        c = (self.base_dir / 'templates' / 'pages' / 'home.html').read_text(encoding='utf-8')
        self.assertNotIn('marquee-strip', c)

    def test_home_html_chips(self):
        c = (self.base_dir / 'templates' / 'pages' / 'home.html').read_text(encoding='utf-8')
        self.assertIn('class="hero-chips"', c)
        self.assertNotIn('hero-chip--2', c)

    def test_post_list_no_badge(self):
        p = self.base_dir / 'templates' / 'blog' / 'post_list.html'
        if p.exists():
            c = p.read_text(encoding='utf-8')
            self.assertNotIn('hero-badge', c)

    def test_fix21_css(self):
        p = self.base_dir / 'static' / 'css' / 'fix21.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('.marquee-strip', c)
        self.assertIn('.hero-chips', c)
        self.assertIn('.filter-chips', c)

    def test_base_html_fix21_last(self):
        c = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')
        self.assertIn('fix21.css', c)
        idx_fix = c.find('fix21.css')
        idx_master = c.find('master.css')
        idx_ui20 = c.find('ui20.css')
        ref = max(idx_master, idx_ui20)
        if ref >= 0:
            self.assertGreater(idx_fix, ref)

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        content = res.content.decode('utf-8')
        self.assertNotIn('marquee-strip', content)
        self.assertIn('hero-chips', content)

    def test_blog_page(self):
        res = self.client.get('/blog/')
        self.assertEqual(res.status_code, 200)
        content = res.content.decode('utf-8')
        self.assertNotIn('class="hero-badge', content)

    def test_portfolio_page(self):
        res = self.client.get('/portfolio/')
        self.assertEqual(res.status_code, 200)

    def test_other_pages(self):
        for url in ['/services/web-design/', '/about-us/', '/contact/', '/styleguide/']:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")