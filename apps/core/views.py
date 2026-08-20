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