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
    class Meta:
        model = Scheme
        fields = ['name', 'description', 'eligibility_criteria', 'required_documents', 'benefits', 'is_active']
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
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


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
        fields = ['taxpayer', 'tax_type', 'amount', 'due_date']
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