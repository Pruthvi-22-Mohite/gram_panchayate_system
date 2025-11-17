from django.db import models
from decimal import Decimal


class PanchayatBudget(models.Model):
    """Model for managing panchayat budget records"""
    
    # Budget head choices
    HEALTH_INSPECTION = 'Health Inspection'
    ELECTRICITY_TAX = 'Electricity Tax'
    GARBAGE_TAX = 'Garbage Tax'
    PUBLIC_WATER_SUPPLY = 'Public Water Supply'
    OTHER_WATER_SERVICES = 'Other Water Services'
    OLD_PRODUCT_INCOME = 'Old Product / Previous Income'
    
    BUDGET_HEAD_CHOICES = [
        (HEALTH_INSPECTION, 'Health Inspection'),
        (ELECTRICITY_TAX, 'Electricity Tax'),
        (GARBAGE_TAX, 'Garbage Tax'),
        (PUBLIC_WATER_SUPPLY, 'Public Water Supply'),
        (OTHER_WATER_SERVICES, 'Other Water Services'),
        (OLD_PRODUCT_INCOME, 'Old Product / Previous Income'),
    ]
    
    # Fields
    id = models.AutoField(primary_key=True, verbose_name='Sr. No.')
    budget_head = models.CharField(max_length=100, choices=BUDGET_HEAD_CHOICES)
    previous_year_amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    revenue_income = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    revenue_collection = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    expenditure_allotted = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    expenditure_spent = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    document = models.FileField(upload_to='budget_documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Panchayat Budget'
        verbose_name_plural = 'Panchayat Budgets'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.budget_head} - {self.total_amount}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to calculate total_amount automatically
        total_amount = previous_year_amount + revenue_income + revenue_collection - expenditure_spent
        """
        self.total_amount = (
            self.previous_year_amount + 
            self.revenue_income + 
            self.revenue_collection - 
            self.expenditure_spent
        )
        super().save(*args, **kwargs)