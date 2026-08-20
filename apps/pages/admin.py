from django.contrib import admin
from .models import HomePage, AboutPage, LegalPage

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('hero_title', 'primary_cta_text', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Hero', {'fields': ('hero_title', 'hero_subtitle', 'hero_image')}),
        ('CTAs', {'fields': ('primary_cta_text', 'primary_cta_url', 'secondary_cta_text', 'secondary_cta_url')}),
        ('Headings', {'fields': ('services_heading', 'services_subheading', 'portfolio_heading', 'portfolio_subheading', 'testimonials_heading', 'faq_heading', 'blog_heading', 'cta_title', 'cta_subtitle', 'cta_button_text', 'cta_button_url')}),
        ('زمان‌ها', {'fields': ('created_at', 'updated_at')}),
    )

    def has_add_permission(self, request):
        return not HomePage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('معرفی', {'fields': ('title', 'intro', 'image')}),
        ('داستان', {'fields': ('story_title', 'story_content')}),
        ('ماموریت', {'fields': ('mission_title', 'mission_content')}),
        ('چشم‌انداز', {'fields': ('vision_title', 'vision_content')}),
        ('سئو', {'fields': ('seo_title', 'seo_description')}),
        ('زمان‌ها', {'fields': ('created_at', 'updated_at')}),
    )

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'slug', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_active')