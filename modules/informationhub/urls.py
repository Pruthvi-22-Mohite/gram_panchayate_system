from django.urls import path
from . import views

app_name = 'informationhub'

urlpatterns = [
    # Village Notices URLs
    path('notices/', views.notices_list, name='notices_list'),
    path('notices/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    
    # Meeting Schedules URLs
    path('meetings/', views.meetings_list, name='meetings_list'),
    path('meetings/<int:meeting_id>/', views.meeting_detail, name='meeting_detail'),
]
