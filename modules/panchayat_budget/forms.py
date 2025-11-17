from django import forms
from .models import PanchayatBudget


class PanchayatBudgetForm(forms.ModelForm):
    """Form for creating and editing panchayat budget entries"""
    
    class Meta:
        model = PanchayatBudget
        fields = [
            'budget_head',
            'previous_year_amount',
            'revenue_income',
            'revenue_collection',
            'expenditure_allotted',
            'expenditure_spent',
            'document'
        ]
        widgets = {
            'budget_head': forms.Select(attrs={
                'class': 'form-control'
            }),
            'previous_year_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'revenue_income': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'revenue_collection': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'expenditure_allotted': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'expenditure_spent': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'document': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
    
    def clean(self):
        """Custom validation for the form"""
        cleaned_data = super().clean()
        return cleaned_data