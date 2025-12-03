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
    # Removed system settings URL
    path('audit-logs/', views.audit_logs, name='audit_logs'),
    path('reports/', views.reports, name='reports'),
    path('reports/data/', views.reports_data, name='reports_data'),
    path('grievances/', views.manage_grievances, name='manage_grievances'),
    path('schemes/', views.manage_schemes, name='manage_schemes'),
    path('schemes/<int:scheme_id>/edit/', views.edit_scheme, name='edit_scheme'),
    path('schemes/<int:scheme_id>/delete/', views.delete_scheme, name='delete_scheme'),
    path('schemes/<int:scheme_id>/toggle-status/', views.toggle_scheme_status, name='toggle_scheme_status'),
    # Information Hub URLs
    path('notices/', views.manage_notices, name='manage_notices'),
    path('notices/<int:notice_id>/edit/', views.edit_notice, name='edit_notice'),
    path('notices/<int:notice_id>/delete/', views.delete_notice, name='delete_notice'),
    path('meetings/', views.manage_meetings, name='manage_meetings'),
    path('meetings/<int:meeting_id>/edit/', views.edit_meeting, name='edit_meeting'),
    path('meetings/<int:meeting_id>/delete/', views.delete_meeting, name='delete_meeting'),
    # Feedback & Suggestions URLs
    path('feedback/', views.manage_feedback, name='manage_feedback'),
    path('feedback/<int:feedback_id>/', views.feedback_detail, name='feedback_detail'),
    path('feedback/<int:feedback_id>/delete/', views.delete_feedback, name='delete_feedback'),
]