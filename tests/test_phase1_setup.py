from django.test import TestCase, Client
from django.conf import settings

class Phase1SetupTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_healthz_status_code(self):
        response = self.client.get('/healthz/')
        self.assertEqual(response.status_code, 200)

    def test_healthz_content(self):
        response = self.client.get('/healthz/')
        self.assertJSONEqual(response.content, {"status": "ok"})

    def test_admin_redirect(self):
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [301, 302])

    def test_secret_key(self):
        self.assertTrue(bool(settings.SECRET_KEY))

    def test_installed_apps(self):
        self.assertIn('django.contrib.admin', settings.INSTALLED_APPS)