from django.core.management.base import BaseCommand
from apps.core.models import SiteSettings, SocialLink, MenuItem, FAQ, ProcessStep, Testimonial

class Command(BaseCommand):
    help = 'Initialize core data'

    def handle(self, *args, **kwargs):
        SiteSettings.load()

        if not SocialLink.objects.exists():
            SocialLink.objects.create(title="اینستاگرام", url="https://instagram.com", is_active=False, order=1)
            SocialLink.objects.create(title="لینکدین", url="https://linkedin.com", is_active=False, order=2)

        if not MenuItem.objects.exists():
            header_items = ["صفحه اصلی", "درباره ما", "خدمات", "نمونه‌کارها", "وبلاگ", "تماس"]
            for i, title in enumerate(header_items, 1):
                MenuItem.objects.create(title=title, url="#", menu_type="header", is_active=True, order=i)
            
            footer_items = ["صفحه اصلی", "درباره ما", "خدمات", "نمونه‌کارها", "تماس"]
            for i, title in enumerate(footer_items, 1):
                MenuItem.objects.create(title=title, url="#", menu_type="footer", is_active=True, order=i)

        if not FAQ.objects.exists():
            FAQ.objects.create(
                question="Sesoo چه خدماتی ارائه می‌دهد؟",
                answer="Sesoo خدمات طراحی سایت، سئو، بهینه‌سازی و پشتیبانی ارائه می‌دهد. این متن به‌زودی با محتوای واقعی جایگزین می‌شود.",
                related_page="general",
                is_active=True
            )

        if not ProcessStep.objects.exists():
            steps = ["تحلیل و مشاوره", "طراحی رابط کاربری", "توسعه و پیاده‌سازی", "تست، تحویل و پشتیبانی"]
            for i, title in enumerate(steps, 1):
                ProcessStep.objects.create(title=title, related_page="general", order=i, is_active=True)

        if not Testimonial.objects.exists():
            Testimonial.objects.create(
                client_name="مشتری نمونه",
                company="شرکت نمونه",
                text="این یک نظر نمونه است و بعداً با نظر واقعی مشتری جایگزین می‌شود.",
                rating=5,
                is_active=False
            )

        self.stdout.write(self.style.SUCCESS('Core initial data has been loaded.'))