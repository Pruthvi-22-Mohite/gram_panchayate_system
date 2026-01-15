from django.urls import path, include

urlpatterns = [
    path('', include('modules.common.urls')),
    path('auth/', include('modules.common.auth_urls')),
    path('auth/admin-panel/', include('modules.admin.urls')),
    path('auth/clerk/', include('modules.clerk.urls')),
    path('auth/citizen/', include('modules.citizen.urls')),
    path('infohub/', include('modules.informationhub.urls')),
    path('emergency/', include('modules.emergencydirectory.urls')),
    path('budget/', include('modules.panchayat_budget.urls')),
    path('assets-projects/', include('modules.asset_project_tracker.urls')),
    path('tax/', include('tax_management.urls')),
]