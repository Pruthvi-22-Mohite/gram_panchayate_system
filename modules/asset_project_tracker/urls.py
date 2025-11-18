from django.urls import path
from . import views

app_name = 'asset_project_tracker'

urlpatterns = [
    # Public views
    path('', views.asset_project_list, name='list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('asset/<int:pk>/', views.asset_detail, name='asset_detail'),
    
    # Asset management
    path('manage/assets/', views.manage_assets, name='manage_assets'),
    path('manage/assets/add/', views.add_asset, name='add_asset'),
    path('manage/assets/<int:pk>/edit/', views.edit_asset, name='edit_asset'),
    path('manage/assets/<int:pk>/delete/', views.delete_asset, name='delete_asset'),
    
    # Project management
    path('manage/projects/', views.manage_projects, name='manage_projects'),
    path('manage/projects/add/', views.add_project, name='add_project'),
    path('manage/projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('manage/projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
]
