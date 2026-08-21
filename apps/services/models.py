from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

class ServicePage(models.Model):
    LEAD_SERVICE_CHOICES = [
        ('web_design', 'طراحی سایت'),
        ('seo', 'سئو سایت'),
        ('both', 'هر دو'),
        ('other', 'سایر'),
    ]
    FAQ_PAGE_CHOICES = [
        ('general', 'عمومی'),
        ('home', 'صفحه اصلی'),
        ('about', 'درباره ما'),
        ('web_design', 'طراحی سایت'),
        ('seo', 'سئو سایت'),
        ('portfolio', 'نمونه‌کارها'),
        ('contact', 'تماس'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    short_description = models.TextField(blank=True)
    hero_title = models.CharField(max_length=255, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    content = RichTextUploadingField(blank=True)
    cover_image = models.ImageField(upload_to="services/pages/", null=True, blank=True)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to="services/og/", null=True, blank=True)
    lead_service_type = models.CharField(max_length=20, choices=LEAD_SERVICE_CHOICES, default='other')
    related_faq_page = models.CharField(max_length=20, choices=FAQ_PAGE_CHOICES, default='general')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'صفحه خدمت'
        verbose_name_plural = 'صفحات خدمات'

class ServiceFeature(models.Model):
    service = models.ForeignKey(ServicePage, related_name='features', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'ویژگی خدمت'
        verbose_name_plural = 'ویژگی‌های خدمات'

class ServicePricing(models.Model):
    service = models.ForeignKey(ServicePage, related_name='pricings', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price_note = models.CharField(max_length=255, blank=True)
    features = models.TextField(blank=True)
    cta_text = models.CharField(max_length=100, default='درخواست مشاوره')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'پکیج خدمت'
        verbose_name_plural = 'پکیج‌های خدمات'