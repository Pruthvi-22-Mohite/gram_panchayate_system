from django.urls import path
from . import views

app_name = 'emergencydirectory'

urlpatterns = [
    # Public citizen views
    path('', views.emergency_list, name='emergency_list'),
    path('<int:contact_id>/', views.emergency_detail, name='emergency_detail'),
    
    # Admin/Clerk management views (protected)
    path('manage/', views.manage_contacts, name='manage_contacts'),
    path('add/', views.add_contact, name='add_contact'),
    path('edit/<int:contact_id>/', views.edit_contact, name='edit_contact'),
    path('delete/<int:contact_id>/', views.delete_contact, name='delete_contact'),
]
