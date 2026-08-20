import os
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase14PremiumUITests(TestCase):
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

    def test_fonts_css(self):
        p = self.base_dir / 'static' / 'css' / 'fonts.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('Vazirmatn', c)
        self.assertIn('Lalezar', c)

    def test_premium_css(self):
        p = self.base_dir / 'static' / 'css' / 'premium.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('--color-primary', c)
        self.assertIn('.hero', c)
        self.assertIn('.btn-primary', c)
        self.assertIn('.site-footer', c)
        self.assertTrue('data-animate' in c or 'keyframes' in c or 'transition' in c)

    def test_premium_js(self):
        p = self.base_dir / 'static' / 'js' / 'premium.js'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('IntersectionObserver', c)
        self.assertIn('prefers-reduced-motion', c)

    def test_base_html_includes(self):
        p = self.base_dir / 'templates' / 'base.html'
        c = p.read_text(encoding='utf-8')
        self.assertIn('css/fonts.css', c)
        self.assertIn('css/premium.css', c)
        self.assertIn('js/premium.js', c)

    def test_svgs_exist(self):
        self.assertTrue((self.base_dir / 'static' / 'images' / 'logo-placeholder.svg').exists())
        self.assertTrue((self.base_dir / 'static' / 'images' / 'favicon.svg').exists())
        self.assertTrue((self.base_dir / 'static' / 'images' / 'hero-illustration.svg').exists())

    def test_ui_guide(self):
        p = self.base_dir / 'docs' / 'PREMIUM_UI_GUIDE.md'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('فونت', c)

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'class="hero"')
        self.assertContains(res, 'hero-title')
        from apps.pages.models import HomePage
        home = HomePage.load()
        if home.hero_title:
            self.assertContains(res, home.hero_title)
        self.assertContains(res, 'data-animate')
        self.assertContains(res, 'درخواست مشاوره')
        self.assertContains(res, 'چرا تبریز سایت')

    def test_other_pages(self):
        urls = ['/services/', '/services/web-design/', '/about-us/', '/contact/', '/styleguide/']
        for url in urls:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")