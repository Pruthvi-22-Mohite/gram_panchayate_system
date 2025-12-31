from django.db import models
from django.utils import timezone
from modules.common.models import CustomUser


class ClerkProfile(models.Model):
    """
    Profile model for Clerk users
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    panchayat_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)  # Required field
    employee_id = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"Clerk Profile: {self.user.username} - {self.panchayat_name}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.designation and not self.designation.strip():
            raise ValidationError({'designation': 'Designation is required.'})
        
        # Additional validations for related CustomUser fields
        if self.user.first_name and not self.user.first_name.replace(' ', '').isalpha():
            raise ValidationError({'first_name': 'First name must contain only alphabets.'})
        
        if self.user.last_name and not self.user.last_name.replace(' ', '').isalpha():
            raise ValidationError({'last_name': 'Last name must contain only alphabets.'})
        
        # Validate mobile number format
        if self.user.mobile_number:
            mobile_number_clean = self.user.mobile_number.replace(' ', '').replace('-', '')
            if len(mobile_number_clean) != 10 or not mobile_number_clean.isdigit():
                raise ValidationError({'mobile_number': 'Mobile number must be exactly 10 digits.'})


class Scheme(models.Model):
    """
    Model for government schemes managed by clerks
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    eligibility_criteria = models.TextField()
    required_documents = models.TextField()
    benefits = models.TextField()
    application_process = models.TextField(blank=True)
    last_date = models.DateField(null=True, blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    downloadable_forms = models.FileField(upload_to='scheme_forms/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    scheme_image = models.ImageField(upload_to='scheme_images/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def clean(self):
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        if not self.application_process or not self.application_process.strip():
            raise ValidationError({'application_process': 'Application process cannot be empty.'})
        
        if self.last_date and self.last_date < timezone.now().date():
            raise ValidationError({'last_date': 'Last date cannot be in the past.'})
        
        if not self.contact_person or not self.contact_person.strip():
            raise ValidationError({'contact_person': 'Contact person cannot be empty.'})


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
        ('garbage', 'Garbage Tax'),
        ('health', 'Health Tax'),
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
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validate that numeric fields are non-negative
        if self.amount < 0:
            raise ValidationError({'amount': 'Negative values are not allowed.'})