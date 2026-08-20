import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from .models import Lead, LeadNote, LeadLog

class LeadNoteInline(admin.TabularInline):
    model = LeadNote
    extra = 0

class LeadLogInline(admin.TabularInline):
    model = LeadLog
    extra = 0
    readonly_fields = ('user', 'old_status', 'new_status', 'note', 'created_at')
    can_delete = False

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'service_type', 'budget', 'status', 'priority', 'consent', 'created_at')
    list_filter = ('status', 'priority', 'service_type', 'budget', 'consent', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'message')
    list_editable = ('status', 'priority')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'user_agent', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content')
    inlines = [LeadNoteInline, LeadLogInline]
    
    fieldsets = (
        ('اطلاعات تماس', {'fields': ('full_name', 'phone', 'email')}),
        ('جزئیات درخواست', {'fields': ('service_type', 'budget', 'message', 'consent')}),
        ('وضعیت و ارجاع', {'fields': ('status', 'priority', 'assigned_to')}),
        ('منبع و زمان‌ها', {'fields': ('source_page', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'ip_address', 'user_agent', 'created_at', 'updated_at')}),
    )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def _change_status_action(self, request, queryset, new_status, message):
        for lead in queryset:
            lead.change_status(new_status, user=request.user)
        self.message_user(request, message)

    @admin.action(description='علامت زدن به عنوان تماس گرفته شده')
    def mark_contacted(self, request, queryset):
        self._change_status_action(request, queryset, 'contacted', 'وضعیت موارد انتخابی به تماس گرفته شد تغییر یافت.')

    @admin.action(description='علامت زدن به عنوان برنده')
    def mark_won(self, request, queryset):
        self._change_status_action(request, queryset, 'won', 'وضعیت موارد انتخابی به برنده تغییر یافت.')

    @admin.action(description='علامت زدن به عنوان از دست رفته')
    def mark_lost(self, request, queryset):
        self._change_status_action(request, queryset, 'lost', 'وضعیت موارد انتخابی به از دست رفته تغییر یافت.')

    @admin.action(description='خروجی CSV')
    def export_leads_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="leads.csv"'
        response.write('\ufeff'.encode('utf-8'))
        
        writer = csv.writer(response)
        writer.writerow(['full_name', 'phone', 'email', 'service_type', 'budget', 'status', 'priority', 'consent', 'source_page', 'created_at'])
        
        for lead in queryset:
            writer.writerow([
                lead.full_name, lead.phone, lead.email, lead.service_type, lead.budget,
                lead.status, lead.priority, lead.consent, lead.source_page, lead.created_at
            ])
        return response

@admin.register(LeadNote)
class LeadNoteAdmin(admin.ModelAdmin):
    list_display = ('lead', 'user', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(LeadLog)
class LeadLogAdmin(admin.ModelAdmin):
    list_display = ('lead', 'old_status', 'new_status', 'user', 'created_at')
    readonly_fields = ('lead', 'user', 'old_status', 'new_status', 'note', 'created_at')