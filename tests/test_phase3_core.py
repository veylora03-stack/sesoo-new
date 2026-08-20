from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from apps.core.models import SiteSettings, SocialLink, MenuItem, FAQ, Testimonial, TeamMember, ProcessStep

User = get_user_model()

class Phase3CoreTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_installed_apps(self):
        self.assertIn('apps.core', settings.INSTALLED_APPS)

    def test_site_settings_load(self):
        obj = SiteSettings.load()
        self.assertEqual(obj.pk, 1)
        count_before = SiteSettings.objects.count()
        SiteSettings.load()
        self.assertEqual(SiteSettings.objects.count(), count_before)

    def test_social_link(self):
        sl = SocialLink.objects.create(title="Test", url="http://test.com")
        self.assertEqual(str(sl), "Test")

    def test_menu_item(self):
        mi = MenuItem.objects.create(title="Home", url="/")
        self.assertEqual(mi.menu_type, "header")

    def test_faq(self):
        faq = FAQ.objects.create(question="Q", answer="A")
        self.assertEqual(faq.related_page, "general")

    def test_testimonial(self):
        t = Testimonial.objects.create(client_name="Client", text="Text")
        self.assertEqual(t.rating, 5)

    def test_team_member(self):
        tm = TeamMember.objects.create(full_name="Name", role="Role")
        self.assertTrue(tm.pk)

    def test_process_step(self):
        ps = ProcessStep.objects.create(title="Step")
        self.assertTrue(ps.pk)

    def test_init_core_command(self):
        call_command('init_core')
        self.assertEqual(SiteSettings.objects.count(), 1)
        self.assertTrue(MenuItem.objects.exists())
        self.assertTrue(FAQ.objects.exists())
        self.assertTrue(ProcessStep.objects.exists())

    def test_admin_views(self):
        admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_login(admin_user)
        
        urls = [
            '/admin/core/sociallink/',
            '/admin/core/menuitem/',
            '/admin/core/faq/',
            '/admin/core/testimonial/',
            '/admin/core/teammember/',
            '/admin/core/processstep/',
            '/admin/core/sitesettings/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed on {url}")