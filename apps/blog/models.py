from django.db import models
from django.urls import reverse
from django.conf import settings

class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'دسته‌بندی وبلاگ'
        verbose_name_plural = 'دسته‌بندی‌های وبلاگ'

class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'تگ'
        verbose_name_plural = 'تگ‌ها'

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('published', 'منتشر شده'),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='blog/covers/', null=True, blank=True)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_posts', null=True, blank=True, on_delete=models.SET_NULL)
    author_name = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to='blog/og/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
            models.Index(fields=['published_at']),
        ]
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.alt_text:
            return f"{self.post.title} - {self.alt_text}"
        elif self.caption:
            return f"{self.post.title} - {self.caption}"
        return f"{self.post.title} - Image {self.pk or ''}"

    class Meta:
        ordering = ['order']
        verbose_name = 'تصویر مقاله'
        verbose_name_plural = 'تصاویر مقاله'