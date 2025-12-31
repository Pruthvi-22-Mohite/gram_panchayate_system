from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class CitizenTaxData(models.Model):
    """
    Model for storing citizen tax data based on Aadhaar number
    """
    # Primary key - Aadhaar number
    aadhaar_number = models.CharField(max_length=12, primary_key=True)
    
    # Property Tax
    property_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    property_due_date = models.DateField(null=True, blank=True)
    property_penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    property_status = models.CharField(max_length=10, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
    ], default='pending')
    
    # Water Tax
    water_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    water_due_date = models.DateField(null=True, blank=True)
    water_penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    water_status = models.CharField(max_length=10, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
    ], default='pending')
    
    # Garbage Tax
    garbage_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    garbage_due_date = models.DateField(null=True, blank=True)
    garbage_penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    garbage_status = models.CharField(max_length=10, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
    ], default='pending')
    
    # Health Tax
    health_tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    health_due_date = models.DateField(null=True, blank=True)
    health_penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    health_status = models.CharField(max_length=10, choices=[
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
    ], default='pending')
    
    # Metadata
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Citizen Tax Data - {self.aadhaar_number}"
    
    def clean(self):
        # Validate that all tax amounts and penalties are non-negative
        if self.property_tax_amount is not None and self.property_tax_amount < 0:
            raise ValidationError({'property_tax_amount': 'Negative values are not allowed.'})
        if self.property_penalty < 0:
            raise ValidationError({'property_penalty': 'Negative values are not allowed.'})
        
        if self.water_tax_amount is not None and self.water_tax_amount < 0:
            raise ValidationError({'water_tax_amount': 'Negative values are not allowed.'})
        if self.water_penalty < 0:
            raise ValidationError({'water_penalty': 'Negative values are not allowed.'})
        
        if self.garbage_tax_amount is not None and self.garbage_tax_amount < 0:
            raise ValidationError({'garbage_tax_amount': 'Negative values are not allowed.'})
        if self.garbage_penalty < 0:
            raise ValidationError({'garbage_penalty': 'Negative values are not allowed.'})
        
        if self.health_tax_amount is not None and self.health_tax_amount < 0:
            raise ValidationError({'health_tax_amount': 'Negative values are not allowed.'})
        if self.health_penalty < 0:
            raise ValidationError({'health_penalty': 'Negative values are not allowed.'})
    
    class Meta:
        verbose_name = "Citizen Tax Data"
        verbose_name_plural = "Citizen Tax Data"