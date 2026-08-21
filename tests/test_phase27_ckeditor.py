from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User
from apps.blog.models import Post
from apps.services.models import ServicePage
from pathlib import Path

class Phase27CKEditorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser("admin27", "admin27@example.com", "password")

    def test_installed_apps(self):
        self.assertIn("ckeditor", settings.INSTALLED_APPS)
        self.assertIn("ckeditor_uploader", settings.INSTALLED_APPS)

    def test_urls(self):
        urls_path = Path(settings.BASE_DIR) / "config" / "urls.py"
        self.assertIn("ckeditor/", urls_path.read_text(encoding="utf-8"))

    def test_models(self):
        self.assertIn("RichText", type(Post._meta.get_field("content")).__name__)
        self.assertIn("RichText", type(ServicePage._meta.get_field("content")).__name__)

    def test_admin_add_post(self):
        self.client.force_login(self.superuser)
        res = self.client.get("/admin/blog/post/add/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("ckeditor", res.content.decode("utf-8").lower())

    def test_pages_200(self):
        res = self.client.get("/services/web-design/")
        self.assertNotEqual(res.status_code, 500)
        
        res2 = self.client.get("/blog/sample-web-design-post/")
        self.assertNotEqual(res2.status_code, 500)

    def test_rich_css(self):
        css_path = Path(settings.BASE_DIR) / "static" / "css" / "rich.css"
        self.assertTrue(css_path.exists())
        base_html = Path(settings.BASE_DIR) / "templates" / "base.html"
        self.assertIn("rich.css", base_html.read_text(encoding="utf-8"))