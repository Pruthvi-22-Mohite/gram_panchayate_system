from django import forms
from .models import EmergencyContact


class EmergencyContactForm(forms.ModelForm):
    """
    Form for creating and editing emergency contacts
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make email required in HTML
        self.fields['email'].widget.attrs.update({'required': 'required'})
    
    class Meta:
        model = EmergencyContact
        fields = [
            'contact_name',
            'contact_type',
            'phone_number',
            'email',
            'address',
            'available_24x7',
            'opening_time',
            'closing_time',
        ]
        
        widgets = {
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact name or organization'
            }),
            'contact_type': forms.Select(attrs={
                'class': 'form-select',
                'onchange': 'toggleOtherContactType()',
                'required': 'required'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
                'required': 'required'  # Required field
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete address'
            }),
            'available_24x7': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'available_24x7_checkbox'
            }),
            'opening_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'opening_time_input'
            }),
            'closing_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'id': 'closing_time_input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add other service type field for 'other' option
        self.fields['other_service_type'] = forms.CharField(
            max_length=100,
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify service type',
                'id': 'other_service_type'
            })
        )
        
        labels = {
            'contact_name': 'Contact Name *',
            'contact_type': 'Service Type *',
            'phone_number': 'Phone Number *',
            'email': 'Email *',  # Updated to indicate required
            'address': 'Address *',
            'available_24x7': 'Available 24/7',
            'opening_time': 'Opening Time',
            'closing_time': 'Closing Time',
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or not email.strip():
            raise forms.ValidationError("Email is required.")
        # Validate email format
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")
        return email
    
    def clean_contact_type(self):
        contact_type = self.cleaned_data.get('contact_type')
        if contact_type == 'other' or contact_type == 'others':
            # If 'other' is selected, we need to validate the custom service type
            other_service_type = self.cleaned_data.get('other_service_type', '').strip()
            if not other_service_type:
                raise forms.ValidationError("When 'Other' is selected, please specify the service type.")
        return contact_type
