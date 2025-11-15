from django.db import models
from modules.common.models import CustomUser


class AdminProfile(models.Model):
    """
    Profile model for Admin users
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    designation = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Admin Profile: {self.user.username}"


class SystemSettings(models.Model):
    """
    Model for system-wide settings managed by admin
    """
    setting_key = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.setting_key}: {self.setting_value}"


class AuditLog(models.Model):
    """
    Model for tracking admin actions and system changes
    """
    admin_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    target_model = models.CharField(max_length=100, blank=True)
    target_id = models.CharField(max_length=100, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.admin_user.username} - {self.action} at {self.timestamp}"