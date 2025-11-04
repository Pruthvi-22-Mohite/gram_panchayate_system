from django.urls import path
from . import views

app_name = 'clerk'

urlpatterns = [
    path('login/', views.clerk_login, name='login'),
    path('dashboard/', views.clerk_dashboard, name='dashboard'),
    path('schemes/', views.manage_schemes, name='manage_schemes'),
    path('applications/', views.scheme_applications, name='scheme_applications'),
    path('applications/<int:application_id>/review/', views.review_application, name='review_application'),
    path('grievances/', views.manage_grievances, name='manage_grievances'),
    path('grievances/<int:grievance_id>/respond/', views.respond_grievance, name='respond_grievance'),
    path('taxes/', views.manage_taxes, name='manage_taxes'),
    path('reports/', views.reports, name='reports'),
]