from django.test import TestCase, Client
from django.conf import settings
from pathlib import Path

class Phase25BrandTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_dir = Path(settings.BASE_DIR)

    def test_svgs_exist_and_have_gradient(self):
        logo = self.base_dir / 'static' / 'images' / 'logo.svg'
        favicon = self.base_dir / 'static' / 'images' / 'favicon.svg'
        self.assertTrue(logo.exists())
        self.assertTrue(favicon.exists())
        self.assertIn('linearGradient', logo.read_text(encoding='utf-8'))
        self.assertIn('linearGradient', favicon.read_text(encoding='utf-8'))

    def test_header_logo(self):
        header = self.base_dir / 'templates' / 'includes' / 'header.html'
        self.assertIn('logo.svg', header.read_text(encoding='utf-8'))

    def test_home_page_logo(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('logo.svg', res.content.decode('utf-8'))