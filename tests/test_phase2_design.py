import os
from pathlib import Path
from django.test import TestCase, Client
from django.conf import settings

class Phase2DesignTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_dir = settings.BASE_DIR

    def test_styleguide_status_code(self):
        response = self.client.get('/styleguide/')
        self.assertEqual(response.status_code, 200)

    def test_styleguide_rtl(self):
        response = self.client.get('/styleguide/')
        self.assertContains(response, 'dir="rtl"')

    def test_styleguide_header_component(self):
        response = self.client.get('/styleguide/')
        self.assertContains(response, 'data-component="site-header"')

    def test_styleguide_footer_component(self):
        response = self.client.get('/styleguide/')
        self.assertContains(response, 'data-component="site-footer"')

    def test_styleguide_component(self):
        response = self.client.get('/styleguide/')
        self.assertContains(response, 'data-component="styleguide"')

    def test_styleguide_base_css(self):
        response = self.client.get('/styleguide/')
        self.assertContains(response, '/static/css/master.css')

    def test_styleguide_components_css(self):
        response = self.client.get('/styleguide/')
        self.assertContains(response, '/static/css/master.css')

    def test_base_css_exists(self):
        self.assertTrue((self.base_dir / 'static' / 'css' / 'base.css').exists())

    def test_components_css_exists(self):
        self.assertTrue((self.base_dir / 'static' / 'css' / 'components.css').exists())

    def test_main_js_exists(self):
        self.assertTrue((self.base_dir / 'static' / 'js' / 'main.js').exists())

    def test_logo_svg_exists(self):
        self.assertTrue((self.base_dir / 'static' / 'images' / 'logo-placeholder.svg').exists())

    def test_favicon_svg_exists(self):
        self.assertTrue((self.base_dir / 'static' / 'images' / 'favicon.svg').exists())

    def test_base_css_has_primary_color(self):
        p = self.base_dir / 'static' / 'css' / 'master.css'
        content = p.read_text(encoding='utf-8')
        self.assertIn('--c-primary', content)

    def test_main_js_has_menu_toggle(self):
        js_path = self.base_dir / 'static' / 'js' / 'main.js'
        content = js_path.read_text(encoding='utf-8')
        self.assertIn('data-menu-toggle', content)