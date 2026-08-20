from django.contrib import admin
from django.utils import timezone
from .models import Category, Tag, Post, PostImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order', 'is_active')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 0
    fields = ('image', 'alt_text', 'caption', 'order', 'is_active')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'is_featured', 'published_at', 'view_count')
    list_filter = ('status', 'is_featured', 'category', 'tags')
    search_fields = ('title', 'slug', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    list_editable = ('is_featured',)
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at', 'view_count')
    inlines = [PostImageInline]

    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('title', 'slug', 'excerpt', 'author', 'author_name')}),
        ('محتوا و تصویر', {'fields': ('content', 'cover_image')}),
        ('دسته و تگ‌ها', {'fields': ('category', 'tags')}),
        ('سئو', {'fields': ('seo_title', 'seo_description', 'og_image')}),
        ('وضعیت انتشار و آمار', {'fields': ('status', 'published_at', 'is_featured', 'view_count', 'created_at', 'updated_at')}),
    )

    def save_model(self, request, obj, form, change):
        if obj.status == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)

    @admin.action(description='انتشار مقالات انتخاب شده')
    def mark_published(self, request, queryset):
        for post in queryset:
            if post.status != 'published':
                post.status = 'published'
                if not post.published_at:
                    post.published_at = timezone.now()
                post.save()
    
    @admin.action(description='پیش‌نویس کردن مقالات انتخاب شده')
    def mark_draft(self, request, queryset):
        queryset.update(status='draft')

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'alt_text', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('post__title', 'alt_text', 'caption')