from django.test import TestCase, Client
from django.core.management import call_command
from apps.pages.models import HomePage, AboutPage, LegalPage
from apps.services.models import ServicePage
from apps.core.models import FAQ, ProcessStep, Testimonial

class Phase13ContentTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_load_site_content_command(self):
        call_command('load_site_content')
        call_command('load_site_content')

        home = HomePage.load()
        self.assertTrue(home.hero_title)
        self.assertNotIn('placeholder', home.hero_title)
        self.assertNotIn('placeholder', home.hero_subtitle)

        about = AboutPage.load()
        self.assertTrue(about.intro)
        self.assertNotIn('placeholder', about.intro)

        self.assertTrue(ServicePage.objects.filter(slug='web-design').exists())
        self.assertTrue(ServicePage.objects.filter(slug='seo').exists())
        
        wd = ServicePage.objects.get(slug='web-design')
        seo = ServicePage.objects.get(slug='seo')
        self.assertNotIn('placeholder', wd.content)
        self.assertNotIn('placeholder', seo.content)
        self.assertTrue(wd.seo_title)
        self.assertTrue(wd.seo_description)
        self.assertTrue(seo.seo_title)
        self.assertTrue(seo.seo_description)

        self.assertGreaterEqual(FAQ.objects.filter(is_active=True).count(), 10)
        self.assertGreaterEqual(FAQ.objects.filter(is_active=True, related_page='web_design').count(), 4)
        self.assertGreaterEqual(FAQ.objects.filter(is_active=True, related_page='seo').count(), 4)
        self.assertGreaterEqual(ProcessStep.objects.filter(is_active=True).count(), 5)

        terms = LegalPage.objects.get(slug='terms')
        privacy = LegalPage.objects.get(slug='privacy')
        self.assertTrue(terms.content)
        self.assertTrue(privacy.content)
        self.assertNotIn('placeholder', terms.content)
        self.assertNotIn('placeholder', privacy.content)

        active_testimonials = Testimonial.objects.filter(is_active=True)
        for t in active_testimonials:
            self.assertNotIn('نمونه', t.client_name)
            self.assertNotIn('placeholder', t.client_name)
            self.assertNotIn('نمونه', t.text)
            self.assertNotIn('placeholder', t.text)

    def test_page_responses(self):
        call_command('load_site_content')
        urls = ['/', '/about-us/', '/services/web-design/', '/services/seo/', '/terms/', '/privacy/']
        for url in urls:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")
            
        home = HomePage.load()
        res_home = self.client.get('/')
        self.assertContains(res_home, home.hero_title)