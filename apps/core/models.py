from django.db import models

class SiteSettings(models.Model):
    brand_name = models.CharField(max_length=200, default="تبریز سایت")
    brand_slug = models.SlugField(max_length=200, blank=True, allow_unicode=True)
    logo = models.ImageField(upload_to="core/site/", null=True, blank=True)
    favicon = models.ImageField(upload_to="core/site/", null=True, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    footer_text = models.TextField(blank=True)
    copyright = models.CharField(max_length=255, blank=True)
    google_search_console_verification = models.CharField(max_length=255, blank=True)
    default_seo_title = models.CharField(max_length=255, blank=True)
    default_seo_description = models.TextField(blank=True)
    default_og_image = models.ImageField(upload_to="core/site/", null=True, blank=True)
    analytics_code = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand_name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"brand_name": "تبریز سایت"})
        return obj

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

class SocialLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=255)
    icon = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "شبکه اجتماعی"
        verbose_name_plural = "شبکه‌های اجتماعی"

class MenuItem(models.Model):
    MENU_TYPES = [
        ("header", "هدر"),
        ("footer", "فوتر"),
    ]
    title = models.CharField(max_length=150)
    url = models.CharField(max_length=255)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE)
    menu_type = models.CharField(max_length=20, choices=MENU_TYPES, default="header")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["menu_type", "order", "title"]
        verbose_name = "آیتم منو"
        verbose_name_plural = "منوها"

class FAQ(models.Model):
    RELATED_PAGES = [
        ("general", "عمومی"),
        ("home", "صفحه اصلی"),
        ("about", "درباره ما"),
        ("web_design", "طراحی سایت"),
        ("seo", "سئو سایت"),
        ("portfolio", "نمونه‌کارها"),
        ("contact", "تماس"),
    ]
    question = models.TextField()
    answer = models.TextField()
    related_page = models.CharField(max_length=20, choices=RELATED_PAGES, default="general")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ["related_page", "order"]
        verbose_name = "سوال متداول"
        verbose_name_plural = "سوالات متداول"

class Testimonial(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    client_name = models.CharField(max_length=150)
    company = models.CharField(max_length=150, blank=True)
    text = models.TextField()
    avatar = models.ImageField(upload_to="core/testimonials/", null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    project = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.client_name

    class Meta:
        ordering = ["order", "client_name"]
        verbose_name = "نظر مشتری"
        verbose_name_plural = "نظرات مشتریان"

class TeamMember(models.Model):
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="core/team/", null=True, blank=True)
    linkedin = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["order", "full_name"]
        verbose_name = "عضو تیم"
        verbose_name_plural = "اعضای تیم"

class ProcessStep(models.Model):
    RELATED_PAGES = [
        ("general", "عمومی"),
        ("home", "صفحه اصلی"),
        ("about", "درباره ما"),
        ("web_design", "طراحی سایت"),
        ("seo", "سئو سایت"),
        ("portfolio", "نمونه‌کارها"),
        ("contact", "تماس"),
    ]
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    related_page = models.CharField(max_length=20, choices=RELATED_PAGES, default="general")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["related_page", "order"]
        verbose_name = "مرحله فرآیند"
        verbose_name_plural = "مراحل فرآیند"