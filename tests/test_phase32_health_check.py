from django.contrib.auth.models import User
import time
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.db import DatabaseError

User = get_user_model()


class Phase32HealthCheckTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staffuser32',
            password='testpass123',
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username='normaluser32',
            password='testpass123',
            is_staff=False
        )
    
    def test_healthz_returns_200_when_healthy(self):
        """Health check returns 200 when database and cache are healthy"""
        response = self.client.get('/healthz/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('database', data)
        self.assertIn('cache', data)
    
    def test_healthz_returns_json_with_status(self):
        """Health check returns JSON with database and cache status"""
        response = self.client.get('/healthz/')
        data = response.json()
        self.assertIn('database', data)
        self.assertIn('cache', data)
        self.assertIn('status', data)
    
    def test_healthz_returns_503_when_database_fails(self):
        """Health check returns 503 when database connection fails"""
        with patch('apps.core.views.connections') as mock_conn:
            mock_conn.__getitem__.return_value.ensure_connection.side_effect = DatabaseError("DB down")
            response = self.client.get('/healthz/')
            self.assertEqual(response.status_code, 503)
            data = response.json()
            self.assertEqual(data['status'], 'unhealthy')
    
    def test_healthz_returns_503_when_cache_fails(self):
        """Health check returns 503 when cache connection fails"""
        with patch('apps.core.views.cache') as mock_cache:
            mock_cache.set.side_effect = Exception("Cache down")
            response = self.client.get('/healthz/')
            self.assertEqual(response.status_code, 503)
            data = response.json()
            self.assertEqual(data['status'], 'unhealthy')
    
    def test_healthz_detailed_requires_staff(self):
        """Detailed health check requires staff authentication"""
        # Anonymous user
        response = self.client.get('/healthz/detailed/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Normal user
        self.client.force_login(User.objects.create_superuser('admin32', 'a@a.com', 'pwd'))
        response = self.client.get('/healthz/detailed/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Staff user
        self.client.force_login(User.objects.create_superuser('admin32', 'a@a.com', 'pwd'))
        response = self.client.get('/healthz/detailed/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('version', data)
        self.assertIn('memory', data)
        self.assertIn('disk', data)
    
    def test_healthz_detailed_includes_system_info(self):
        """Detailed health check includes system information"""
        self.client.force_login(User.objects.create_superuser('admin32', 'a@a.com', 'pwd'))
        response = self.client.get('/healthz/detailed/')
        data = response.json()
        self.assertIn('python_version', data)
        self.assertIn('django_version', data)
        self.assertIn('uptime', data)
        self.assertIn('memory', data)
        self.assertIn('rss_mb', data['memory'])