from django.db import models
from django.conf import settings
from django.utils import timezone


class CertificateApplication(models.Model):
    """Model for certificate applications submitted by citizens"""
    
    CERTIFICATE_TYPES = [
        ('birth', 'Birth Certificate'),
        ('death', 'Death Certificate'),
        ('income', 'Income Certificate'),
        ('caste', 'Caste Certificate'),
        ('residence', 'Residence Certificate'),
        ('marriage', 'Marriage Certificate'),
        ('farmer', 'Farmer Certificate'),
        ('senior_citizen', 'Senior Citizen Certificate'),
        ('bpl', 'BPL Certificate'),
    ]
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificate_applications')
    certificate_type = models.CharField(max_length=20, choices=CERTIFICATE_TYPES)
    full_name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    mother_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    aadhar = models.CharField(max_length=12)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    remarks = models.TextField(blank=True, null=True)
    assigned_clerk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_certificates')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_certificate_type_display()} - {self.full_name}"


class CertificateDocument(models.Model):
    """Supporting documents for certificate applications"""
    application = models.ForeignKey(CertificateApplication, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='certificates/documents/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Document for {self.application}"


class ApprovedCertificate(models.Model):
    """Final approved certificate PDFs"""
    application = models.OneToOneField(CertificateApplication, on_delete=models.CASCADE, related_name='approved_certificate')
    certificate_number = models.CharField(max_length=50, unique=True)
    certificate_file = models.FileField(upload_to='certificates/approved/')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    approved_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Certificate {self.certificate_number}"


class RTIRequest(models.Model):
    """RTI (Right to Information) requests"""
    
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('sc', 'Scheduled Caste'),
        ('st', 'Scheduled Tribe'),
        ('obc', 'Other Backward Class'),
        ('bpl', 'Below Poverty Line'),
    ]
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('responded', 'Responded'),
        ('rejected', 'Rejected'),
    ]
    
    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rti_requests')
    subject = models.CharField(max_length=500)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    address = models.TextField()
    supporting_doc = models.FileField(upload_to='rti/supporting/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    response_file = models.FileField(upload_to='rti/responses/', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    assigned_clerk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_rtis')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"RTI: {self.subject[:50]}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validate required fields
        if not self.subject or not self.subject.strip():
            raise ValidationError({'subject': 'Subject is required.'})
        
        if not self.description or not self.description.strip():
            raise ValidationError({'description': 'Description is required.'})
        
        if not self.category:
            raise ValidationError({'category': 'Category is required.'})
        
        if not self.address or not self.address.strip():
            raise ValidationError({'address': 'Address is required.'})


class LandRecordLink(models.Model):
    """Land record linking requests"""
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='land_records')
    survey_number = models.CharField(max_length=100)
    gat_number = models.CharField(max_length=100)
    property_id = models.CharField(max_length=100, blank=True, null=True)
    ownership_proof = models.FileField(upload_to='land_records/proof/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    remarks = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_land_records')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Land Record - Survey: {self.survey_number}, Gat: {self.gat_number}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validate required fields
        if not self.survey_number or not self.survey_number.strip():
            raise ValidationError({'survey_number': 'Survey Number is required.'})
        
        if not self.gat_number or not self.gat_number.strip():
            raise ValidationError({'gat_number': 'Gat Number is required.'})
        
        # Validate that numeric fields are non-negative
        if self.area < 0:
            raise ValidationError({'area': 'Negative values are not allowed.'})


class LandParcel(models.Model):
    """Dummy land parcel database for search"""
    survey_number = models.CharField(max_length=100)
    gat_number = models.CharField(max_length=100)
    property_id = models.CharField(max_length=100, unique=True)
    area = models.DecimalField(max_digits=10, decimal_places=2)  # in acres
    location = models.CharField(max_length=500)
    ownership_type = models.CharField(max_length=50, default='Private')
    
    def __str__(self):
        return f"{self.property_id} - Survey: {self.survey_number}"
