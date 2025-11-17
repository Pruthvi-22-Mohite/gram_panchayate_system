from django.contrib import admin
from .models import PanchayatBudget


@admin.register(PanchayatBudget)
class PanchayatBudgetAdmin(admin.ModelAdmin):
    """Admin configuration for PanchayatBudget model"""
    
    list_display = [
        'id',
        'budget_head',
        'previous_year_amount',
        'revenue_income',
        'revenue_collection',
        'expenditure_spent',
        'total_amount',
        'created_at'
    ]
    
    list_filter = [
        'budget_head',
        'created_at'
    ]
    
    search_fields = [
        'budget_head'
    ]
    
    readonly_fields = [
        'total_amount',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        ('Budget Information', {
            'fields': (
                'budget_head',
                'previous_year_amount',
                'revenue_income',
                'revenue_collection',
                'expenditure_allotted',
                'expenditure_spent',
                'total_amount'
            )
        }),
        ('Supporting Documents', {
            'fields': (
                'document',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        """Only allow admin users to add budget entries"""
        return request.user.user_type in ['ADMIN']
    
    def has_change_permission(self, request, obj=None):
        """Only allow admin and clerk users to change budget entries"""
        return request.user.user_type in ['ADMIN', 'CLERK']
    
    def has_delete_permission(self, request, obj=None):
        """Only allow admin and clerk users to delete budget entries"""
        return request.user.user_type in ['ADMIN', 'CLERK']