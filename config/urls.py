from apps.core import views as core_views
from apps.core.views import (
    test_error_view,
    healthz_view,
    healthz_detailed_view,
    robots_txt,
)
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import sitemaps

urlpatterns = [
    path('test-error/', test_error_view, name='test_error'),
    path('admin/', admin.site.urls),
    path('healthz/detailed/', healthz_detailed_view, name='healthz_detailed'),
    path('healthz/', healthz_view, name='healthz'),
    path('styleguide/', TemplateView.as_view(template_name='pages/styleguide.html'), name='styleguide'),
    path('contact/', include('apps.leads.urls', namespace='leads')),
    path('services/', include('apps.services.urls', namespace='services')),
    path('portfolio/', include('apps.portfolio.urls', namespace='portfolio')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('robots.txt', robots_txt, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('', include('apps.pages.urls', namespace='pages')),
    path("dashboard/", core_views.DashboardView.as_view(), name="dashboard"),
]


handler404 = "apps.core.views.page_not_found"
handler500 = "apps.core.views.server_error"
urlpatterns += [path("ckeditor5/", include("django_ckeditor_5.urls"))]
