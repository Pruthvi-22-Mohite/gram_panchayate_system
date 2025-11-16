from django.urls import path
from . import views

app_name = 'certificates_rti'

urlpatterns = [
    # ===========================
    # CITIZEN URLS - CERTIFICATES
    # ===========================
    path('citizen/certificates/', views.citizen_certificate_list, name='citizen_certificate_list'),
    path('citizen/certificates/apply/', views.citizen_certificate_apply, name='citizen_certificate_apply'),
    path('citizen/certificates/<int:pk>/', views.citizen_certificate_detail, name='citizen_certificate_detail'),
    path('citizen/certificates/<int:pk>/download/', views.citizen_certificate_download, name='citizen_certificate_download'),
    
    # ===========================
    # CITIZEN URLS - RTI
    # ===========================
    path('citizen/rti/', views.citizen_rti_list, name='citizen_rti_list'),
    path('citizen/rti/submit/', views.citizen_rti_submit, name='citizen_rti_submit'),
    path('citizen/rti/<int:pk>/', views.citizen_rti_detail, name='citizen_rti_detail'),
    path('citizen/rti/<int:pk>/download/', views.citizen_rti_download_response, name='citizen_rti_download_response'),
    
    # ===========================
    # CITIZEN URLS - LAND RECORDS
    # ===========================
    path('citizen/land-records/', views.citizen_land_search, name='citizen_land_search'),
    path('citizen/land-records/link/', views.citizen_land_link_request, name='citizen_land_link_request'),
    path('citizen/land-records/link/<str:property_id>/', views.citizen_land_link_request, name='citizen_land_link_request_id'),
    path('citizen/land-records/status/', views.citizen_land_status, name='citizen_land_status'),
    
    # ===========================
    # CLERK URLS - CERTIFICATES
    # ===========================
    path('clerk/certificates/', views.clerk_certificate_list, name='clerk_certificate_list'),
    path('clerk/certificates/<int:pk>/', views.clerk_certificate_detail, name='clerk_certificate_detail'),
    path('clerk/certificates/<int:pk>/upload/', views.clerk_certificate_upload, name='clerk_certificate_upload'),
    
    # ===========================
    # CLERK URLS - RTI
    # ===========================
    path('clerk/rti/', views.clerk_rti_list, name='clerk_rti_list'),
    path('clerk/rti/<int:pk>/', views.clerk_rti_detail, name='clerk_rti_detail'),
    path('clerk/rti/<int:pk>/upload-response/', views.clerk_rti_upload_response, name='clerk_rti_upload_response'),
    
    # ===========================
    # CLERK URLS - LAND RECORDS
    # ===========================
    path('clerk/land-records/', views.clerk_land_list, name='clerk_land_list'),
    path('clerk/land-records/<int:pk>/', views.clerk_land_detail, name='clerk_land_detail'),
    
    # ===========================
    # ADMIN URLS - CERTIFICATES
    # ===========================
    path('admin-panel/certificates/', views.admin_certificate_list, name='admin_certificate_list'),
    path('admin-panel/certificates/<int:pk>/', views.admin_certificate_detail, name='admin_certificate_detail'),
    
    # ===========================
    # ADMIN URLS - RTI
    # ===========================
    path('admin-panel/rti/', views.admin_rti_list, name='admin_rti_list'),
    path('admin-panel/rti/<int:pk>/', views.admin_rti_detail, name='admin_rti_detail'),
    
    # ===========================
    # ADMIN URLS - LAND RECORDS
    # ===========================
    path('admin-panel/land-records/', views.admin_land_list, name='admin_land_list'),
    path('admin-panel/land-records/<int:pk>/', views.admin_land_detail, name='admin_land_detail'),
]
