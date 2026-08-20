import os
from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from pathlib import Path

User = get_user_model()

class Phase10SecurityTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_installed_apps(self):
        self.assertIn('axes', settings.INSTALLED_APPS)

    def test_middleware(self):
        self.assertIn('axes.middleware.AxesMiddleware', settings.MIDDLEWARE)

    def test_auth_backends(self):
        self.assertIn('axes.backends.AxesBackend', settings.AUTHENTICATION_BACKENDS)
        self.assertIn('django.contrib.auth.backends.ModelBackend', settings.AUTHENTICATION_BACKENDS)

    def test_security_settings(self):
        self.assertEqual(settings.X_FRAME_OPTIONS, 'DENY')
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, 'Lax')
        self.assertEqual(settings.CSRF_COOKIE_SAMESITE, 'Lax')
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertTrue(settings.CSRF_COOKIE_HTTPONLY)

    def test_axes_settings(self):
        self.assertTrue(settings.AXES_ENABLED)
        self.assertEqual(settings.AXES_FAILURE_LIMIT, 5)

    def test_home_headers(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')

    def test_admin_login_fail(self):
        from axes.models import AccessAttempt
        User.objects.create_superuser('admin', 'admin@test.com', 'password')
        initial_attempts = AccessAttempt.objects.count()
        response = self.client.post('/admin/login/', {'username': 'admin', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(AccessAttempt.objects.count(), initial_attempts)

    def test_admin_login_success(self):
        User.objects.create_superuser('admin2', 'admin2@test.com', 'password2')
        response = self.client.post('/admin/login/', {'username': 'admin2', 'password': 'password2'})
        self.assertEqual(response.status_code, 302)

    def test_production_file(self):
        prod_path = Path(settings.BASE_DIR) / 'config' / 'settings' / 'production.py'
        self.assertTrue(prod_path.exists())
        content = prod_path.read_text(encoding='utf-8')
        self.assertIn('DEBUG = False', content)
        self.assertIn('SECURE_SSL_REDIRECT = True', content)
        self.assertIn('SESSION_COOKIE_SECURE = True', content)
        self.assertIn('CSRF_COOKIE_SECURE = True', content)
        self.assertIn('whitenoise.middleware.WhiteNoiseMiddleware', content)
        self.assertIn('STORAGES', content)

    def test_env_example_file(self):
        env_path = Path(settings.BASE_DIR) / '.env.example'
        self.assertTrue(env_path.exists())
        content = env_path.read_text(encoding='utf-8')
        self.assertIn('SECRET_KEY', content)
        self.assertIn('ALLOWED_HOSTS', content)
        self.assertIn('DB_ENGINE', content)
        self.assertIn('DB_NAME', content)