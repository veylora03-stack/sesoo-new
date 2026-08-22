"""
Real production validation tests.
Tests actual behavior, not just file existence.
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()


class BlogSearchTests(TestCase):
    """Test blog search functionality."""

    def setUp(self):
        self.client = Client()
        cache.clear()
        from apps.blog.models import Post, Category
        self.category = Category.objects.create(
            title='Test Category', slug='test-cat', is_active=True
        )
        self.post = Post.objects.create(
            title='طراحی سایت حرفه‌ای',
            slug='test-post-1',
            content='محتوای تست درباره طراحی سایت',
            category=self.category,
            status='published',
        )

    def test_blog_list_returns_200(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_blog_search_finds_post(self):
        response = self.client.get('/blog/', {'q': 'طراحی سایت'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'طراحی سایت حرفه‌ای')

    def test_blog_search_no_results(self):
        response = self.client.get('/blog/', {'q': 'چیزی که وجود ندارد'})
        self.assertEqual(response.status_code, 200)

    def test_blog_category_page(self):
        response = self.client.get(f'/blog/category/{self.category.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'طراحی سایت حرفه‌ای')

    def test_blog_detail_page(self):
        response = self.client.get(f'/blog/{self.post.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'طراحی سایت حرفه‌ای')

    def test_blog_404(self):
        response = self.client.get('/blog/nonexistent-post/')
        self.assertEqual(response.status_code, 404)


class ServicesTests(TestCase):
    """Test services functionality."""

    def setUp(self):
        self.client = Client()
        from apps.services.models import ServicePage
        self.service = ServicePage.objects.create(
            title='طراحی سایت',
            slug='web-design',
            short_description='خدمات طراحی سایت',
            is_active=True,
        )

    def test_services_list(self):
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)

    def test_services_detail(self):
        response = self.client.get('/services/web-design/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'طراحی سایت')

    def test_services_404(self):
        response = self.client.get('/services/nonexistent/')
        self.assertEqual(response.status_code, 404)


class PermissionTests(TestCase):
    """Test access controls."""

    def setUp(self):
        self.client = Client()

    def test_admin_requires_login(self):
        response = self.client.get('/admin/')
        self.assertIn(response.status_code, [302, 403])

    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_staff(self):
        user = User.objects.create_user('regular', 'r@test.com', 'pass')
        self.client.force_login(user)
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirects to /

    def test_healthz_public(self):
        response = self.client.get('/healthz/')
        self.assertEqual(response.status_code, 200)

    def test_healthz_detailed_requires_staff(self):
        response = self.client.get('/healthz/detailed/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User-Agent')

    def test_sitemap(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)

    def test_test_error_forbidden_in_production(self):
        """test-error should return 403 when DEBUG=False."""
        from django.test import override_settings
        with override_settings(DEBUG=False):
            response = self.client.get('/test-error/')
            self.assertEqual(response.status_code, 403)


class SecurityHeadersTests(TestCase):
    """Test security headers are present."""

    def setUp(self):
        self.client = Client()

    def test_x_frame_options(self):
        response = self.client.get('/')
        self.assertEqual(response.get('X-Frame-Options'), 'DENY')

    def test_x_content_type_options(self):
        response = self.client.get('/')
        self.assertEqual(response.get('X-Content-Type-Options'), 'nosniff')

    def test_no_server_header_leak(self):
        response = self.client.get('/')
        # Should not expose server software
        self.assertNotIn('Server', response)


class PageTests(TestCase):
    """Test all main pages return 200."""

    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get('/about-us/')
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_styleguide(self):
        response = self.client.get('/styleguide/')
        self.assertEqual(response.status_code, 200)

    def test_404_page(self):
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
