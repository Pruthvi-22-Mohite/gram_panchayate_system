from django.urls import path
from . import views

app_name = 'tax_management'

urlpatterns = [
    # Citizen URLs
    path('citizen/bills/', views.citizen_tax_bills, name='citizen_tax_bills'),
    
    # Admin URLs
    path('admin/excel-upload/', views.admin_excel_upload, name='admin_excel_upload'),
    
    # Clerk URLs
    path('clerk/excel-upload/', views.clerk_excel_upload, name='clerk_excel_upload'),
]