from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('switch-language/', views.switch_language, name='switch_language'),
    path('change-password/', views.change_password, name='change_password'),
]