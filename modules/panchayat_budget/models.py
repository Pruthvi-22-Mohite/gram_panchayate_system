from django.db import models
from django.conf import settings
import os

class PanchayatBudget(models.Model):
    """Model for managing panchayat budget PDFs for the last 3 financial years"""
    
    # Last 3 financial years
    FINANCIAL_YEAR_CHOICES = [
        ('2022-2023', '2022-2023'),
        ('2023-2024', '2023-2024'),
        ('2024-2025', '2024-2025'),
    ]
    
    financial_year = models.CharField(
        max_length=9, 
        choices=FINANCIAL_YEAR_CHOICES,
        unique=True,
        verbose_name="Financial Year"
    )
    title = models.CharField(max_length=200, verbose_name="Budget Title")
    description = models.TextField(blank=True, verbose_name="Description")
    pdf_file = models.FileField(upload_to='budget_pdfs/', verbose_name="PDF File")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Uploaded By"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Upload Date")
    
    class Meta:
        verbose_name = 'Panchayat Budget'
        verbose_name_plural = 'Panchayat Budgets'
        ordering = ['-financial_year']
    
    def __str__(self):
        return f"{self.title} ({self.financial_year})"
    
    def filename(self):
        """Return the filename of the PDF"""
        return os.path.basename(self.pdf_file.name)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.financial_year or not self.financial_year.strip():
            raise ValidationError({'financial_year': 'Financial year is required.'})
        if not self.title or not self.title.strip():
            raise ValidationError({'title': 'Title is required.'})
        if not self.description or not self.description.strip():
            raise ValidationError({'description': 'Description is required.'})
        if not self.pdf_file:
            raise ValidationError({'pdf_file': 'Budget file is required.'})
        else:
            # Check if the file is a PDF
            if not self.pdf_file.name.lower().endswith('.pdf'):
                raise ValidationError({'pdf_file': 'Only PDF files are allowed.'})
            # Check if the file is empty
            if self.pdf_file.size == 0:
                raise ValidationError({'pdf_file': 'Budget file cannot be empty.'})

class BudgetEntry(models.Model):
    """Model for managing detailed panchayat budget entries with numeric amounts"""
    
    BUDGET_HEAD_CHOICES = [
        ('health_inspection', 'Health Inspection'),
        ('electricity_tax', 'Electricity Tax'),
        ('garbage_tax', 'Garbage Tax'),
        ('public_water_supply', 'Public Water Supply'),
        ('old_product_income', 'Old Product Income'),
        ('development_works', 'Development Works'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('sanitation', 'Sanitation'),
        ('water_supply', 'Water Supply'),
        ('roads', 'Roads'),
        ('other', 'Other'),
    ]
    
    budget_head = models.CharField(max_length=50, choices=BUDGET_HEAD_CHOICES, verbose_name="Budget Head")
    previous_year_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Previous Year Amount")
    revenue_income = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Revenue Income")
    revenue_collection = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Revenue Collection")
    expenditure_allotted = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Expenditure Allotted")
    expenditure_spent = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Expenditure Spent")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    
    class Meta:
        verbose_name = 'Budget Entry'
        verbose_name_plural = 'Budget Entries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_budget_head_display()} - ₹{self.previous_year_amount}"
    
    def total_amount(self):
        """Calculate total amount: Previous Year + Revenue Income + Revenue Collection - Expenditure Spent"""
        return self.previous_year_amount + self.revenue_income + self.revenue_collection - self.expenditure_spent
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validate that all numeric fields are non-negative
        if self.previous_year_amount is not None and self.previous_year_amount < 0:
            raise ValidationError({'previous_year_amount': 'Negative values are not allowed.'})
        if self.revenue_income is not None and self.revenue_income < 0:
            raise ValidationError({'revenue_income': 'Negative values are not allowed.'})
        if self.revenue_collection is not None and self.revenue_collection < 0:
            raise ValidationError({'revenue_collection': 'Negative values are not allowed.'})
        if self.expenditure_allotted is not None and self.expenditure_allotted < 0:
            raise ValidationError({'expenditure_allotted': 'Negative values are not allowed.'})
        if self.expenditure_spent is not None and self.expenditure_spent < 0:
            raise ValidationError({'expenditure_spent': 'Negative values are not allowed.'})
        
        # Validate required fields
        if not self.budget_head:
            raise ValidationError({'budget_head': 'Budget head is required.'})
        
        if self.previous_year_amount is None:
            raise ValidationError({'previous_year_amount': 'Previous year amount is required.'})
        if self.revenue_income is None:
            raise ValidationError({'revenue_income': 'Revenue income is required.'})
        if self.revenue_collection is None:
            raise ValidationError({'revenue_collection': 'Revenue collection is required.'})
        if self.expenditure_allotted is None:
            raise ValidationError({'expenditure_allotted': 'Expenditure allotted is required.'})
        if self.expenditure_spent is None:
            raise ValidationError({'expenditure_spent': 'Expenditure spent is required.'})