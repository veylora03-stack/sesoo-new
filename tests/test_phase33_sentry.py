
import os
from django.test import TestCase, Client, override_settings
from pathlib import Path

class Phase33SentryTests(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_sentry_in_requirements(self):
        """sentry-sdk must be in prod requirements."""
        req_file = Path("requirements/prod.txt") if Path("requirements/prod.txt").exists() else Path("requirements.txt")
        self.assertTrue(req_file.exists(), "Requirements file not found")
        content = req_file.read_text(encoding="utf-8")
        self.assertIn("sentry-sdk", content)
        
    def test_sentry_init_logic_in_production(self):
        """production.py must contain sentry_sdk.init logic."""
        prod_file = Path("config/settings/production.py")
        if prod_file.exists():
            content = prod_file.read_text(encoding="utf-8")
            self.assertIn("sentry_sdk.init", content)
            self.assertIn("DjangoIntegration", content)
            
    def test_sentry_dsn_in_base_settings(self):
        """base.py must define SENTRY_DSN."""
        base_file = Path("config/settings/base.py")
        if base_file.exists():
            content = base_file.read_text(encoding="utf-8")
            self.assertIn("SENTRY_DSN", content)
            
    @override_settings(DEBUG=True)
    def test_error_view_available_in_debug(self):
        """test-error view should raise error in DEBUG mode."""
        with self.assertRaises(ValueError):
            self.client.get('/test-error/')
            
    @override_settings(DEBUG=False)
    def test_error_view_forbidden_in_production(self):
        """test-error view should return 403 when DEBUG is False."""
        response = self.client.get('/test-error/')
        self.assertEqual(response.status_code, 403)
