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
from django.db import connections
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required


def healthz_view(request):
    """
    Basic health check endpoint for load balancers and orchestrators.
    Returns 200 if all checks pass, 503 if any check fails.
    """
    status = {
        "database": "unknown",
        "cache": "unknown",
        "status": "healthy"
    }
    http_status = 200
    timeout = 5  # seconds
    
    # Check database connection
    try:
        start_time = time.time()
        db_conn = connections['default']
        db_conn.ensure_connection()
        elapsed = time.time() - start_time
        if elapsed < timeout:
            status["database"] = "connected"
        else:
            status["database"] = "slow"
            status["status"] = "degraded"
    except Exception as e:
        status["database"] = f"error: {str(e)[:100]}"
        status["status"] = "unhealthy"
        http_status = 503
    
    # Check cache connection
    try:
        start_time = time.time()
        test_key = f"health_check_{int(time.time())}"
        test_value = "test"
        cache.set(test_key, test_value, timeout=timeout)
        retrieved = cache.get(test_key)
        cache.delete(test_key)
        elapsed = time.time() - start_time
        
        if retrieved == test_value and elapsed < timeout:
            status["cache"] = "connected"
        else:
            status["cache"] = "slow"
            status["status"] = "degraded"
    except Exception as e:
        status["cache"] = f"error: {str(e)[:100]}"
        status["status"] = "unhealthy"
        http_status = 503
    
    return JsonResponse(status, status=http_status)


@staff_member_required
def healthz_detailed_view(request):
    """
    Detailed health check endpoint with system information.
    Only accessible to staff members.
    """
    status = {
        "database": "unknown",
        "cache": "unknown",
        "status": "healthy",
        "version": getattr(settings, 'APP_VERSION', '1.0.0'),
        "python_version": sys.version,
        "django_version": __import__('django').get_version(),
        "uptime": "unknown",
        "memory": {},
        "disk": {},
        "timestamp": datetime.utcnow().isoformat()
    }
    http_status = 200
    timeout = 5
    
    # Check database
    try:
        start_time = time.time()
        db_conn = connections['default']
        db_conn.ensure_connection()
        elapsed = time.time() - start_time
        status["database"] = {
            "status": "connected",
            "response_time_ms": round(elapsed * 1000, 2),
            "backend": settings.DATABASES['default']['ENGINE']
        }
    except Exception as e:
        status["database"] = {"status": "error", "message": str(e)[:200]}
        status["status"] = "unhealthy"
        http_status = 503
    
    # Check cache
    try:
        start_time = time.time()
        test_key = f"health_detailed_{int(time.time())}"
        test_value = "test_detailed"
        cache.set(test_key, test_value, timeout=timeout)
        retrieved = cache.get(test_key)
        cache.delete(test_key)
        elapsed = time.time() - start_time
        
        if retrieved == test_value:
            status["cache"] = {
                "status": "connected",
                "response_time_ms": round(elapsed * 1000, 2),
                "backend": settings.CACHES['default']['BACKEND']
            }
        else:
            status["cache"] = {"status": "error", "message": "Cache read/write failed"}
            status["status"] = "unhealthy"
            http_status = 503
    except Exception as e:
        status["cache"] = {"status": "error", "message": str(e)[:200]}
        status["status"] = "unhealthy"
        http_status = 503
    
    # System information
    try:
        process = psutil.Process()
        status["uptime"] = str(datetime.now() - datetime.fromtimestamp(process.create_time()))
        status["memory"] = {
            "rss_mb": round(process.memory_info().rss / 1024 / 1024, 2),
            "vms_mb": round(process.memory_info().vms / 1024 / 1024, 2),
            "percent": process.memory_percent()
        }
        status["disk"] = {
            "usage_percent": psutil.disk_usage('/').percent,
            "free_gb": round(psutil.disk_usage('/').free / 1024 / 1024 / 1024, 2)
        }
    except Exception as e:
        status["system_error"] = str(e)[:200]
    
    return JsonResponse(status, status=http_status)

def robots_txt(request):
    """Serve robots.txt dynamically."""
    from django.http import HttpResponse
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Disallow: /healthz/detailed/",
        "Allow: /",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def page_not_found(request, exception):
    """Custom 404 handler."""
    from django.shortcuts import render
    return render(request, 'errors/404.html', status=404)


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Staff-only dashboard view."""
    template_name = "dashboard/index.html"
    
    def test_func(self):
        return self.request.user.is_staff


def server_error(request):
    """Custom 500 handler."""
    from django.shortcuts import render
    return render(request, 'errors/500.html', status=500)
