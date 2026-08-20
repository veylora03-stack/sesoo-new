from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from pathlib import Path

class Phase22DeterministicTests(TestCase):
    def setUp(self):
        self.client = Client()
        call_command('init_pages')
        call_command('init_services')
        call_command('init_portfolio')
        call_command('init_blog')
        try: call_command('load_site_content')
        except: pass
        self.base_dir = Path(settings.BASE_DIR)

    def test_base_html_fix22_last(self):
        c = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')
        self.assertIn('fix22.css?v=22', c)
        idx_fix = c.find('fix22.css')
        idx_master = c.find('master.css')
        idx_ui20 = c.find('ui20.css')
        self.assertGreater(idx_fix, idx_master)
        self.assertGreater(idx_fix, idx_ui20)

    def test_base_html_no_deprecated(self):
        c = (self.base_dir / 'templates' / 'base.html').read_text(encoding='utf-8')
        for dep in ['css/polish.css', 'css/scale.css', 'css/premium.css', 'css/finalize.css', 'css/theme.css', 'css/base.css', 'css/components.css']:
            self.assertNotIn(dep, c)

    def test_list_templates_inline_spacing(self):
        for p in ['templates/portfolio/portfolio_list.html', 'templates/blog/post_list.html']:
            f = self.base_dir / p
            if f.exists():
                c = f.read_text(encoding='utf-8')
                self.assertIn('style="margin-bottom: 2.5rem;"', c)

    def test_post_list_no_badge(self):
        f = self.base_dir / 'templates' / 'blog' / 'post_list.html'
        if f.exists():
            c = f.read_text(encoding='utf-8')
            self.assertNotIn('hero-badge', c)

    def test_home_html(self):
        c = (self.base_dir / 'templates' / 'pages' / 'home.html').read_text(encoding='utf-8')
        self.assertNotIn('marquee-strip', c)
        self.assertIn('hero-chips', c)

    def test_fix22_css(self):
        p = self.base_dir / 'static' / 'css' / 'fix22.css'
        self.assertTrue(p.exists())
        c = p.read_text(encoding='utf-8')
        self.assertIn('.filter-chips', c)
        self.assertIn('.hero-chips', c)
        self.assertIn('.marquee-strip', c)

    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('marquee-strip', res.content.decode('utf-8'))

    def test_portfolio_page(self):
        res = self.client.get('/portfolio/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('margin-bottom: 2.5rem', res.content.decode('utf-8'))

    def test_blog_page(self):
        res = self.client.get('/blog/')
        self.assertEqual(res.status_code, 200)
        self.assertNotIn('hero-badge', res.content.decode('utf-8'))

    def test_other_pages(self):
        for url in ['/services/web-design/', '/about-us/', '/contact/', '/styleguide/']:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, f"Failed on {url}")