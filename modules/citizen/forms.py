from django import forms
from django.contrib.auth.forms import UserCreationForm
from modules.common.models import CustomUser
from modules.clerk.models import Grievance
from .models import FeedbackSuggestion, CitizenDocument


class CitizenLoginForm(forms.Form):
    """
    Form for citizen login with username and password
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


class CitizenRegistrationForm(forms.ModelForm):
    """
    Form for citizen registration
    """
    aadhaar_number = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Aadhaar number'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your address',
            'rows': 3
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'mobile_number', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your mobile number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            })
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get("mobile_number")
        if CustomUser.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError("A user with this mobile number already exists")
        return mobile_number
    
    def clean_aadhaar_number(self):
        aadhaar_number = self.cleaned_data.get("aadhaar_number")
        if aadhaar_number:
            if len(aadhaar_number) != 12:
                raise forms.ValidationError("Aadhaar number must be 12 digits")
            if not aadhaar_number.isdigit():
                raise forms.ValidationError("Aadhaar number must contain only digits")
        return aadhaar_number
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'citizen'
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class SchemeApplicationForm(forms.Form):
    """
    Dynamic form for scheme applications
    """
    applicant_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full name as per documents'
        })
    )
    father_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Father\'s name'
        })
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    annual_income = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Annual income in rupees'
        })
    )
    caste_category = forms.ChoiceField(
        choices=[
            ('general', 'General'),
            ('obc', 'OBC'),
            ('sc', 'SC'),
            ('st', 'ST'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    bank_account_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bank account number'
        })
    )
    ifsc_code = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'IFSC code'
        })
    )
    supporting_documents = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )


class GrievanceForm(forms.ModelForm):
    """
    Form for lodging grievances
    """
    class Meta:
        model = Grievance
        fields = ['title', 'description', 'category', 'priority', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief title of your grievance'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Detailed description of your grievance',
                'rows': 5
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category (e.g., Water Supply, Roads, etc.)'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class FeedbackForm(forms.ModelForm):
    """
    Form for feedback and suggestions
    """
    class Meta:
        model = FeedbackSuggestion
        fields = ['feedback_type', 'subject', 'message', 'attachment', 'is_anonymous']
        widgets = {
            'feedback_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your feedback'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your detailed feedback or suggestion',
                'rows': 5
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf,.doc,.docx'
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class FeedbackResponseForm(forms.ModelForm):
    """
    Form for admin/clerk to respond to feedback
    """
    class Meta:
        model = FeedbackSuggestion
        fields = ['status', 'admin_response']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'admin_response': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your response here...',
                'rows': 4
            })
        }


class DocumentUploadForm(forms.ModelForm):
    """
    Form for uploading citizen documents
    """
    class Meta:
        model = CitizenDocument
        fields = ['document_type', 'document_number', 'document_file']
        widgets = {
            'document_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'document_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document number (if applicable)'
            }),
            'document_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }