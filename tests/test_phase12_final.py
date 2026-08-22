from django.test import TestCase, Client
from django.core.management import call_command
from django.conf import settings
from pathlib import Path
from apps.core.models import SiteSettings
from apps.leads.models import Lead

class Phase12FinalTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')

    def test_all_pages_200(self):
        urls = [
            '/', '/about-us/', '/services/', '/services/web-design/', '/services/seo/',
            '/portfolio/', '/portfolio/sesoo-corporate-sample/',
            '/blog/', '/blog/sample-web-design-post/',
            '/contact/', '/terms/', '/privacy/', '/healthz/', '/styleguide/'
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed on {url}")

    def test_robots_and_sitemap(self):
        res_robots = self.client.get('/robots.txt')
        self.assertEqual(res_robots.status_code, 200)
        self.assertContains(res_robots, 'Disallow: /admin/')
        self.assertContains(res_robots, 'sitemap')

        res_sitemap = self.client.get('/sitemap.xml')
        self.assertEqual(res_sitemap.status_code, 200)
        self.assertContains(res_sitemap, '/services/web-design/')
        self.assertContains(res_sitemap, '/blog/sample-web-design-post/')

    def test_lead_creation_and_honeypot(self):
        valid_data = {
            'full_name': 'کاربر تست نهایی',
            'phone': '09120000000',
            'email': 'final@example.com',
            'service_type': 'web_design',
            'budget': 'medium',
            'message': 'تست نهایی فاز 12',
            'consent': True,
            'source_page': 'contact',
            'website': '',
        }
        res = self.client.post('/contact/', valid_data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Lead.objects.count(), 1)

        honeypot_data = valid_data.copy()
        honeypot_data['website'] = 'http://spam.com'
        res_hp = self.client.post('/contact/', honeypot_data)
        self.assertEqual(res_hp.status_code, 302)
        self.assertEqual(Lead.objects.count(), 1)

    def test_404_page(self):
        res = self.client.get('/this-page-should-not-exist/')
        self.assertEqual(res.status_code, 404)
        self.assertContains(res, 'صفحه مورد نظر پیدا نشد', status_code=404)

    def test_500_template_exists(self):
        p = Path(settings.BASE_DIR) / 'templates' / 'errors' / '500.html'
        self.assertTrue(p.exists())
        content = p.read_text(encoding='utf-8')
        self.assertIn('خطایی در سرور', content)

    def test_gsc_verification(self):
        site = SiteSettings.load()
        site.google_search_console_verification = 'test-gsc-123'
        site.save()
        res = self.client.get('/')
        self.assertContains(res, 'test-gsc-123')

    def test_security_headers(self):
        res = self.client.get('/')
        self.assertIn('X-Frame-Options', res)
        self.assertIn('X-Content-Type-Options', res)

    def test_qa_script_exists(self):
        p = Path(settings.BASE_DIR) / 'scripts' / 'run_qa.ps1'
        self.assertTrue(p.exists())
        content = p.read_text(encoding='utf-8')
        self.assertIn('manage.py test', content)

    def test_docs_exist(self):
        base = Path(settings.BASE_DIR) / 'docs'
        self.assertTrue((base / 'FINAL_QA_CHECKLIST.md').exists())
        self.assertTrue((base / 'GSC_SETUP.md').exists())
        self.assertTrue((base / 'GO_LIVE_CHECKLIST.md').exists())
        
        gsc = (base / 'GSC_SETUP.md').read_text(encoding='utf-8')
        self.assertIn('Google Search Console', gsc)
        self.assertIn('google_search_console_verification', gsc)
        
        go_live = (base / 'GO_LIVE_CHECKLIST.md').read_text(encoding='utf-8')
        self.assertIn('DEBUG=False', go_live)