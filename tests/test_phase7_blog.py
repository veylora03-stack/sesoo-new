from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from apps.blog.models import Category, Tag, Post, PostImage

User = get_user_model()

class Phase7BlogTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_installed_apps(self):
        self.assertIn('apps.blog', settings.INSTALLED_APPS)

    def test_init_blog_command(self):
        call_command('init_blog')
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(Post.objects.count(), 4)
        self.assertEqual(Post.objects.filter(status='published').count(), 3)
        self.assertEqual(Post.objects.filter(status='draft').count(), 1)

    def test_init_blog_idempotent(self):
        call_command('init_blog')
        call_command('init_blog')
        self.assertEqual(Post.objects.count(), 4)

    def test_blog_list_view(self):
        call_command('init_blog')
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'نمونه مقاله آموزش طراحی سایت')
        self.assertContains(response, 'نمونه مقاله آموزش سئو')
        self.assertNotContains(response, 'مقاله پیش‌نویس نمونه')

    def test_blog_search(self):
        call_command('init_blog')
        response = self.client.get('/blog/?q=طراحی')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'نمونه مقاله آموزش طراحی سایت')

    def test_blog_category_view(self):
        call_command('init_blog')
        response = self.client.get('/blog/category/web-design/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'نمونه مقاله آموزش طراحی سایت')
        
        response_seo = self.client.get('/blog/category/seo/')
        self.assertEqual(response_seo.status_code, 200)
        self.assertContains(response_seo, 'نمونه مقاله آموزش سئو')

    def test_blog_tag_view(self):
        call_command('init_blog')
        response = self.client.get('/blog/tag/django/')
        self.assertEqual(response.status_code, 200)
        response_seo = self.client.get('/blog/tag/seo/')
        self.assertEqual(response_seo.status_code, 200)

    def test_blog_detail_view(self):
        call_command('init_blog')
        response = self.client.get('/blog/sample-web-design-post/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'اصول اولیه طراحی سایت')

    def test_blog_draft_404(self):
        call_command('init_blog')
        response = self.client.get('/blog/sample-draft-post/')
        self.assertEqual(response.status_code, 404)

    def test_blog_invalid_404(self):
        response = self.client.get('/blog/invalid-post/')
        self.assertEqual(response.status_code, 404)

    def test_view_count_increment(self):
        call_command('init_blog')
        post = Post.objects.get(slug='sample-web-design-post')
        initial_count = post.view_count
        self.client.get('/blog/sample-web-design-post/')
        post.refresh_from_db()
        self.assertEqual(post.view_count, initial_count + 1)

    def test_admin_views(self):
        admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_login(admin_user)
        
        urls = [
            '/admin/blog/category/',
            '/admin/blog/tag/',
            '/admin/blog/post/',
            '/admin/blog/postimage/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed on {url}")

    def test_get_absolute_url(self):
        call_command('init_blog')
        p = Post.objects.get(slug='sample-web-design-post')
        self.assertIn('/blog/', p.get_absolute_url())
        self.assertIn('sample-web-design-post', p.get_absolute_url())

    def test_post_image_str_without_image(self):
        call_command('init_blog')
        p = Post.objects.get(slug='sample-web-design-post')
        img = PostImage.objects.create(post=p, alt_text='Test Alt', caption='Test Caption')
        self.assertIn('Test Alt', str(img))