from django.contrib import admin
from .models import PanchayatBudget


@admin.register(PanchayatBudget)
class PanchayatBudgetAdmin(admin.ModelAdmin):
    """Admin configuration for PanchayatBudget model"""
    
    list_display = [
        'financial_year',
        'title',
        'uploaded_by',
        'uploaded_at'
    ]
    
    list_filter = [
        'financial_year',
        'uploaded_at'
    ]
    
    search_fields = [
        'title',
        'financial_year'
    ]
    
    readonly_fields = [
        'uploaded_at'
    ]
    
    fieldsets = (
        ('Budget Information', {
            'fields': (
                'financial_year',
                'title',
                'description',
                'pdf_file'
            )
        }),
        ('Metadata', {
            'fields': (
                'uploaded_by',
                'uploaded_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        """Only allow admin users to add budget entries"""
        return request.user.is_superuser or request.user.user_type == 'clerk'
    
    def has_change_permission(self, request, obj=None):
        """Only allow admin and clerk users to change budget entries"""
        return request.user.is_superuser or request.user.user_type == 'clerk'
    
    def has_delete_permission(self, request, obj=None):
        """Only allow admin and clerk users to delete budget entries"""
        return request.user.is_superuser or request.user.user_type == 'clerk'