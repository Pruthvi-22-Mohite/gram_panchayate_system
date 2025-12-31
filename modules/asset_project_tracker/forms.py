from django import forms
from .models import Asset, Project


class AssetForm(forms.ModelForm):
    """Form for creating and updating assets"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make required fields required in HTML
        self.fields['ward_number'].widget.attrs.update({'required': 'required'})
        self.fields['purchase_date'].widget.attrs.update({'required': 'required'})
        self.fields['purchase_cost'].widget.attrs.update({'required': 'required'})
        self.fields['current_value'].widget.attrs.update({'required': 'required'})
        self.fields['contact_number'].widget.attrs.update({'required': 'required'})
    
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
            'asset_type': forms.Select(attrs={'class': 'form-select', 'onchange': 'toggleOtherAssetType()', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'ward_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ward number', 'required': 'required'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'purchase_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'required': 'required'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'required': 'required'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'last_maintenance_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsible_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of responsible person'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact number', 'required': 'required'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Additional remarks'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add other asset type field for 'other' option
        self.fields['other_asset_type'] = forms.CharField(
            max_length=100,
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify asset type',
                'id': 'other_asset_type'
            })
        )
    
    def clean_ward_number(self):
        ward_number = self.cleaned_data.get('ward_number')
        if not ward_number or not ward_number.strip():
            raise forms.ValidationError("Ward number is required.")
        return ward_number
    
    def clean_purchase_date(self):
        purchase_date = self.cleaned_data.get('purchase_date')
        if not purchase_date:
            raise forms.ValidationError("Purchase date is required.")
        return purchase_date
    
    def clean_purchase_cost(self):
        purchase_cost = self.cleaned_data.get('purchase_cost')
        if purchase_cost is not None and purchase_cost < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return purchase_cost
    
    def clean_current_value(self):
        current_value = self.cleaned_data.get('current_value')
        if current_value is not None and current_value < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return current_value
    
    def clean_asset_type(self):
        asset_type = self.cleaned_data.get('asset_type')
        if asset_type == 'other':
            # If 'other' is selected, we need to validate the custom asset type
            other_asset_type = self.cleaned_data.get('other_asset_type', '').strip()
            if not other_asset_type:
                raise forms.ValidationError("When 'Other' is selected, please specify the asset type.")
        return asset_type
    
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number:
            # Remove any spaces or hyphens
            contact_number_clean = contact_number.replace(' ', '').replace('-', '')
            if len(contact_number_clean) != 10 or not contact_number_clean.isdigit():
                raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact_number


class ProjectForm(forms.ModelForm):
    """Form for creating and updating projects"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make required fields required in HTML
        self.fields['ward_number'].widget.attrs.update({'required': 'required'})
        self.fields['budget_spent'].widget.attrs.update({'required': 'required'})
        self.fields['start_date'].widget.attrs.update({'required': 'required'})
        self.fields['target_completion_date'].widget.attrs.update({'required': 'required'})
        self.fields['contractor_name'].widget.attrs.update({'required': 'required'})
        self.fields['contractor_contact'].widget.attrs.update({'required': 'required'})
    
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
            'project_type': forms.Select(attrs={'class': 'form-select', 'onchange': 'toggleOtherProjectType()', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter project description'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'ward_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ward number', 'required': 'required'}),
            'budget_allocated': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'budget_spent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'required': 'required'}),
            'funding_source': forms.Select(attrs={'class': 'form-select', 'onchange': 'toggleOtherField(this, "funding")'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'target_completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}),
            'actual_completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'progress_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'placeholder': '0-100'}),
            'contractor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contractor name', 'required': 'required'}),
            'contractor_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact number', 'required': 'required'}),
            'beneficiaries_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of beneficiaries'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Additional remarks'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add other project type field for 'other' option
        self.fields['other_project_type'] = forms.CharField(
            max_length=100,
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify project type',
                'id': 'other_project_type'
            })
        )
        
        # Add other funding source field for 'other' option
        self.fields['other_funding_source'] = forms.CharField(
            max_length=100,
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify funding source',
                'id': 'other_funding_source'
            })
        )
    
    def clean_ward_number(self):
        ward_number = self.cleaned_data.get('ward_number')
        if not ward_number or not ward_number.strip():
            raise forms.ValidationError("Ward number is required.")
        return ward_number
    
    def clean_budget_spent(self):
        budget_spent = self.cleaned_data.get('budget_spent')
        if budget_spent is not None and budget_spent < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return budget_spent
    
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if not start_date:
            raise forms.ValidationError("Start date is required.")
        return start_date
    
    def clean_target_completion_date(self):
        target_completion_date = self.cleaned_data.get('target_completion_date')
        start_date = self.cleaned_data.get('start_date')
        
        if not target_completion_date:
            raise forms.ValidationError("Target completion date is required.")
        
        if start_date and target_completion_date and target_completion_date <= start_date:
            raise forms.ValidationError("Target completion date must be after start date.")
        
        return target_completion_date
    
    def clean_contractor_name(self):
        contractor_name = self.cleaned_data.get('contractor_name')
        if not contractor_name or not contractor_name.strip():
            raise forms.ValidationError("Contractor name is required.")
        return contractor_name
    
    def clean_project_type(self):
        project_type = self.cleaned_data.get('project_type')
        if project_type == 'other':
            # If 'other' is selected, we need to validate the custom project type
            other_project_type = self.cleaned_data.get('other_project_type', '').strip()
            if not other_project_type:
                raise forms.ValidationError("When 'Other' is selected, please specify the project type.")
        return project_type
    
    def clean_contractor_contact(self):
        contractor_contact = self.cleaned_data.get('contractor_contact')
        if contractor_contact:
            # Remove any spaces or hyphens
            contractor_contact_clean = contractor_contact.replace(' ', '').replace('-', '')
            if len(contractor_contact_clean) != 10 or not contractor_contact_clean.isdigit():
                raise forms.ValidationError("Contractor contact number must be exactly 10 digits.")
        return contractor_contact
    
    def clean_budget_allocated(self):
        budget_allocated = self.cleaned_data.get('budget_allocated')
        if budget_allocated is not None and budget_allocated < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return budget_allocated
    
    def clean_progress_percentage(self):
        progress_percentage = self.cleaned_data.get('progress_percentage')
        if progress_percentage is not None and progress_percentage < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return progress_percentage
    
    def clean_beneficiaries_count(self):
        beneficiaries_count = self.cleaned_data.get('beneficiaries_count')
        if beneficiaries_count is not None and beneficiaries_count < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return beneficiaries_count
    
    def clean_funding_source(self):
        funding_source = self.cleaned_data.get('funding_source')
        if funding_source == 'other':
            # If 'other' is selected, we need to validate the custom funding source
            other_funding_source = self.cleaned_data.get('other_funding_source', '').strip()
            if not other_funding_source:
                raise forms.ValidationError("When 'Other' is selected, please specify the funding source.")
        return funding_source
