from django.contrib import admin
from .models import ServicePage, ServiceFeature, ServicePricing

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 0

class ServicePricingInline(admin.TabularInline):
    model = ServicePricing
    extra = 0

@admin.register(ServicePage)
class ServicePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'lead_service_type', 'related_faq_page', 'order', 'is_active', 'updated_at')
    list_filter = ('is_active', 'lead_service_type', 'related_faq_page')
    search_fields = ('title', 'slug', 'short_description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ServiceFeatureInline, ServicePricingInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('title', 'slug', 'short_description')}),
        ('محتوا و تصویر', {'fields': ('hero_title', 'hero_subtitle', 'content', 'cover_image')}),
        ('سئو', {'fields': ('seo_title', 'seo_description', 'og_image')}),
        ('تنظیمات فرم و FAQ', {'fields': ('lead_service_type', 'related_faq_page')}),
        ('وضعیت و ترتیب', {'fields': ('order', 'is_active', 'created_at', 'updated_at')}),
    )

@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

@admin.register(ServicePricing)
class ServicePricingAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'price_note', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'features')