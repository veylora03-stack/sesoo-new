from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command

class Phase9SeoTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')

    def test_installed_apps(self):
        self.assertIn('django.contrib.sitemaps', settings.INSTALLED_APPS)
        self.assertIn('django.contrib.sites', settings.INSTALLED_APPS)
        self.assertEqual(settings.SITE_ID, 1)

    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain; charset=utf-8')
        self.assertContains(response, 'Disallow: /admin/')
        self.assertContains(response, 'Disallow: /styleguide/')
        self.assertContains(response, 'sitemap.xml')

    def test_sitemap_xml(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<urlset')
        self.assertContains(response, '/services/web-design/')
        self.assertContains(response, '/portfolio/sesoo-corporate-sample/')
        self.assertContains(response, '/blog/sample-web-design-post/')
        self.assertContains(response, '/about-us/')

    def test_home_schema(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, 'Organization')
        self.assertContains(response, 'WebSite')

    def test_styleguide_noindex(self):
        response = self.client.get('/styleguide/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'noindex')

    def test_service_schema(self):
        response = self.client.get('/services/web-design/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, 'Service')

    def test_article_schema(self):
        response = self.client.get('/blog/sample-web-design-post/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, 'Article')

    def test_creativework_schema(self):
        response = self.client.get('/portfolio/sesoo-corporate-sample/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, 'CreativeWork')