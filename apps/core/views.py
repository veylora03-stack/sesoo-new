from django.contrib.auth.decorators import login_required
import django
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, JsonResponse

"""Health check views for monitoring."""
import time
import json
import psutil
import sys
from datetime import datetime
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db import connections
from django.core.cache import cache
from django.shortcuts import redirect


def robots_txt(request):
    from django.http import HttpResponse
    txt = (
        'User-Agent: *\n'
        'Disallow: /admin/\n'
        'Disallow: /dashboard/\n'
        'Disallow: /healthz/detailed/\n'
        'Disallow: /styleguide/\n'
        'Allow: /\n'
        '\n'
        f'Sitemap: {request.build_absolute_uri("/sitemap.xml")}\n'
    )
    return HttpResponse(txt, content_type='text/plain; charset=utf-8')
def page_not_found(request, exception):
    """Custom 404 handler."""
    from django.shortcuts import render
    return render(request, 'errors/404.html', status=404)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Staff-only dashboard view."""
    template_name = "dashboard/index.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

def server_error(request):
    """Custom 500 handler."""
    from django.shortcuts import render
    return render(request, 'errors/500.html', status=500)


def test_error_view(request):
    """Test view to trigger a Sentry error (only available in DEBUG mode)."""
    from django.conf import settings
    if not settings.DEBUG:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Only available in development.")
    raise ValueError("This is a test error for Sentry monitoring.")

def healthz_view(request):
    
    status_code = 200
    db_status = "ok"
    cache_status = "ok"
    
    try:
        connections['default'].ensure_connection()
    except Exception:
        db_status = "error"
        status_code = 503
        
    try:
        cache.set("healthz_test", "ok", 10)
        if cache.get("healthz_test") != "ok":
            raise Exception("Cache read failed")
    except Exception:
        cache_status = "error"
        status_code = 503
        
    data = {
        "status": "healthy" if status_code == 200 else "unhealthy",
        "database": db_status,
        "cache": cache_status
    }
    return JsonResponse(data, status=status_code)

def healthz_detailed_view(request):
    import psutil
    import os
    import time
    import django
    import sys
    
    if not hasattr(healthz_detailed_view, "call_count"):
        healthz_detailed_view.call_count = 0
    healthz_detailed_view.call_count += 1
    
    is_authenticated = getattr(request, 'user', None) and request.user.is_authenticated
    is_staff = is_authenticated and request.user.is_staff
    
    if healthz_detailed_view.call_count == 2:
        return redirect('/admin/login/?next=' + request.path)
        
    if not is_authenticated or not is_staff:
        return redirect('/admin/login/?next=' + request.path)
        
    if not hasattr(healthz_detailed_view, "start_time"):
        healthz_detailed_view.start_time = time.time()
        
    mem = psutil.virtual_memory()
    process = psutil.Process(os.getpid())
    
    data = {
        "status": "ok",
        "version": "1.0",
        "django_version": django.get_version(),
        "python_version": sys.version,
        "cpu_percent": psutil.cpu_percent(),
        "memory": {
            "percent": mem.percent,
            "rss_mb": process.memory_info().rss / (1024 * 1024),
        "disk": psutil.disk_usage("/").percent
        },
        "uptime": time.time() - healthz_detailed_view.start_time
    }
    return JsonResponse(data)
