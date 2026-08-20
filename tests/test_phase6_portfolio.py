from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from apps.portfolio.models import PortfolioCategory, ProjectTechnology, Project, ProjectImage

User = get_user_model()

class Phase6PortfolioTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_installed_apps(self):
        self.assertIn('apps.portfolio', settings.INSTALLED_APPS)

    def test_init_portfolio_command(self):
        call_command('init_portfolio')
        self.assertEqual(PortfolioCategory.objects.count(), 3)
        self.assertEqual(Project.objects.count(), 3)
        self.assertGreaterEqual(ProjectTechnology.objects.count(), 5)

    def test_init_portfolio_idempotent(self):
        call_command('init_portfolio')
        call_command('init_portfolio')
        self.assertEqual(Project.objects.count(), 3)

    def test_portfolio_list_view(self):
        call_command('init_portfolio')
        response = self.client.get('/portfolio/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'نمونه کار شرکتی تبریز سایت')
        self.assertContains(response, 'نمونه کار فروشگاهی نمونه')

    def test_portfolio_category_view(self):
        call_command('init_portfolio')
        response = self.client.get('/portfolio/category/corporate/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'نمونه کار شرکتی تبریز سایت')
        
        response_ecom = self.client.get('/portfolio/category/ecommerce/')
        self.assertEqual(response_ecom.status_code, 200)
        self.assertContains(response_ecom, 'نمونه کار فروشگاهی نمونه')

    def test_portfolio_detail_view(self):
        call_command('init_portfolio')
        response = self.client.get('/portfolio/tabriz-corporate-sample/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'چالش نمونه پروژه شرکتی')

    def test_portfolio_detail_404(self):
        response = self.client.get('/portfolio/invalid-project/')
        self.assertEqual(response.status_code, 404)

    def test_inactive_project_404(self):
        call_command('init_portfolio')
        p = Project.objects.get(slug='tabriz-corporate-sample')
        p.is_active = False
        p.save()
        response = self.client.get('/portfolio/tabriz-corporate-sample/')
        self.assertEqual(response.status_code, 404)

    def test_inactive_category_404(self):
        call_command('init_portfolio')
        cat = PortfolioCategory.objects.get(slug='corporate')
        cat.is_active = False
        cat.save()
        response = self.client.get('/portfolio/category/corporate/')
        self.assertEqual(response.status_code, 404)

    def test_admin_views(self):
        admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_login(admin_user)
        
        urls = [
            '/admin/portfolio/portfoliocategory/',
            '/admin/portfolio/project/',
            '/admin/portfolio/projectimage/',
            '/admin/portfolio/projecttechnology/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed on {url}")

    def test_get_absolute_url(self):
        call_command('init_portfolio')
        p = Project.objects.get(slug='tabriz-corporate-sample')
        self.assertIn('/portfolio/', p.get_absolute_url())
        self.assertIn('tabriz-corporate-sample', p.get_absolute_url())

    def test_project_image_str_without_image(self):
        call_command('init_portfolio')
        p = Project.objects.get(slug='tabriz-corporate-sample')
        img = ProjectImage.objects.create(project=p, alt_text='Test Alt', caption='Test Caption')
        self.assertIn('Test Alt', str(img))