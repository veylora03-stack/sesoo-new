from django.db import models
from django.conf import settings

class Lead(models.Model):
    SERVICE_CHOICES = [
        ('web_design', 'طراحی سایت'),
        ('seo', 'سئو سایت'),
        ('both', 'هر دو'),
        ('other', 'سایر'),
    ]
    BUDGET_CHOICES = [
        ('unknown', 'مشخص نشده'),
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'زیاد'),
    ]
    STATUS_CHOICES = [
        ('new', 'جدید'),
        ('contacted', 'تماس گرفته شد'),
        ('qualified', 'واجد شرایط'),
        ('proposal', 'پیشنهاد داده شد'),
        ('won', 'منجر به پروژه شد'),
        ('lost', 'از دست رفت'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'زیاد'),
    ]

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='web_design')
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES, default='unknown')
    message = models.TextField(blank=True)
    source_page = models.CharField(max_length=255, blank=True)
    utm_source = models.CharField(max_length=255, blank=True)
    utm_medium = models.CharField(max_length=255, blank=True)
    utm_campaign = models.CharField(max_length=255, blank=True)
    utm_term = models.CharField(max_length=255, blank=True)
    utm_content = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='leads', on_delete=models.SET_NULL)
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.phone}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def change_status(self, new_status, user=None, note=""):
        if self.status != new_status:
            old_status = self.status
            self.status = new_status
            self.save(update_fields=['status', 'updated_at'])
            LeadLog.objects.create(
                lead=self,
                user=user,
                old_status=old_status,
                new_status=new_status,
                note=note
            )

class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, related_name='notes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lead} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']

class LeadLog(models.Model):
    lead = models.ForeignKey(Lead, related_name='logs', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lead} - {self.new_status}"

    class Meta:
        ordering = ['-created_at']