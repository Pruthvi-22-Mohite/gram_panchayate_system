from django.apps import AppConfig

class TaxManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tax_management'
    
    def ready(self):
        # Import signals or other initialization code here if needed
        pass