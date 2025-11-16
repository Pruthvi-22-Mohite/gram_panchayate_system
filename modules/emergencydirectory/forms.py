from django import forms
from .models import EmergencyContact


class EmergencyContactForm(forms.ModelForm):
    """
    Form for creating and editing emergency contacts
    """
    
    class Meta:
        model = EmergencyContact
        fields = [
            'contact_name',
            'contact_type',
            'phone_number',
            'email',
            'address',
        ]
        
        widgets = {
            'contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact name or organization'
            }),
            'contact_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email (optional)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete address'
            }),
        }
        
        labels = {
            'contact_name': 'Contact Name *',
            'contact_type': 'Service Type *',
            'phone_number': 'Phone Number *',
            'email': 'Email',
            'address': 'Address *',
        }
