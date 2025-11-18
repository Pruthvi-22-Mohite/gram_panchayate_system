from django.db import models
from django.utils import timezone
from modules.common.models import CustomUser


class Asset(models.Model):
    """Model for tracking Gram Panchayat assets"""
    
    ASSET_TYPE_CHOICES = [
        ('infrastructure', 'Public Infrastructure'),
        ('property', 'Gram Panchayat Property'),
        ('vehicle', 'Vehicle'),
        ('equipment', 'Equipment'),
        ('furniture', 'Furniture'),
        ('other', 'Other'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('damaged', 'Damaged'),
    ]
    
    asset_name = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    ward_number = models.CharField(max_length=50, blank=True)
    
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    last_maintenance_date = models.DateField(blank=True, null=True)
    next_maintenance_date = models.DateField(blank=True, null=True)
    
    responsible_person = models.CharField(max_length=200, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    
    photo = models.ImageField(upload_to='assets/', blank=True, null=True)
    remarks = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='assets_created')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.asset_name} ({self.get_asset_type_display()})"
    
    def get_condition_badge_class(self):
        """Return Bootstrap badge class based on condition"""
        condition_classes = {
            'excellent': 'bg-success',
            'good': 'bg-primary',
            'fair': 'bg-warning',
            'poor': 'bg-danger',
            'damaged': 'bg-dark',
        }
        return condition_classes.get(self.condition, 'bg-secondary')


class Project(models.Model):
    """Model for tracking development projects"""
    
    PROJECT_TYPE_CHOICES = [
        ('road', 'Road Construction'),
        ('water', 'Water Supply'),
        ('sanitation', 'Sanitation'),
        ('building', 'Building Construction'),
        ('electricity', 'Electrification'),
        ('drainage', 'Drainage System'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('proposed', 'Proposed'),
        ('approved', 'Approved'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
        ('suspended', 'Suspended'),
    ]
    
    FUNDING_SOURCE_CHOICES = [
        ('central', 'Central Government'),
        ('state', 'State Government'),
        ('local', 'Local Funds'),
        ('mplads', 'MPLADS'),
        ('mgnrega', 'MGNREGA'),
        ('other', 'Other'),
    ]
    
    project_name = models.CharField(max_length=300)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    ward_number = models.CharField(max_length=50, blank=True)
    
    budget_allocated = models.DecimalField(max_digits=12, decimal_places=2)
    budget_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    funding_source = models.CharField(max_length=20, choices=FUNDING_SOURCE_CHOICES)
    
    start_date = models.DateField()
    target_completion_date = models.DateField()
    actual_completion_date = models.DateField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='proposed')
    progress_percentage = models.IntegerField(default=0)
    
    contractor_name = models.CharField(max_length=200, blank=True)
    contractor_contact = models.CharField(max_length=15, blank=True)
    
    beneficiaries_count = models.IntegerField(default=0)
    
    photo = models.ImageField(upload_to='projects/', blank=True, null=True)
    document = models.FileField(upload_to='project_docs/', blank=True, null=True)
    
    remarks = models.TextField(blank=True)
    
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='projects_created')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project_name} ({self.get_status_display()})"
    
    def get_status_badge_class(self):
        """Return Bootstrap badge class based on status"""
        status_classes = {
            'proposed': 'bg-secondary',
            'approved': 'bg-info',
            'ongoing': 'bg-primary',
            'completed': 'bg-success',
            'delayed': 'bg-warning',
            'suspended': 'bg-danger',
        }
        return status_classes.get(self.status, 'bg-secondary')
    
    def get_budget_utilization_percentage(self):
        """Calculate budget utilization percentage"""
        if self.budget_allocated > 0:
            return round((self.budget_spent / self.budget_allocated) * 100, 2)
        return 0
    
    def is_delayed(self):
        """Check if project is delayed"""
        if self.status == 'ongoing' and self.target_completion_date < timezone.now().date():
            return True
        return False
