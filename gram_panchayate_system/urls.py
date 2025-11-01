"""
URL configuration for gram_panchayate_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gram_panchayate_system import views

urlpatterns = [
    path('django-admin/', admin.site.urls),  # Changed from 'admin/' to 'django-admin/'
    path('', views.home, name='home'),
    path('auth/', include('authentication.urls')),  # Include authentication URLs
    path('pay-tax/', views.pay_tax, name='pay_tax'),
    path('lodge-grievance/', views.lodge_grievance, name='lodge_grievance'),
    path('view-schemes/', views.view_schemes, name='view_schemes'),
    path('emergency-directory/', views.emergency_directory, name='emergency_directory'),
    path('feedback-suggestions/', views.feedback_suggestions, name='feedback_suggestions'),
    path('view-budget/', views.view_budget, name='view_budget'),
    path('api/send-otp/', views.send_otp_api, name='send_otp_api'),
]