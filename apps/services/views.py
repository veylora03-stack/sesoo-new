from django.views.generic import ListView, DetailView
from .models import ServicePage
try:
    from apps.core.models import FAQ
except ImportError:
    FAQ = None

class ServiceListView(ListView):
    model = ServicePage
    template_name = 'services/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return ServicePage.objects.filter(is_active=True).order_by('order', 'title')

class ServiceDetailView(DetailView):
    model = ServicePage
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        return ServicePage.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object
        context['features'] = service.features.filter(is_active=True).order_by('order')
        context['pricings'] = service.pricings.filter(is_active=True).order_by('order')
        if FAQ:
            try:
                context['faqs'] = FAQ.objects.filter(is_active=True, related_page=service.related_faq_page).order_by('order')
            except Exception:
                context['faqs'] = []
        else:
            context['faqs'] = []
        return context