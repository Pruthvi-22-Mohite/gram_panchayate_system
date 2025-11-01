from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('clerk-login/', views.clerk_login, name='clerk_login'),
    path('citizen-otp-request/', views.citizen_otp_request, name='citizen_otp_request'),
    path('citizen-otp-verify/', views.citizen_otp_verify, name='citizen_otp_verify'),
    path('citizen-aadhaar-otp-request/', views.citizen_aadhaar_otp_request, name='citizen_aadhaar_otp_request'),
    path('citizen-aadhaar-otp-verify/', views.citizen_aadhaar_otp_verify, name='citizen_aadhaar_otp_verify'),
    path('citizen-register/', views.citizen_registration, name='citizen_registration'),
    path('logout/', views.logout_view, name='logout'),
    path('citizen/dashboard/', views.citizen_dashboard, name='citizen_dashboard'),
    path('clerk/dashboard/', views.clerk_dashboard, name='clerk_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]