import re
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase20Design10Tests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')
        try: call_command('load_site_content')
        except: pass
        self.base_dir = Path(settings.BASE_DIR)

    def test_base_html_css(self):
        c = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')
        self.assertIn('ui20.css', c)
        self.assertNotIn('polish.css', c)
        self.assertNotIn('scale.css', c)
        self.assertNotIn('finalize.css', c)

    def test_home_html_structure(self):
        c = (self.base_dir / 'templates' / 'pages' / 'home.html').read_text(encoding='utf-8')
        self.assertIn('class="hero-chips"', c)
        self.assertIn('marquee-strip', c)

    def test_portfolio_card(self):
        p = self.base_dir / 'templates' / 'includes' / 'portfolio_card.html'
        if p.exists():
            c = p.read_text(encoding='utf-8')
            self.assertIn('pcard-cat', c)
            self.assertIn('pcard-tag', c)

    def test_post_card(self):
        p = self.base_dir / 'templates' / 'includes' / 'post_card.html'
        if p.exists():
            c = p.read_text(encoding='utf-8')
            self.assertIn('bcard-cat', c)
            self.assertIn('bcard-meta', c)
            self.assertIn('bcard-more', c)

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'marquee-strip')
        self.assertContains(res, 'hero-chips')

    def test_portfolio_page(self):
        res = self.client.get('/portfolio/')
        self.assertEqual(res.status_code, 200)
        content = res.content.decode('utf-8')
        self.assertTrue('filter-chips' in content or 'empty-state' in content or 'pcard' in content)

    def test_blog_page(self):
        res = self.client.get('/blog/')
        self.assertEqual(res.status_code, 200)
        content = res.content.decode('utf-8')
        self.assertTrue('search-box' in content or 'bcard' in content or 'empty-state' in content)

    def test_other_pages(self):
        for url in ['/services/web-design/', '/about-us/', '/contact/', '/styleguide/']:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")