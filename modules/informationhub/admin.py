from django.contrib import admin
from .models import VillageNotice, MeetingSchedule


@admin.register(VillageNotice)
class VillageNoticeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Village Notices
    """
    list_display = ['title', 'notice_type', 'issued_by', 'date', 'is_active', 'created_at']
    list_filter = ['notice_type', 'is_active', 'date', 'issued_by']
    search_fields = ['title', 'description', 'issued_by']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    
    fieldsets = (
        ('Notice Information', {
            'fields': ('title', 'description', 'notice_type')
        }),
        ('Issuance Details', {
            'fields': ('issued_by', 'date', 'attachment')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = []
    
    def get_readonly_fields(self, request, obj=None):
        """Make created_at and updated_at readonly if needed"""
        if obj:  # Editing an existing object
            return self.readonly_fields + []
        return self.readonly_fields


@admin.register(MeetingSchedule)
class MeetingScheduleAdmin(admin.ModelAdmin):
    """
    Admin configuration for Meeting Schedules
    """
    list_display = ['meeting_title', 'meeting_date', 'time', 'location', 'organized_by', 'is_cancelled']
    list_filter = ['is_cancelled', 'meeting_date', 'organized_by']
    search_fields = ['meeting_title', 'agenda', 'location', 'organized_by']
    date_hierarchy = 'meeting_date'
    ordering = ['-meeting_date', 'time']
    
    fieldsets = (
        ('Meeting Information', {
            'fields': ('meeting_title', 'agenda')
        }),
        ('Schedule Details', {
            'fields': ('meeting_date', 'time', 'location')
        }),
        ('Organization', {
            'fields': ('organized_by', 'is_cancelled')
        }),
    )
    
    def get_queryset(self, request):
        """Customize queryset if needed"""
        qs = super().get_queryset(request)
        return qs
