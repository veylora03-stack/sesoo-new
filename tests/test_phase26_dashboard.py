from django.test import TestCase, Client
from django.contrib.auth.models import User

class Phase26DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.normal_user = User.objects.create_user('user', 'user@example.com', 'password')

    def test_staff_dashboard_access(self):
        self.client.force_login(self.superuser)
        res = self.client.get('/dashboard/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'داشبورد مدیریت')
        self.assertContains(res, 'لیدها بر اساس وضعیت')

    def test_normal_user_redirect(self):
        self.client.force_login(self.normal_user)
        res = self.client.get('/dashboard/')
        self.assertEqual(res.status_code, 302)

    def test_anonymous_redirect(self):
        res = self.client.get('/dashboard/')
        self.assertEqual(res.status_code, 302)