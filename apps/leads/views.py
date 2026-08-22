import time

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import LeadForm
from .rate_limit import is_rate_limited, record_lead_submission, get_client_ip
from .notifications import send_lead_notification


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
        # Honeypot check
        website = form.cleaned_data.get('website')
        if website:
            return super().form_valid(form)

        # IP-based rate limiting
        is_limited, remaining, retry_after = is_rate_limited(self.request)
        if is_limited:
            form.add_error(None, "درخواست‌های زیادی ارسال کرده‌اید. لطفاً چند لحظه صبر کنید.")
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

        # Record for rate limiting
        record_lead_submission(self.request)

        messages.success(self.request, "درخواست شما با موفقیت ثبت شد. کارشناسان تبریز سایت به‌زودی با شما تماس می‌گیرند.")
        return super().form_valid(form)


class LeadSuccessView(TemplateView):
    template_name = 'leads/success.html'
