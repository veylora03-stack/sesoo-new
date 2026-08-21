from apps.core import views as core_views
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import sitemaps
from apps.core.views import robots_txt

def healthz_view(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
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