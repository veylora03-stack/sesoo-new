from django.test import TestCase, Client, override_settings
from django.core import mail
from django.conf import settings
from pathlib import Path
from apps.leads.models import Lead

class Phase24NotifyTests(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(LEAD_NOTIFY_EMAIL="admin@example.com", EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_lead_notification_email(self):
        res = self.client.get('/contact/')
        form = None
        if hasattr(res, 'context') and res.context:
            form = res.context.get('form')
            if not form:
                for k, v in res.context.items():
                    if hasattr(v, 'fields'):
                        form = v
                        break
                        
        data = {}
        if form:
            for name, field in form.fields.items():
                if field.required:
                    if hasattr(field, 'choices') and field.choices:
                        for c in field.choices:
                            if c[0] != '' and c[0] is not None:
                                data[name] = c[0]
                                break
                    elif field.__class__.__name__ == 'BooleanField':
                        data[name] = True
                    else:
                        data[name] = 'Test'
                        
        data['full_name'] = 'Test User'
        data['phone'] = '09123456789'
        data['email'] = 'test@example.com'
        data['message'] = 'Hello test message'
        if form and 'consent' in form.fields:
            data['consent'] = True
            
        for k in list(data.keys()):
            if 'honeypot' in k.lower() or k in ['website', 'url', 'company']:
                data[k] = ''
                
        res = self.client.post('/contact/', data)
        if Lead.objects.count() == 0 and hasattr(res, 'context') and res.context and res.context.get('form'):
            import sys
            print("FORM ERRORS:", res.context['form'].errors, file=sys.stderr)
            
        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('09123456789', mail.outbox[0].body)

    def test_development_settings(self):
        dev_path = Path(settings.BASE_DIR) / 'config' / 'settings' / 'development.py'
        if dev_path.exists():
            content = dev_path.read_text(encoding='utf-8')
            self.assertIn('AXES_FAILURE_LIMIT', content)

    def test_contact_get(self):
        res = self.client.get('/contact/')
        self.assertEqual(res.status_code, 200)