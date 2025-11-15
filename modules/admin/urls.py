from django.urls import path
from . import views

app_name = 'admin_module'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('clerks/', views.manage_clerks, name='manage_clerks'),
    path('clerks/create/', views.create_clerk, name='create_clerk'),
    path('citizens/', views.manage_citizens, name='manage_citizens'),
    path('settings/', views.system_settings, name='system_settings'),
    path('audit-logs/', views.audit_logs, name='audit_logs'),
    path('reports/', views.reports, name='reports'),
    path('grievances/', views.manage_grievances, name='manage_grievances'),
]