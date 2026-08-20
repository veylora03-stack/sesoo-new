from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Project, PortfolioCategory

class PortfolioListView(ListView):
    model = Project
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(is_active=True).select_related('category').prefetch_related('technologies').order_by('order', '-created_at', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PortfolioCategory.objects.filter(is_active=True).order_by('order')
        return context

class PortfolioCategoryView(ListView):
    model = Project
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        self.category = get_object_or_404(PortfolioCategory, slug=self.kwargs['slug'], is_active=True)
        return Project.objects.filter(is_active=True, category=self.category).select_related('category').prefetch_related('technologies').order_by('order', '-created_at', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PortfolioCategory.objects.filter(is_active=True).order_by('order')
        context['current_category'] = self.category
        return context

class PortfolioDetailView(DetailView):
    model = Project
    template_name = 'portfolio/portfolio_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context['gallery'] = project.images.filter(is_active=True).order_by('order')
        context['technologies'] = project.technologies.all()
        context['related_projects'] = Project.objects.filter(
            is_active=True, category=project.category
        ).exclude(pk=project.pk)[:3]
        return context