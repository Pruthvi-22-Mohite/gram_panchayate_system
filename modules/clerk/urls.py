from django.urls import path
from . import views

app_name = 'clerk'

urlpatterns = [
    path('login/', views.clerk_login, name='login'),
    path('dashboard/', views.clerk_dashboard, name='dashboard'),
    path('schemes/', views.manage_schemes, name='manage_schemes'),
    path('schemes/add/', views.manage_schemes, name='add_scheme'),
    path('schemes/<int:scheme_id>/edit/', views.edit_scheme, name='edit_scheme'),
    path('schemes/<int:scheme_id>/delete/', views.delete_scheme, name='delete_scheme'),
    path('schemes/<int:scheme_id>/toggle-status/', views.toggle_scheme_status, name='toggle_scheme_status'),
    path('applications/', views.scheme_applications, name='scheme_applications'),
    path('applications/<int:application_id>/review/', views.review_application, name='review_application'),
    path('grievances/', views.manage_grievances, name='manage_grievances'),
    path('grievances/<int:grievance_id>/respond/', views.respond_grievance, name='respond_grievance'),
    path('taxes/', views.manage_taxes, name='manage_taxes'),
    path('reports/', views.reports, name='reports'),
    # Information Hub URLs
    path('notices/', views.manage_notices, name='manage_notices'),
    path('notices/<int:notice_id>/edit/', views.edit_notice, name='edit_notice'),
    path('notices/<int:notice_id>/delete/', views.delete_notice, name='delete_notice'),
    path('meetings/', views.manage_meetings, name='manage_meetings'),
    path('meetings/<int:meeting_id>/edit/', views.edit_meeting, name='edit_meeting'),
    path('meetings/<int:meeting_id>/delete/', views.delete_meeting, name='delete_meeting'),
]