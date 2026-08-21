import re
from django.test import TestCase, Client
from django.conf import settings
from pathlib import Path

class Phase29CssFixTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_dir = Path(settings.BASE_DIR)
        self.content = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')

    def test_single_icons_link(self):
        self.assertEqual(self.content.count('icons.css'), 1)

    def test_no_hardcoded_static_css(self):
        self.assertNotIn('href="/static/css/', self.content)
        self.assertNotIn("href='/static/css/", self.content)

    def test_no_escaped_quote_corruption(self):
        self.assertNotIn("\\'", self.content)

    def test_links_use_static_tag(self):
        links = re.findall(r'<link[^>]*stylesheet[^>]*>', self.content)
        self.assertTrue(len(links) > 0)
        for link in links:
            if 'http://' in link or 'https://' in link:
                continue
            self.assertIn('{% static', link)

    def test_cache_version_unified(self):
        links = re.findall(r'<link[^>]*stylesheet[^>]*>', self.content)
        for link in links:
            if 'http://' in link or 'https://' in link:
                continue
            self.assertIn('?v=29', link)

    def test_home_renders(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)