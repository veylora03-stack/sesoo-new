from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase23IconsTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')
        try: call_command('load_site_content')
        except: pass
        self.base_dir = Path(settings.BASE_DIR)

    def test_icons_html(self):
        c = (self.base_dir / 'templates' / 'includes' / 'icons.html').read_text(encoding='utf-8')
        self.assertIn('id="i-code"', c)
        self.assertIn('id="i-instagram"', c)
        self.assertIn('id="i-arrow-left"', c)

    def test_base_html(self):
        c = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')
        self.assertIn('include "includes/icons.html"', c)
        self.assertIn('icons.css?v=23', c)

    def test_home_html(self):
        c = (self.base_dir / 'templates' / 'pages' / 'home.html').read_text(encoding='utf-8')
        self.assertIn('use href="#i-zap"', c)
        self.assertIn('use href="#i-shield"', c)
        self.assertNotIn('polyline points="22 12 18 12', c)
        self.assertIn('use href="#i-check"', c)

    def test_portfolio_card(self):
        c = (self.base_dir / 'templates' / 'includes' / 'portfolio_card.html').read_text(encoding='utf-8')
        self.assertIn('#i-image', c)
        self.assertIn('#i-arrow-left', c)

    def test_post_card(self):
        c = (self.base_dir / 'templates' / 'includes' / 'post_card.html').read_text(encoding='utf-8')
        self.assertIn('#i-article', c)

    def test_footer_html(self):
        c = (self.base_dir / 'templates' / 'includes' / 'footer.html').read_text(encoding='utf-8')
        self.assertIn('#i-mail', c)
        self.assertIn('#i-instagram', c)

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        content = res.content.decode('utf-8')
        self.assertIn('svg-sprite', content)
        self.assertIn('i-code', content)

    def test_portfolio_page(self):
        res = self.client.get('/portfolio/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('i-image', res.content.decode('utf-8'))

    def test_blog_page(self):
        res = self.client.get('/blog/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('i-article', res.content.decode('utf-8'))