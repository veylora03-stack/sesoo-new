import time
from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from apps.leads.models import Lead, LeadNote, LeadLog

User = get_user_model()


class Phase4LeadsTests(TestCase):
    def setUp(self):
        self.client = Client()
        cache.clear()  # Clear rate limiting cache between tests
        self.valid_data = {
            'full_name': 'کاربر تست',
            'phone': '09123456789',
            'email': 'test@example.com',
            'service_type': 'web_design',
            'budget': 'medium',
            'message': 'این یک پیام تست است.',
            'consent': True,
            'source_page': 'contact',
            'website': '',
        }

    def test_installed_apps(self):
        self.assertIn('apps.leads', settings.INSTALLED_APPS)

    def test_contact_get(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'phone')
        self.assertContains(response, 'full_name')

    def test_valid_post(self):
        response = self.client.post('/contact/', self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lead.objects.count(), 1)
        lead = Lead.objects.first()
        self.assertEqual(lead.status, 'new')
        self.assertTrue(lead.consent)
        self.assertEqual(lead.phone, '09123456789')

    def test_invalid_phone(self):
        data = self.valid_data.copy()
        data['phone'] = '123'
        response = self.client.post('/contact/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)
        self.assertContains(response, 'شماره تماس معتبر نیست')

    def test_no_consent(self):
        data = self.valid_data.copy()
        data['consent'] = False
        response = self.client.post('/contact/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_honeypot(self):
        data = self.valid_data.copy()
        data['website'] = 'http://spam.example.com'
        response = self.client.post('/contact/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lead.objects.count(), 0)

    def test_rate_limit(self):
        """IP-based rate limiting blocks after too many submissions."""
        for i in range(5):
            data = self.valid_data.copy()
            data['phone'] = f'0912345678{i}'
            response = self.client.post('/contact/', data)
            self.assertEqual(response.status_code, 302, f"Lead {i+1} should succeed")

        self.assertEqual(Lead.objects.count(), 5)

        # 6th request should be rate limited
        data = self.valid_data.copy()
        data['phone'] = '09123456780'
        response = self.client.post('/contact/', data)
        self.assertEqual(response.status_code, 200)  # Form with error
        self.assertEqual(Lead.objects.count(), 5)  # No new lead

    def test_missing_required_fields(self):
        """Missing required fields should fail validation."""
        data = {
            'full_name': '',
            'phone': '',
            'consent': True,
            'website': '',
        }
        response = self.client.post('/contact/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 0)

    def test_change_status(self):
        lead = Lead.objects.create(full_name='Test', phone='09123456789', consent=True)
        lead.change_status('contacted')
        lead.refresh_from_db()
        self.assertEqual(lead.status, 'contacted')
        self.assertEqual(LeadLog.objects.count(), 1)

    def test_admin_views(self):
        admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_login(admin_user)

        urls = [
            '/admin/leads/lead/',
            '/admin/leads/leadnote/',
            '/admin/leads/leadlog/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed on {url}")
