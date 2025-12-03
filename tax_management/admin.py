from django.contrib import admin
from .models import CitizenTaxData

@admin.register(CitizenTaxData)
class CitizenTaxDataAdmin(admin.ModelAdmin):
    list_display = (
        'aadhaar_number',
        'property_tax_amount',
        'property_due_date',
        'property_status',
        'water_tax_amount',
        'water_due_date',
        'water_status',
        'garbage_tax_amount',
        'garbage_due_date',
        'garbage_status',
        'health_tax_amount',
        'health_due_date',
        'health_status',
        'updated_at'
    )
    
    list_filter = (
        'property_status',
        'water_status',
        'garbage_status',
        'health_status',
        'updated_at'
    )
    
    search_fields = ('aadhaar_number',)
    
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Citizen Information', {
            'fields': ('aadhaar_number',)
        }),
        ('Property Tax', {
            'fields': (
                'property_tax_amount',
                'property_due_date',
                'property_penalty',
                'property_status'
            )
        }),
        ('Water Tax', {
            'fields': (
                'water_tax_amount',
                'water_due_date',
                'water_penalty',
                'water_status'
            )
        }),
        ('Garbage Tax', {
            'fields': (
                'garbage_tax_amount',
                'garbage_due_date',
                'garbage_penalty',
                'garbage_status'
            )
        }),
        ('Health Tax', {
            'fields': (
                'health_tax_amount',
                'health_due_date',
                'health_penalty',
                'health_status'
            )
        }),
        ('Metadata', {
            'fields': ('updated_at',)
        }),
    )