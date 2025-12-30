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