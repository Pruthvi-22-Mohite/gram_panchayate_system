from django.db import models
from django.utils import timezone
from modules.common.models import CustomUser


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


class Scheme(models.Model):
    """
    Model for government schemes managed by clerks
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    eligibility_criteria = models.TextField()
    required_documents = models.TextField()
    benefits = models.TextField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class SchemeApplication(models.Model):
    """
    Model for citizen applications to schemes
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE)
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    application_data = models.JSONField()  # Store form data as JSON
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='reviewed_applications'
    )
    review_notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.applicant.username} - {self.scheme.name}"


class Grievance(models.Model):
    """
    Model for citizen grievances handled by clerks
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    photo = models.ImageField(upload_to='grievance_photos/', null=True, blank=True)
    
    submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_grievances'
    )
    
    submitted_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.status}"


class TaxRecord(models.Model):
    """
    Model for tax records managed by clerks
    """
    TAX_TYPES = [
        ('property', 'Property Tax'),
        ('water', 'Water Tax'),
        ('trade', 'Trade License Fee'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    
    taxpayer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tax_type = models.CharField(max_length=20, choices=TAX_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    created_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='created_tax_records'
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.taxpayer.username} - {self.tax_type} - ₹{self.amount}"