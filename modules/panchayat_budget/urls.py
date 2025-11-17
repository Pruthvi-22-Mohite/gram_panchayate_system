from django.urls import path
from . import views

app_name = 'panchayat_budget'

urlpatterns = [
    # Admin/Clerk URLs
    path('admin-panel/', views.budget_list, name='budget_list'),
    path('admin-panel/add/', views.budget_add, name='budget_add'),
    path('admin-panel/<int:pk>/edit/', views.budget_edit, name='budget_edit'),
    path('admin-panel/<int:pk>/delete/', views.budget_delete, name='budget_delete'),
    path('admin-panel/<int:pk>/', views.budget_detail, name='budget_detail'),
    
    # Clerk URLs (same as admin for now)
    path('clerk/', views.budget_list, name='clerk_budget_list'),
    path('clerk/add/', views.budget_add, name='clerk_budget_add'),
    path('clerk/<int:pk>/edit/', views.budget_edit, name='clerk_budget_edit'),
    path('clerk/<int:pk>/', views.budget_detail, name='clerk_budget_detail'),
    
    # Citizen URLs
    path('citizen/', views.budget_public_list, name='budget_public_list'),
    path('citizen/<int:pk>/', views.budget_public_detail, name='budget_public_detail'),
]