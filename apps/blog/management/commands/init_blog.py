from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.blog.models import Category, Tag, Post

class Command(BaseCommand):
    help = 'Initialize blog data'

    def handle(self, *args, **kwargs):
        cat1, _ = Category.objects.get_or_create(slug='web-design', defaults={'title': 'آموزش طراحی سایت', 'description': 'مقالات آموزشی در حوزه طراحی سایت', 'order': 1, 'is_active': True})
        cat2, _ = Category.objects.get_or_create(slug='seo', defaults={'title': 'آموزش سئو', 'description': 'مقالات آموزشی در حوزه سئو و گوگل', 'order': 2, 'is_active': True})
        cat3, _ = Category.objects.get_or_create(slug='news', defaults={'title': 'اخبار تبریز سایت', 'description': 'اخبار و به‌روزرسانی‌های تبریز سایت', 'order': 3, 'is_active': True})

        tag1, _ = Tag.objects.get_or_create(slug='django', defaults={'title': 'Django'})
        tag2, _ = Tag.objects.get_or_create(slug='web-design', defaults={'title': 'طراحی سایت'})
        tag3, _ = Tag.objects.get_or_create(slug='seo', defaults={'title': 'سئو'})

        now = timezone.now()

        p1, _ = Post.objects.update_or_create(
            slug='sample-web-design-post',
            defaults={
                'title': 'نمونه مقاله آموزش طراحی سایت',
                'excerpt': 'این یک خلاصه نمونه برای مقاله آموزش طراحی سایت است.',
                'content': 'این متنplaceholder برای محتوای مقاله طراحی سایت است. در این مقاله درباره اصول اولیه طراحی سایت صحبت می‌کنیم.',
                'category': cat1,
                'status': 'published',
                'published_at': now,
                'is_featured': True,
                'author_name': 'تبریز سایت'
            }
        )
        p1.tags.add(tag1, tag2)

        p2, _ = Post.objects.update_or_create(
            slug='sample-seo-post',
            defaults={
                'title': 'نمونه مقاله آموزش سئو',
                'excerpt': 'این یک خلاصه نمونه برای مقاله آموزش سئو است.',
                'content': 'این متنplaceholder برای محتوای مقاله سئو است. در این مقاله درباره بهینه‌سازی سایت برای گوگل صحبت می‌کنیم.',
                'category': cat2,
                'status': 'published',
                'published_at': now - timedelta(days=1),
                'is_featured': False,
                'author_name': 'تبریز سایت'
            }
        )
        p2.tags.add(tag3)

        p3, _ = Post.objects.update_or_create(
            slug='sample-news-post',
            defaults={
                'title': 'نمونه خبر تبریز سایت',
                'excerpt': 'این یک خلاصه نمونه برای خبر تبریز سایت است.',
                'content': 'این متنplaceholder برای محتوای خبر است. در این خبر درباره فعالیت‌های تبریز سایت صحبت می‌کنیم.',
                'category': cat3,
                'status': 'published',
                'published_at': now - timedelta(days=2),
                'is_featured': False,
                'author_name': 'تبریز سایت'
            }
        )
        p3.tags.add(tag1)

        p4, _ = Post.objects.update_or_create(
            slug='sample-draft-post',
            defaults={
                'title': 'مقاله پیش‌نویس نمونه',
                'excerpt': 'این مقاله هنوز منتشر نشده است.',
                'content': 'این محتوا فقط برای تست وضعیت پیش‌نویس است.',
                'category': cat1,
                'status': 'draft',
                'published_at': None,
                'is_featured': False,
                'author_name': 'تبریز سایت'
            }
        )
        p4.tags.add(tag2)

        self.stdout.write(self.style.SUCCESS('Blog initial data has been loaded.'))