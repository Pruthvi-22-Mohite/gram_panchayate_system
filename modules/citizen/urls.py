from django.urls import path
from . import views

app_name = 'citizen'

urlpatterns = [
    path('login/', views.citizen_login, name='login'),
    path('register/', views.citizen_registration, name='register'),
    path('dashboard/', views.citizen_dashboard, name='dashboard'),
    path('schemes/', views.view_schemes, name='view_schemes'),
    path('schemes/<int:scheme_id>/', views.scheme_detail, name='scheme_detail'),
    path('schemes/<int:scheme_id>/apply/', views.apply_scheme, name='apply_scheme'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('lodge-grievance/', views.lodge_grievance, name='lodge_grievance'),
    path('my-grievances/', views.my_grievances, name='my_grievances'),
    path('pay-tax/', views.pay_tax, name='pay_tax'),
    path('view-budget/', views.view_budget, name='view_budget'),
    path('emergency-directory/', views.emergency_directory, name='emergency_directory'),
    path('feedback-suggestions/', views.feedback_suggestions, name='feedback_suggestions'),
    path('my-documents/', views.my_documents, name='my_documents'),
]