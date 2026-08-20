from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from apps.pages.models import HomePage, AboutPage, LegalPage
from apps.core.models import MenuItem

User = get_user_model()

class Phase8PagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_installed_apps(self):
        self.assertIn('apps.pages', settings.INSTALLED_APPS)

    def test_context_processor(self):
        cp_list = settings.TEMPLATES[0]['OPTIONS']['context_processors']
        self.assertIn('apps.core.context_processors.core_context', cp_list)

    def test_init_pages_command(self):
        call_command('init_pages')
        self.assertEqual(HomePage.objects.count(), 1)
        self.assertEqual(AboutPage.objects.count(), 1)
        self.assertEqual(LegalPage.objects.count(), 2)
        self.assertGreaterEqual(MenuItem.objects.filter(menu_type='header').count(), 6)
        self.assertGreaterEqual(MenuItem.objects.filter(menu_type='footer').count(), 6)

    def test_init_pages_idempotent(self):
        call_command('init_pages')
        call_command('init_pages')
        self.assertEqual(HomePage.objects.count(), 1)
        self.assertEqual(AboutPage.objects.count(), 1)

    def test_menu_urls(self):
        call_command('init_pages')
        service_menu = MenuItem.objects.get(title='خدمات', menu_type='header')
        self.assertEqual(service_menu.url, '/services/')

    def test_home_view(self):
        call_command('init_pages')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'طراحی سایت و سئو در تبریز')
        self.assertContains(response, 'درخواست مشاوره')
        self.assertContains(response, 'تبریز سایت')

    def test_about_view(self):
        call_command('init_pages')
        response = self.client.get('/about-us/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'درباره تبریز سایت')

    def test_legal_views(self):
        call_command('init_pages')
        response_terms = self.client.get('/terms/')
        self.assertEqual(response_terms.status_code, 200)
        self.assertContains(response_terms, 'قوانین و مقررات')

        response_privacy = self.client.get('/privacy/')
        self.assertEqual(response_privacy.status_code, 200)
        self.assertContains(response_privacy, 'حریم خصوصی')

        response_404 = self.client.get('/legal/invalid-page/')
        self.assertEqual(response_404.status_code, 404)

    def test_admin_views(self):
        admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_login(admin_user)
        
        urls = [
            '/admin/pages/homepage/',
            '/admin/pages/aboutpage/',
            '/admin/pages/legalpage/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed on {url}")

    def test_load_idempotent(self):
        HomePage.load()
        HomePage.load()
        self.assertEqual(HomePage.objects.count(), 1)

        AboutPage.load()
        AboutPage.load()
        self.assertEqual(AboutPage.objects.count(), 1)