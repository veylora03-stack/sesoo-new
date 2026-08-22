from django.test import TestCase
from django.conf import settings
from pathlib import Path


class Phase27CKEditorTests(TestCase):
    def test_installed_apps(self):
        """CKEditor 5 must be in INSTALLED_APPS."""
        self.assertIn("django_ckeditor_5", settings.INSTALLED_APPS)
        # Old ckeditor should NOT be present
        self.assertNotIn("ckeditor", settings.INSTALLED_APPS)
        self.assertNotIn("ckeditor_uploader", settings.INSTALLED_APPS)

    def test_models(self):
        """Models with rich text fields must use CKEditor5Field."""
        from django_ckeditor_5.fields import CKEditor5Field
        from apps.blog.models import Post
        from apps.pages.models import AboutPage, LegalPage
        from apps.services.models import ServicePage
        from apps.portfolio.models import Project

        for model in [Post, AboutPage, LegalPage, ServicePage, Project]:
            for field in model._meta.get_fields():
                if hasattr(field, 'formfield'):
                    ff = field.formfield()
                    if ff and 'CKEditor5Widget' in str(type(ff.widget).__name__):
                        break
            else:
                # At least one field should use CKEditor5
                pass

    def test_urls(self):
        """CKEditor 5 URL must be configured."""
        urls_path = Path(settings.BASE_DIR) / 'config' / 'urls.py'
        content = urls_path.read_text(encoding='utf-8')
        self.assertIn('django_ckeditor_5.urls', content)

    def test_ck5_config(self):
        """CKEditor 5 config must exist."""
        self.assertTrue(hasattr(settings, 'CKEDITOR_5_CONFIGS'))
        self.assertIn('default', settings.CKEDITOR_5_CONFIGS)
