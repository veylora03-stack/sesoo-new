import os
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase14UITests(TestCase):
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

    def test_theme_css(self):
        p = self.base_dir / 'static' / 'css' / 'theme.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('--color-primary', c)
        self.assertIn('.hero', c)
        self.assertIn('.btn-primary', c)
        self.assertIn('.site-footer', c)
        self.assertTrue('data-animate' in c or 'keyframes' in c or 'transition' in c)

    def test_animations_js(self):
        p = self.base_dir / 'static' / 'js' / 'animations.js'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('IntersectionObserver', c)
        self.assertIn('prefers-reduced-motion', c)

    def test_base_html_includes(self):
        p = self.base_dir / 'templates' / 'base.html'
        c = p.read_text(encoding='utf-8')
        self.assertIn('css/fonts.css', c)
        self.assertIn('css/theme.css', c)
        self.assertIn('js/animations.js', c)

    def test_svgs_exist(self):
        self.assertTrue((self.base_dir / 'static' / 'images' / 'logo-placeholder.svg').exists())
        self.assertTrue((self.base_dir / 'static' / 'images' / 'favicon.svg').exists())

    def test_ui_guide(self):
        p = self.base_dir / 'docs' / 'UI_GUIDE.md'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('فونت', c)

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'class="hero"')
        from apps.pages.models import HomePage
        home = HomePage.load()
        if home.hero_title:
            self.assertContains(res, home.hero_title)
        self.assertContains(res, 'data-animate')
        self.assertContains(res, 'درخواست مشاوره')

    def test_other_pages(self):
        urls = ['/styleguide/', '/services/', '/services/web-design/', '/about-us/', '/contact/']
        for url in urls:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")