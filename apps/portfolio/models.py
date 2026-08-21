from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

class PortfolioCategory(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'دسته‌بندی نمونه‌کار'
        verbose_name_plural = 'دسته‌بندی‌های نمونه‌کار'

class ProjectTechnology(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'تکنولوژی پروژه'
        verbose_name_plural = 'تکنولوژی‌های پروژه'

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    category = models.ForeignKey(PortfolioCategory, related_name='projects', on_delete=models.PROTECT)
    client_name = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=200, blank=True)
    cover_image = models.ImageField(upload_to='portfolio/covers/', null=True, blank=True)
    summary = RichTextUploadingField(blank=True)
    challenge = RichTextUploadingField(blank=True)
    solution = RichTextUploadingField(blank=True)
    result = RichTextUploadingField(blank=True)
    live_url = models.URLField(blank=True)
    technologies = models.ManyToManyField(ProjectTechnology, related_name='projects', blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to='portfolio/og/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['order', '-created_at', 'title']
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه‌ها'

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/images/', null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.alt_text:
            return f"{self.project.title} - {self.alt_text}"
        elif self.caption:
            return f"{self.project.title} - {self.caption}"
        return f"{self.project.title} - Image {self.pk or ''}"

    class Meta:
        ordering = ['order']
        verbose_name = 'تصویر پروژه'
        verbose_name_plural = 'تصاویر پروژه'