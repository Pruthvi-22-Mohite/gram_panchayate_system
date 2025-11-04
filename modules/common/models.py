from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser
    Adds user type field to distinguish between Admin, Clerk, and Citizen
    """
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('clerk', 'Clerk'),
        ('citizen', 'Citizen'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='citizen')
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"


class BaseModel(models.Model):
    """
    Abstract base model with common fields
    """
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Notification(models.Model):
    """
    Model for system notifications
    """
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class SystemConfiguration(models.Model):
    """
    Model for system-wide configuration
    """
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.key}: {self.value}"