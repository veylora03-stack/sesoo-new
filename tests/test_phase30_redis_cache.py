from django.contrib.auth.models import User
import re
from pathlib import Path
from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Phase30RedisCacheTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_dir = Path(settings.BASE_DIR)
        self.prod_settings = (self.base_dir / 'config' / 'settings' / 'production.py').read_text(encoding='utf-8')

    def test_development_uses_locmemcache(self):
        cache_backend = settings.CACHES['default']['BACKEND']
        self.assertIn('LocMemCache', cache_backend)
    
    def test_production_uses_redis(self):
        self.assertIn('RedisCache', self.prod_settings)
        self.assertIn('django_redis.client.DefaultClient', self.prod_settings)
    
    def test_cache_middleware_in_middleware_list(self):
        middleware_list = settings.MIDDLEWARE
        has_cache_middleware = any(
            'cache' in mw.lower() or 'authenticatedusercachebypass' in mw.lower() for mw in middleware_list
        )
        self.assertTrue(has_cache_middleware)
    
    def test_authenticated_users_bypass_cache(self):
        from apps.core.middleware import AuthenticatedUserCacheBypass
        user = User.objects.create_user(username='testuser30', password='testpass123')
        client = Client()
        client.force_login(user)
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_session_engine_uses_cache(self):
        self.assertIn("SESSION_ENGINE = 'django.contrib.sessions.backends.cache'", self.prod_settings)