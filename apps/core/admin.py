from django.contrib import admin
from .models import SiteSettings, SocialLink, MenuItem, FAQ, Testimonial, TeamMember, ProcessStep

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'phone', 'email', 'city', 'is_active', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('اطلاعات برند', {'fields': ('brand_name', 'brand_slug', 'description', 'is_active')}),
        ('تماس', {'fields': ('phone', 'mobile', 'email', 'address', 'city')}),
        ('سئو و کدها', {'fields': ('default_seo_title', 'default_seo_description', 'google_search_console_verification', 'analytics_code')}),
        ('تصاویر', {'fields': ('logo', 'favicon', 'default_og_image')}),
        ('فوتر', {'fields': ('footer_text', 'copyright')}),
        ('زمان‌ها', {'fields': ('created_at', 'updated_at')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'url')
    list_filter = ('is_active',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'menu_type', 'parent', 'order', 'is_active')
    list_filter = ('menu_type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'url')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'related_page', 'order', 'is_active')
    list_filter = ('related_page', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company', 'rating', 'project', 'order', 'is_active')
    list_filter = ('rating', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('client_name', 'company', 'text')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('full_name', 'role')

@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'related_page', 'order', 'is_active')
    list_filter = ('related_page', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')