from django.urls import path, include

urlpatterns = [
    path('', include('modules.common.urls')),
    path('admin-panel/', include('modules.admin.urls')),
    path('clerk/', include('modules.clerk.urls')),
    path('citizen/', include('modules.citizen.urls')),
    path('infohub/', include('modules.informationhub.urls')),
    path('emergency/', include('modules.emergencydirectory.urls')),
]