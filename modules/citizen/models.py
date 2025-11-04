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
        ('feedback', 'Feedback'),
        ('suggestion', 'Suggestion'),
        ('complaint', 'Complaint'),
    ]
    
    citizen = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)
    is_anonymous = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.feedback_type}: {self.subject}"


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