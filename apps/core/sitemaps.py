from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.urls import reverse
from apps.services.models import ServicePage
from apps.portfolio.models import Project, PortfolioCategory
from apps.blog.models import Post, Category

class StaticSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return [
            'pages:home', 'pages:about', 'leads:contact', 
            'services:list', 'portfolio:list', 'blog:list', 
            'pages:terms', 'pages:privacy'
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        if item in ['pages:home', 'services:list', 'portfolio:list', 'blog:list']:
            return 0.9
        return 0.6

class PortfolioCategorySitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        return PortfolioCategory.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('portfolio:category', kwargs={'slug': obj.slug})

sitemaps = {
    'static': StaticSitemap,
    'services': GenericSitemap({'queryset': ServicePage.objects.filter(is_active=True), 'date_field': 'updated_at'}, priority=0.9),
    'portfolio_categories': PortfolioCategorySitemap,
    'portfolio_projects': GenericSitemap({'queryset': Project.objects.filter(is_active=True), 'date_field': 'updated_at'}, priority=0.8),
    'blog_categories': GenericSitemap({'queryset': Category.objects.filter(is_active=True)}, priority=0.6),
    'blog_posts': GenericSitemap({'queryset': Post.objects.filter(status="published"), 'date_field': 'published_at'}, priority=0.7),
}