from django.core.management.base import BaseCommand
from apps.portfolio.models import PortfolioCategory, ProjectTechnology, Project

class Command(BaseCommand):
    help = 'Initialize portfolio data'

    def handle(self, *args, **kwargs):
        cat1, _ = PortfolioCategory.objects.get_or_create(slug='corporate', defaults={'title': 'وب‌سایت شرکتی', 'description': 'نمونه‌کارهای طراحی وب‌سایت شرکتی', 'order': 1, 'is_active': True})
        cat2, _ = PortfolioCategory.objects.get_or_create(slug='ecommerce', defaults={'title': 'فروشگاه اینترنتی', 'description': 'نمونه‌کارهای طراحی فروشگاه اینترنتی', 'order': 2, 'is_active': True})
        cat3, _ = PortfolioCategory.objects.get_or_create(slug='seo-projects', defaults={'title': 'پروژه‌های سئو', 'description': 'نمونه‌کارها و نتایج پروژه‌های سئو', 'order': 3, 'is_active': True})

        techs = {}
        for t in ['Django', 'Python', 'HTML/CSS', 'JavaScript', 'SEO']:
            techs[t], _ = ProjectTechnology.objects.get_or_create(title=t)

        if not Project.objects.filter(slug='sesoo-corporate-sample').exists():
            p1 = Project.objects.create(
                title='Sesoo Corporate Sample', slug='sesoo-corporate-sample', category=cat1,
                client_name='مشتری نمونه', industry='خدمات',
                summary='این یک خلاصه نمونه برای پروژه شرکتی است و بعداً با محتوای واقعی جایگزین می‌شود.',
                challenge='چالش نمونه پروژه شرکتی در این بخش قرار می‌گیرد.',
                solution='راه‌حل نمونه پروژه شرکتی در این بخش قرار می‌گیرد.',
                result='نتیجه نهایی پروژه شرکتی در این بخش قرار می‌گیرد.',
                is_featured=True, is_active=True, order=1
            )
            p1.technologies.add(techs['Django'], techs['Python'], techs['HTML/CSS'])

        if not Project.objects.filter(slug='sample-ecommerce').exists():
            p2 = Project.objects.create(
                title='نمونه کار فروشگاهی نمونه', slug='sample-ecommerce', category=cat2,
                client_name='فروشگاه نمونه', industry='تجارت الکترونیک',
                summary='این یک خلاصه نمونه برای پروژه فروشگاهی است و بعداً با محتوای واقعی جایگزین می‌شود.',
                challenge='چالش نمونه پروژه فروشگاهی در این بخش قرار می‌گیرد.',
                solution='راه‌حل نمونه پروژه فروشگاهی در این بخش قرار می‌گیرد.',
                result='نتیجه نهایی پروژه فروشگاهی در این بخش قرار می‌گیرد.',
                is_featured=True, is_active=True, order=2
            )
            p2.technologies.add(techs['Django'], techs['JavaScript'], techs['HTML/CSS'])

        if not Project.objects.filter(slug='sample-seo-project').exists():
            p3 = Project.objects.create(
                title='نمونه پروژه سئو', slug='sample-seo-project', category=cat3,
                client_name='مشتری نمونه سئو', industry='خدمات',
                summary='این یک خلاصه نمونه برای پروژه سئو است و بعداً با محتوای واقعی جایگزین می‌شود.',
                challenge='چالش نمونه پروژه سئو در این بخش قرار می‌گیرد.',
                solution='راه‌حل نمونه پروژه سئو در این بخش قرار می‌گیرد.',
                result='نتیجه نهایی پروژه سئو در این بخش قرار می‌گیرد.',
                is_featured=False, is_active=True, order=3
            )
            p3.technologies.add(techs['SEO'])

        self.stdout.write(self.style.SUCCESS('Portfolio initial data has been loaded.'))