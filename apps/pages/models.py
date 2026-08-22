from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from django.urls import reverse

class HomePage(models.Model):
    hero_title = models.CharField(max_length=255, default="Web Design & SEO")
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="pages/home/", null=True, blank=True)
    primary_cta_text = models.CharField(max_length=100, default="درخواست مشاوره رایگان")
    primary_cta_url = models.CharField(max_length=255, default="/contact/")
    secondary_cta_text = models.CharField(max_length=100, blank=True)
    secondary_cta_url = models.CharField(max_length=255, blank=True)
    services_heading = models.CharField(max_length=200, default="Our Services")
    services_subheading = models.TextField(blank=True)
    portfolio_heading = models.CharField(max_length=200, default="نمونه‌کارهای منتخب")
    portfolio_subheading = models.TextField(blank=True)
    testimonials_heading = models.CharField(max_length=200, default="نظرات مشتریان")
    faq_heading = models.CharField(max_length=200, default="سوالات متداول")
    blog_heading = models.CharField(max_length=200, default="آخرین مقالات")
    cta_title = models.CharField(max_length=255, default="برای شروع پروژه آماده‌ای؟")
    cta_subtitle = models.TextField(blank=True)
    cta_button_text = models.CharField(max_length=100, default="درخواست مشاوره")
    cta_button_url = models.CharField(max_length=255, default="/contact/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"hero_title": "Web Design & SEO"})
        return obj

    def __str__(self):
        return self.hero_title

    class Meta:
        verbose_name = "صفحه اصلی"
        verbose_name_plural = "صفحه اصلی"

class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="About Sesoo")
    intro = CKEditor5Field(blank=True)
    story_title = models.CharField(max_length=200, blank=True)
    story_content = CKEditor5Field(blank=True)
    mission_title = models.CharField(max_length=200, blank=True)
    mission_content = CKEditor5Field(blank=True)
    vision_title = models.CharField(max_length=200, blank=True)
    vision_content = CKEditor5Field(blank=True)
    image = models.ImageField(upload_to="pages/about/", null=True, blank=True)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"title": "About Sesoo"})
        return obj

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

class LegalPage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    content = CKEditor5Field(blank=True)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.slug == 'terms':
            return reverse('pages:terms')
        elif self.slug == 'privacy':
            return reverse('pages:privacy')
        return reverse('pages:legal', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'صفحه قانونی'
        verbose_name_plural = 'صفحات قانونی'