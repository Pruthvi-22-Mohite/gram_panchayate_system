from django.contrib import admin
from .models import (
    CertificateApplication, CertificateDocument, ApprovedCertificate,
    RTIRequest, LandRecordLink, LandParcel
)


@admin.register(CertificateApplication)
class CertificateApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'certificate_type', 'full_name', 'citizen', 'status', 'created_at']
    list_filter = ['status', 'certificate_type', 'created_at']
    search_fields = ['full_name', 'father_name', 'aadhar', 'citizen__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('citizen', 'certificate_type', 'full_name', 'father_name', 'mother_name')
        }),
        ('Contact Details', {
            'fields': ('address', 'phone', 'aadhar')
        }),
        ('Application Details', {
            'fields': ('reason', 'status', 'remarks', 'assigned_clerk')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CertificateDocument)
class CertificateDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'application', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['application__full_name']
    readonly_fields = ['uploaded_at']


@admin.register(ApprovedCertificate)
class ApprovedCertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_number', 'application', 'approved_by', 'approved_at']
    list_filter = ['approved_at']
    search_fields = ['certificate_number', 'application__full_name']
    readonly_fields = ['approved_at']


@admin.register(RTIRequest)
class RTIRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'citizen', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['subject', 'description', 'citizen__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Request Information', {
            'fields': ('citizen', 'subject', 'description', 'category', 'address')
        }),
        ('Documents', {
            'fields': ('supporting_doc', 'response_file')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'remarks', 'assigned_clerk')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LandRecordLink)
class LandRecordLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'citizen', 'survey_number', 'gat_number', 'property_id', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['survey_number', 'gat_number', 'property_id', 'citizen__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Land Details', {
            'fields': ('citizen', 'survey_number', 'gat_number', 'property_id')
        }),
        ('Verification', {
            'fields': ('ownership_proof', 'status', 'remarks', 'verified_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LandParcel)
class LandParcelAdmin(admin.ModelAdmin):
    list_display = ['property_id', 'survey_number', 'gat_number', 'area', 'location', 'ownership_type']
    list_filter = ['ownership_type']
    search_fields = ['property_id', 'survey_number', 'gat_number', 'location']
    
    fieldsets = (
        ('Parcel Identification', {
            'fields': ('property_id', 'survey_number', 'gat_number')
        }),
        ('Parcel Details', {
            'fields': ('area', 'location', 'ownership_type')
        }),
    )
