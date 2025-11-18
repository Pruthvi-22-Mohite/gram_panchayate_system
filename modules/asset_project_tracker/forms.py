from django import forms
from .models import Asset, Project


class AssetForm(forms.ModelForm):
    """Form for creating and updating assets"""
    
    class Meta:
        model = Asset
        fields = [
            'asset_name', 'asset_type', 'description', 'location', 'ward_number',
            'purchase_date', 'purchase_cost', 'current_value',
            'condition', 'last_maintenance_date', 'next_maintenance_date',
            'responsible_person', 'contact_number', 'photo', 'remarks', 'is_active'
        ]
        widgets = {
            'asset_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter asset name'}),
            'asset_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'ward_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ward number'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'purchase_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'last_maintenance_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsible_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of responsible person'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact number'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Additional remarks'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProjectForm(forms.ModelForm):
    """Form for creating and updating projects"""
    
    class Meta:
        model = Project
        fields = [
            'project_name', 'project_type', 'description', 'location', 'ward_number',
            'budget_allocated', 'budget_spent', 'funding_source',
            'start_date', 'target_completion_date', 'actual_completion_date',
            'status', 'progress_percentage',
            'contractor_name', 'contractor_contact', 'beneficiaries_count',
            'photo', 'document', 'remarks'
        ]
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'project_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter project description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'ward_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ward number'}),
            'budget_allocated': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'budget_spent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'funding_source': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'target_completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actual_completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'progress_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'placeholder': '0-100'}),
            'contractor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contractor name'}),
            'contractor_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact number'}),
            'beneficiaries_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of beneficiaries'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Additional remarks'}),
        }
