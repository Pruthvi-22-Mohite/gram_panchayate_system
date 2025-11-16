from django.db import models


class EmergencyContact(models.Model):
    """
    Model to store emergency contact information for the village
    """
    CONTACT_TYPE_CHOICES = [
        ('police', 'Police'),
        ('hospital', 'Hospital'),
        ('fire_brigade', 'Fire Brigade'),
        ('electricity', 'Electricity Department'),
        ('water', 'Water Department'),
        ('sarpanch', 'Sarpanch'),
        ('talathi', 'Talathi'),
        ('ambulance', 'Ambulance'),
        ('disaster', 'Disaster Management'),
        ('others', 'Others'),
    ]
    
    contact_name = models.CharField(max_length=200, help_text="Contact name or organization")
    contact_type = models.CharField(
        max_length=50,
        choices=CONTACT_TYPE_CHOICES,
        help_text="Type of emergency service"
    )
    phone_number = models.CharField(max_length=20, help_text="Contact phone number")
    address = models.TextField(help_text="Complete address")
    email = models.EmailField(blank=True, null=True, help_text="Email address (optional)")
    available_24x7 = models.BooleanField(
        default=True,
        help_text="Is this service available 24x7?"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="Bootstrap icon class (e.g., bi-telephone-fill)"
    )
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Is this contact active?")
    
    class Meta:
        ordering = ['-last_updated']
        verbose_name = 'Emergency Contact'
        verbose_name_plural = 'Emergency Contacts'
    
    def __str__(self):
        return f"{self.contact_name} - {self.get_contact_type_display()}"
    
    def get_icon_class(self):
        """Return icon class or default based on contact type"""
        if self.icon:
            return self.icon
        
        icon_map = {
            'police': 'bi-shield-fill',
            'hospital': 'bi-hospital-fill',
            'fire_brigade': 'bi-fire',
            'electricity': 'bi-lightning-fill',
            'water': 'bi-droplet-fill',
            'sarpanch': 'bi-person-badge-fill',
            'talathi': 'bi-person-fill',
            'ambulance': 'bi-plus-square-fill',
            'disaster': 'bi-exclamation-triangle-fill',
            'others': 'bi-telephone-fill',
        }
        return icon_map.get(self.contact_type, 'bi-telephone-fill')
    
    def get_badge_class(self):
        """Return Bootstrap badge class based on contact type"""
        badge_map = {
            'police': 'bg-primary',
            'hospital': 'bg-danger',
            'fire_brigade': 'bg-warning',
            'electricity': 'bg-info',
            'water': 'bg-primary',
            'sarpanch': 'bg-success',
            'talathi': 'bg-secondary',
            'ambulance': 'bg-danger',
            'disaster': 'bg-warning',
            'others': 'bg-secondary',
        }
        return badge_map.get(self.contact_type, 'bg-secondary')
