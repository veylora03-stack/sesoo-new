from django.contrib import admin
from .models import PortfolioCategory, ProjectTechnology, Project, ProjectImage

@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_active')

@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 0
    fields = ('image', 'alt_text', 'caption', 'order', 'is_active')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client_name', 'industry', 'is_featured', 'is_active', 'order', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active', 'technologies')
    search_fields = ('title', 'slug', 'client_name', 'industry', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_featured', 'is_active')
    filter_horizontal = ('technologies',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProjectImageInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('title', 'slug', 'category', 'client_name', 'industry', 'cover_image', 'live_url')}),
        ('محتوا', {'fields': ('summary', 'challenge', 'solution', 'result')}),
        ('تکنولوژی‌ها', {'fields': ('technologies',)}),
        ('سئو', {'fields': ('seo_title', 'seo_description', 'og_image')}),
        ('وضعیت و ترتیب', {'fields': ('is_featured', 'is_active', 'order', 'created_at', 'updated_at')}),
    )

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'alt_text', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('project__title', 'alt_text', 'caption')