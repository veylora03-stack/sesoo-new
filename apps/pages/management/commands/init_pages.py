from django.core.management.base import BaseCommand
from apps.pages.models import HomePage, AboutPage, LegalPage
from apps.core.models import MenuItem

class Command(BaseCommand):
    help = 'Initialize pages data'

    def handle(self, *args, **kwargs):
        home = HomePage.load()
        home.hero_subtitle = "Sesoo به کسب‌وکارها کمک می‌کند با طراحی سایت حرفه‌ای و سئوی اصولی، مشتریان بیشتری از گوگل جذب کنند."
        home.primary_cta_text = "درخواست مشاوره رایگان"
        home.primary_cta_url = "/contact/"
        home.secondary_cta_text = "مشاهده خدمات"
        home.secondary_cta_url = "/services/"
        home.services_heading = "خدمات Sesoo"
        home.services_subheading = "راه‌حل‌های دیجیتال برای رشد کسب‌وکار شما"
        home.portfolio_heading = "نمونه‌کارهای منتخب"
        home.portfolio_subheading = "نگاهی به پروژه‌هایی که با افتخار انجام داده‌ایم"
        home.testimonials_heading = "نظرات مشتریان"
        home.faq_heading = "سوالات متداول"
        home.blog_heading = "آخرین مقالات"
        home.cta_title = "برای شروع پروژه آماده‌ای؟"
        home.cta_subtitle = "اطلاعات تماس خود را ثبت کن تا کارشناسان Sesoo در اولین فرصت با شما تماس بگیرند."
        home.cta_button_text = "درخواست مشاوره"
        home.cta_button_url = "/contact/"
        home.save()

        about = AboutPage.load()
        about.intro = "Sesoo یک مجموعه دیجیتال در Sesoo است که روی طراحی سایت، سئو و رشد آنلاین کسب‌وکارها تمرکز دارد. این متنplaceholder است و بعداً با محتوای واقعی جایگزین می‌شود."
        about.story_title = "داستان Sesoo"
        about.story_content = "این متنplaceholder برای داستان Sesoo است و بعداً با محتوای واقعی جایگزین می‌شود."
        about.mission_title = "ماموریت ما"
        about.mission_content = "این متنplaceholder برای ماموریت Sesoo است و بعداً با محتوای واقعی جایگزین می‌شود."
        about.vision_title = "چشم‌انداز ما"
        about.vision_content = "این متنplaceholder برای چشم‌انداز Sesoo است و بعداً با محتوای واقعی جایگزین می‌شود."
        about.seo_title = "درباره Sesoo"
        about.seo_description = "آشنایی با Sesoo، خدمات، ماموریت و تیم ما."
        about.save()

        LegalPage.objects.update_or_create(slug='terms', defaults={'title': 'قوانین و مقررات', 'content': 'این متنplaceholder برای قوانین و مقررات Sesoo است و بعداً با محتوای واقعی جایگزین می‌شود.', 'is_active': True, 'order': 1})
        LegalPage.objects.update_or_create(slug='privacy', defaults={'title': 'حریم خصوصی', 'content': 'این متنplaceholder برای حریم خصوصی Sesoo است و بعداً با محتوای واقعی جایگزین می‌شود.', 'is_active': True, 'order': 2})

        header_menus = [
            ("صفحه اصلی", "/", 1),
            ("درباره ما", "/about-us/", 2),
            ("خدمات", "/services/", 3),
            ("نمونه‌کارها", "/portfolio/", 4),
            ("وبلاگ", "/blog/", 5),
            ("تماس", "/contact/", 6),
        ]
        for title, url, order in header_menus:
            MenuItem.objects.update_or_create(title=title, menu_type='header', defaults={'url': url, 'order': order, 'is_active': True})

        footer_menus = [
            ("صفحه اصلی", "/", 1),
            ("درباره ما", "/about-us/", 2),
            ("خدمات", "/services/", 3),
            ("نمونه‌کارها", "/portfolio/", 4),
            ("وبلاگ", "/blog/", 5),
            ("تماس", "/contact/", 6),
        ]
        for title, url, order in footer_menus:
            MenuItem.objects.update_or_create(title=title, menu_type='footer', defaults={'url': url, 'order': order, 'is_active': True})

        self.stdout.write(self.style.SUCCESS('Pages initial data has been loaded.'))