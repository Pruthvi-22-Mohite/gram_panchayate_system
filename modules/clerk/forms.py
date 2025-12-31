from django import forms
from django.contrib.auth.forms import AuthenticationForm
from modules.common.models import CustomUser
from .models import Scheme, Grievance, TaxRecord


class ClerkLoginForm(AuthenticationForm):
    """
    Custom login form for Clerk users
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )


class SchemeForm(forms.ModelForm):
    """
    Form for creating and editing government schemes
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make required fields required in HTML
        self.fields['application_process'].widget.attrs.update({'required': 'required'})
        self.fields['last_date'].widget.attrs.update({'required': 'required'})
        self.fields['contact_person'].widget.attrs.update({'required': 'required'})
    
    class Meta:
        model = Scheme
        fields = ['name', 'description', 'eligibility_criteria', 'required_documents', 
                  'benefits', 'application_process', 'last_date', 'contact_person', 
                  'downloadable_forms', 'is_active', 'scheme_image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Scheme name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Scheme description',
                'rows': 4
            }),
            'eligibility_criteria': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Who is eligible for this scheme?',
                'rows': 3
            }),
            'required_documents': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'List of required documents',
                'rows': 3
            }),
            'benefits': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Benefits provided by this scheme',
                'rows': 3
            }),
            'application_process': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Step-by-step application process',
                'rows': 3,
                'required': 'required'  # Required field
            }),
            'last_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required'  # Required field
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name and contact details of the person to contact',
                'required': 'required'  # Required field
            }),
            'downloadable_forms': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'scheme_image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_application_process(self):
        application_process = self.cleaned_data.get('application_process')
        if not application_process or not application_process.strip():
            raise forms.ValidationError("Application process is required and cannot be empty.")
        return application_process
    
    def clean_last_date(self):
        last_date = self.cleaned_data.get('last_date')
        if not last_date:
            raise forms.ValidationError("Last date is required.")
        from django.utils import timezone
        if last_date < timezone.now().date():
            raise forms.ValidationError("Last date cannot be in the past.")
        return last_date
    
    def clean_contact_person(self):
        contact_person = self.cleaned_data.get('contact_person')
        if not contact_person or not contact_person.strip():
            raise forms.ValidationError("Contact person is required.")
        return contact_person


class GrievanceResponseForm(forms.ModelForm):
    """
    Form for responding to grievances
    """
    class Meta:
        model = Grievance
        fields = ['status', 'priority', 'resolution_notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'resolution_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter resolution notes or response',
                'rows': 4
            })
        }


class TaxRecordForm(forms.ModelForm):
    """
    Form for creating tax records
    """
    taxpayer = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(user_type='citizen'),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = TaxRecord
        fields = ['taxpayer', 'tax_type', 'amount', 'due_date', 'status']
        widgets = {
            'tax_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'step': '0.01'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return amount


class SchemeApplicationReviewForm(forms.Form):
    """
    Form for reviewing scheme applications
    """
    STATUS_CHOICES = [
        ('approved', 'Approve'),
        ('rejected', 'Reject'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    review_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter review notes',
            'rows': 4
        }),
        required=False
    )