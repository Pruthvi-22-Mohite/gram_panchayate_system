from django.urls import path
from . import views

app_name = 'panchayat_budget'

urlpatterns = [
    # URLs for budget entries with numeric fields
    path('entries/', views.public_budget_entry_list, name='budget_public_list'),
    path('entries/<int:pk>/', views.budget_entry_detail, name='budget_public_detail'),
    path('entries/manage/', views.budget_list, name='budget_list'),
    path('entries/add/', views.budget_add, name='budget_add'),
    path('entries/edit/<int:pk>/', views.budget_edit, name='budget_edit'),
    path('entries/delete/<int:pk>/', views.budget_delete, name='budget_delete'),
    
    # Admin/Clerk URLs to manage budget PDFs (specific paths first)
    path('manage/', views.manage_budget_pdfs, name='manage_budget_pdfs'),
    path('upload/', views.upload_budget_pdf, name='upload_budget_pdf'),
    path('edit/<str:financial_year>/', views.edit_budget_pdf, name='edit_budget_pdf'),
    path('delete/<str:financial_year>/', views.delete_budget_pdf, name='delete_budget_pdf'),
    
    # Citizen URLs to view budget PDFs
    path('citizen/', views.citizen_budget_list, name='citizen_budget_list'),
    path('citizen/<str:financial_year>/', views.budget_pdf_view, name='citizen_budget_pdf_view'),
    
    # Public URLs to view budget PDFs (most general last)
    path('', views.public_budget_list, name='public_budget_list'),
    path('<str:financial_year>/', views.budget_pdf_view, name='budget_pdf_view'),
]