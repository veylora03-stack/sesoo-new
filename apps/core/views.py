from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render

def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse('sitemap'))
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /healthz/",
        "Disallow: /styleguide/",
        "Allow: /",
        "",
        f"Sitemap: {sitemap_url}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")

def page_not_found(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def server_error(request):
    return render(request, 'errors/500.html', status=500)

from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

@method_decorator(staff_member_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        from apps.leads.models import Lead
        from apps.blog.models import Post
        from apps.portfolio.models import Project
        from apps.services.models import ServicePage
        ctx = super().get_context_data(**kwargs)
        week_ago = timezone.now() - timedelta(days=7)
        ctx["leads_total"] = Lead.objects.count()
        ctx["leads_new"] = Lead.objects.filter(status="new").count()
        ctx["leads_week"] = Lead.objects.filter(created_at__gte=week_ago).count()
        ctx["posts_published"] = Post.objects.filter(status="published").count()
        ctx["projects_active"] = Project.objects.filter(is_active=True).count()
        ctx["services_active"] = ServicePage.objects.filter(is_active=True).count()
        total = max(Lead.objects.count(), 1)
        ctx["status_bars"] = [
            {"label": s, "count": Lead.objects.filter(status=s).count(),
             "percent": int(Lead.objects.filter(status=s).count() * 100 / total)}
            for s, _ in Lead._meta.get_field("status").choices
        ]
        ctx["recent_leads"] = Lead.objects.order_by("-created_at")[:5]
        return ctx
