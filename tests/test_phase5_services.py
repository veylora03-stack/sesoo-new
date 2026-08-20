from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from apps.services.models import ServicePage, ServiceFeature, ServicePricing

User = get_user_model()

class Phase5ServicesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_installed_apps(self):
        self.assertIn('apps.services', settings.INSTALLED_APPS)

    def test_init_services_command(self):
        call_command('init_services')
        self.assertEqual(ServicePage.objects.count(), 2)
        self.assertTrue(ServicePage.objects.filter(slug='web-design').exists())
        self.assertTrue(ServicePage.objects.filter(slug='seo').exists())
        
        wd = ServicePage.objects.get(slug='web-design')
        self.assertGreaterEqual(wd.features.count(), 4)
        
        seo = ServicePage.objects.get(slug='seo')
        self.assertGreaterEqual(seo.features.count(), 4)

    def test_init_services_idempotent(self):
        call_command('init_services')
        call_command('init_services')
        self.assertEqual(ServicePage.objects.count(), 2)

    def test_service_list_view(self):
        call_command('init_services')
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'طراحی سایت')
        self.assertContains(response, 'سئو سایت')

    def test_service_detail_view(self):
        call_command('init_services')
        response = self.client.get('/services/web-design/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'طراحی سایت حرفه‌ای در تبریز')
        
        response_seo = self.client.get('/services/seo/')
        self.assertEqual(response_seo.status_code, 200)

    def test_service_detail_404(self):
        response = self.client.get('/services/invalid-service/')
        self.assertEqual(response.status_code, 404)

    def test_inactive_service_404(self):
        call_command('init_services')
        wd = ServicePage.objects.get(slug='web-design')
        wd.is_active = False
        wd.save()
        response = self.client.get('/services/web-design/')
        self.assertEqual(response.status_code, 404)

    def test_admin_views(self):
        admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_login(admin_user)
        
        urls = [
            '/admin/services/servicepage/',
            '/admin/services/servicefeature/',
            '/admin/services/servicepricing/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed on {url}")

    def test_get_absolute_url(self):
        call_command('init_services')
        wd = ServicePage.objects.get(slug='web-design')
        self.assertIn('/services/', wd.get_absolute_url())
        self.assertIn('web-design', wd.get_absolute_url())