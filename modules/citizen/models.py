from django.db import models
from django.utils import timezone
from modules.common.models import CustomUser


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


class CitizenDocument(models.Model):
    """
    Model for storing citizen documents
    """
    DOCUMENT_TYPES = [
        ('aadhaar', 'Aadhaar Card'),
        ('pan', 'PAN Card'),
        ('voter_id', 'Voter ID'),
        ('ration_card', 'Ration Card'),
        ('income_certificate', 'Income Certificate'),
        ('caste_certificate', 'Caste Certificate'),
        ('other', 'Other'),
    ]
    
    citizen = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=50, blank=True)
    document_file = models.FileField(upload_to='citizen_documents/', null=True, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.citizen.username} - {self.document_type}"


class FeedbackSuggestion(models.Model):
    """
    Model for citizen feedback and suggestions
    """
    FEEDBACK_TYPES = [
        ('suggestion', 'Suggestion'),
        ('complaint', 'Complaint'),
        ('query', 'Query'),
        ('appreciation', 'Appreciation'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]
    
    citizen = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    attachment = models.FileField(upload_to='feedback_attachments/', blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_response = models.TextField(blank=True, null=True)
    responded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_responses')
    responded_at = models.DateTimeField(null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Feedback/Suggestion'
        verbose_name_plural = 'Feedback/Suggestions'
    
    def __str__(self):
        return f"{self.get_feedback_type_display()}: {self.subject}"
    
    def get_status_badge_class(self):
        badge_map = {
            'pending': 'bg-warning',
            'reviewed': 'bg-info',
            'resolved': 'bg-success',
        }
        return badge_map.get(self.status, 'bg-secondary')


class EmergencyContact(models.Model):
    """
    Model for emergency contacts directory
    """
    CONTACT_TYPES = [
        ('police', 'Police'),
        ('fire', 'Fire Department'),
        ('medical', 'Medical Emergency'),
        ('ambulance', 'Ambulance'),
        ('hospital', 'Hospital'),
        ('panchayat', 'Panchayat Office'),
        ('other', 'Other'),
    ]
    
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} - {self.contact_type}"


class BudgetItem(models.Model):
    """
    Model for panchayat budget items (read-only for citizens)
    """
    BUDGET_CATEGORIES = [
        ('development', 'Development Works'),
        ('infrastructure', 'Infrastructure'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('sanitation', 'Sanitation'),
        ('water', 'Water Supply'),
        ('roads', 'Roads'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=20, choices=BUDGET_CATEGORIES)
    item_name = models.CharField(max_length=200)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    financial_year = models.CharField(max_length=10)  # e.g., "2023-24"
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.item_name} - {self.financial_year}"
    
    @property
    def remaining_amount(self):
        return self.allocated_amount - self.spent_amount
    
    @property
    def utilization_percentage(self):
        if self.allocated_amount > 0:
            return (self.spent_amount / self.allocated_amount) * 100
        return 0