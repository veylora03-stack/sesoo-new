from django.core.management.base import BaseCommand
from apps.services.models import ServicePage, ServiceFeature, ServicePricing
try:
    from apps.core.models import FAQ
except ImportError:
    FAQ = None

class Command(BaseCommand):
    help = 'Initialize services data'

    def handle(self, *args, **kwargs):
        wd, _ = ServicePage.objects.update_or_create(
            slug='web-design',
            defaults={
                'title': 'طراحی سایت',
                'short_description': 'طراحی سایت شرکتی، فروشگاهی و اختصاصی با تمرکز بر سرعت، امنیت و سئو.',
                'hero_title': 'طراحی سایت حرفه‌ای در Sesoo',
                'hero_subtitle': 'ساخت وب‌سایت سریع، امن و قابل توسعه برای کسب‌وکار شما',
                'content': 'این متنplaceholder برای صفحه طراحی سایت است و بعداً با محتوای واقعی جایگزین می‌شود.',
                'lead_service_type': 'web_design',
                'related_faq_page': 'web_design',
                'order': 1,
                'is_active': True,
            }
        )
        
        seo, _ = ServicePage.objects.update_or_create(
            slug='seo',
            defaults={
                'title': 'سئو سایت',
                'short_description': 'خدمات سئو تکنیکال، بهینه‌سازی محتوا و رشد ورودی گوگل.',
                'hero_title': 'خدمات سئو سایت در Sesoo',
                'hero_subtitle': 'افزایش دیده شدن در گوگل با سئوی اصولی و قابل اندازه‌گیری',
                'content': 'این متنplaceholder برای صفحه سئو سایت است و بعداً با محتوای واقعی جایگزین می‌شود.',
                'lead_service_type': 'seo',
                'related_faq_page': 'seo',
                'order': 2,
                'is_active': True,
            }
        )

        wd_features = ["طراحی رابط کاربری اختصاصی", "سازگاری با موبایل و تبلت", "سرعت بارگذاری مناسب", "قابلیت توسعه در آینده"]
        for i, title in enumerate(wd_features, 1):
            ServiceFeature.objects.update_or_create(service=wd, title=title, defaults={'order': i, 'is_active': True})

        seo_features = ["سئو تکنیکال", "بهینه‌سازی محتوا", "تحقیق کلمات کلیدی", "گزارش‌دهی دوره‌ای"]
        for i, title in enumerate(seo_features, 1):
            ServiceFeature.objects.update_or_create(service=seo, title=title, defaults={'order': i, 'is_active': True})

        ServicePricing.objects.update_or_create(
            service=wd, title='پکیج پایه',
            defaults={
                'price_note': 'تماس بگیرید',
                'features': 'طراحی صفحات اصلی\nاتصال به پنل مدیریت\nپشتیبانی اولیه',
                'cta_text': 'درخواست مشاوره',
                'is_active': False,
                'order': 1,
            }
        )

        if FAQ:
            try:
                FAQ.objects.update_or_create(
                    question="هزینه طراحی سایت چگونه محاسبه می‌شود؟",
                    defaults={
                        'answer': 'هزینه طراحی سایت بر اساس نیاز پروژه، امکانات و نوع طراحی تعیین می‌شود. این متن بعداً با محتوای واقعی جایگزین می‌شود.',
                        'related_page': 'web_design',
                        'is_active': True,
                    }
                )
                FAQ.objects.update_or_create(
                    question="مدت زمان طراحی سایت چقدر است؟",
                    defaults={
                        'answer': 'مدت زمان پروژه به امکانات و محتوای مورد نیاز بستگی دارد. این متن بعداً با محتوای واقعی جایگزین می‌شود.',
                        'related_page': 'web_design',
                        'is_active': True,
                    }
                )
                FAQ.objects.update_or_create(
                    question="نتایج سئو چه زمانی مشخص می‌شود؟",
                    defaults={
                        'answer': 'نتایج سئو معمولاً به رقابت کلمات کلیدی و وضعیت فعلی سایت بستگی دارد. این متن بعداً با محتوای واقعی جایگزین می‌شود.',
                        'related_page': 'seo',
                        'is_active': True,
                    }
                )
                FAQ.objects.update_or_create(
                    question="آیا سئو تضمینی است؟",
                    defaults={
                        'answer': 'سئوی اصولی بر پایه استانداردهای گوگل انجام می‌شود، اما تضمین رتبه دقیق امکان‌پذیر نیست. این متن بعداً با محتوای واقعی جایگزین می‌شود.',
                        'related_page': 'seo',
                        'is_active': True,
                    }
                )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Could not create FAQs: {e}'))

        self.stdout.write(self.style.SUCCESS('Services initial data has been loaded.'))