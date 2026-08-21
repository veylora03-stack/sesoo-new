from apps.leads.notifications import send_lead_notification
import time
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LeadForm

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class ContactView(FormView):
    template_name = 'leads/contact.html'
    form_class = LeadForm
    success_url = reverse_lazy('leads:success')

    def get_initial(self):
        initial = super().get_initial()
        initial['source_page'] = self.request.GET.get('source', 'contact')
        service = self.request.GET.get('service')
        valid_services = ['web_design', 'seo', 'both', 'other']
        if service in valid_services:
            initial['service_type'] = service
        return initial

    def form_valid(self, form):
        website = form.cleaned_data.get('website')
        if website:
            return super().form_valid(form)

        last_lead_at = self.request.session.get('last_lead_at')
        if last_lead_at and (time.time() - last_lead_at) < 5:
            form.add_error(None, "لطفاً چند لحظه صبر کنید و دوباره تلاش کنید.")
            return self.form_invalid(form)

        instance = form.save(commit=False)
        instance.ip_address = get_client_ip(self.request)
        instance.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        
        instance.utm_source = self.request.POST.get('utm_source') or self.request.GET.get('utm_source', '')
        instance.utm_medium = self.request.POST.get('utm_medium') or self.request.GET.get('utm_medium', '')
        instance.utm_campaign = self.request.POST.get('utm_campaign') or self.request.GET.get('utm_campaign', '')
        instance.utm_term = self.request.POST.get('utm_term') or self.request.GET.get('utm_term', '')
        instance.utm_content = self.request.POST.get('utm_content') or self.request.GET.get('utm_content', '')
        
        instance.source_page = self.request.POST.get('source_page') or self.request.GET.get('source', 'contact')
        
        instance.save()
        send_lead_notification(instance)
        
        self.request.session['last_lead_at'] = time.time()
        
        messages.success(self.request, "درخواست شما با موفقیت ثبت شد. کارشناسان تبریز سایت به‌زودی با شما تماس می‌گیرند.")
        return super().form_valid(form)

class LeadSuccessView(TemplateView):
    template_name = 'leads/success.html'