from django.contrib import admin
from .models import EmergencyContact


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for Emergency Contacts
    """
    list_display = [
        'contact_name',
        'contact_type',
        'phone_number',
        'available_24x7',
        'is_active',
        'last_updated'
    ]
    
    list_filter = ['contact_type', 'available_24x7', 'is_active', 'created_at']
    
    search_fields = ['contact_name', 'phone_number', 'address', 'email']
    
    ordering = ['-last_updated']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('contact_name', 'contact_type', 'phone_number')
        }),
        ('Address & Email', {
            'fields': ('address', 'email')
        }),
        ('Availability & Status', {
            'fields': ('available_24x7', 'is_active', 'icon')
        }),
    )
    
    readonly_fields = []
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields readonly when editing"""
        if obj:  # Editing existing object
            return self.readonly_fields
        return self.readonly_fields
