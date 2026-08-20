from django.views.generic import TemplateView, DetailView
from .models import HomePage, AboutPage, LegalPage
try:
    from apps.services.models import ServicePage
    from apps.portfolio.models import Project
    from apps.core.models import Testimonial, FAQ, ProcessStep, TeamMember
    from apps.blog.models import Post
except ImportError:
    pass

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home'] = HomePage.load()
        try:
            context['services'] = ServicePage.objects.filter(is_active=True).order_by('order', 'title')
            context['featured_projects'] = Project.objects.filter(is_active=True, is_featured=True).select_related('category').order_by('order', '-created_at')[:6]
            context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('order')[:6]
            context['faqs'] = FAQ.objects.filter(is_active=True, related_page__in=['home', 'general']).order_by('order')
            context['process_steps'] = ProcessStep.objects.filter(is_active=True, related_page__in=['home', 'general']).order_by('order')
            context['latest_posts'] = Post.objects.filter(status='published').select_related('category').order_by('-published_at', '-created_at')[:3]
        except Exception:
            pass
        return context

class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = AboutPage.load()
        try:
            context['team_members'] = TeamMember.objects.filter(is_active=True).order_by('order')
            context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('order')[:3]
        except Exception:
            pass
        return context

class LegalDetailView(DetailView):
    model = LegalPage
    template_name = 'pages/legal.html'
    context_object_name = 'page'

    def get_queryset(self):
        return LegalPage.objects.filter(is_active=True)