from django.apps import AppConfig


class AdminModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.admin'
    verbose_name = 'Admin Module'
    label = 'admin_module'