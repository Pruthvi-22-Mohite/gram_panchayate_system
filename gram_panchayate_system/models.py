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

class AdminProfile(models.Model):
    """
    Profile model for Admin users
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    designation = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Admin Profile: {self.user.username}"

class ClerkProfile(models.Model):
    """
    Profile model for Clerk users
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    panchayat_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"Clerk Profile: {self.user.username} - {self.panchayat_name}"

class CitizenProfile(models.Model):
    """
    Profile model for Citizen users
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Citizen Profile: {self.user.username}"

class OTP(models.Model):
    """
    Model to store OTP for citizen login
    """
    mobile_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        """
        Check if OTP is expired (valid for 10 minutes)
        """
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)
    
    def __str__(self):
        return f"OTP for {self.mobile_number}: {self.otp}"