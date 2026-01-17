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
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name',
            'required': 'required'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name',
            'required': 'required'
        })
    )
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
        fields = ('username', 'first_name', 'last_name', 'mobile_number', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
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
            
        # Validate password strength
        if password1:
            self.validate_password_strength(password1)
            
        return password2
        
    def validate_password_strength(self, password):
        """Validate password strength: minimum 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char"""
        import re
            
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
            
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
            
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
            
        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one number.")
            
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\"\'\\|,.<>/?]', password):
            raise forms.ValidationError("Password must contain at least one special character (!@#$%^&*()_+-=[]{};\'\\|,.<>?).")
            
        return password
    
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get("mobile_number")
        if not mobile_number:
            raise forms.ValidationError("Mobile number is required.")
        
        # Remove any spaces, hyphens, or other characters
        mobile_clean = mobile_number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        # Check length
        if len(mobile_clean) != 10:
            raise forms.ValidationError("Mobile number must be exactly 10 digits.")
        
        # Check if all characters are digits
        if not mobile_clean.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")
        
        # Check if number already exists
        if CustomUser.objects.filter(mobile_number=mobile_clean).exists():
            raise forms.ValidationError("A user with this mobile number already exists")
        
        return mobile_clean
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Username is required.")
        
        # Check username length
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters long.")
        
        if len(username) > 150:
            raise forms.ValidationError("Username cannot exceed 150 characters.")
        
        # Check for invalid characters
        import re
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            raise forms.ValidationError("Username can only contain letters, numbers, and underscores.")
        
        # Check if username already exists
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken.")
        
        return username
    
    def clean_aadhaar_number(self):
        aadhaar_number = self.cleaned_data.get("aadhaar_number")
        if aadhaar_number:
            if len(aadhaar_number) != 12:
                raise forms.ValidationError("Aadhaar number must be 12 digits")
            if not aadhaar_number.isdigit():
                raise forms.ValidationError("Aadhaar number must contain only digits")
        return aadhaar_number
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name or not first_name.strip():
            raise forms.ValidationError("First name is required.")
        if not first_name.replace(' ', '').isalpha():
            raise forms.ValidationError("First name must contain only alphabets.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name or not last_name.strip():
            raise forms.ValidationError("Last name is required.")
        if not last_name.replace(' ', '').isalpha():
            raise forms.ValidationError("Last name must contain only alphabets.")
        return last_name
    
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
    
    def clean_annual_income(self):
        annual_income = self.cleaned_data.get('annual_income')
        if annual_income is not None and annual_income < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return annual_income
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
                'placeholder': 'Category (e.g., Water Supply, Roads, etc.)',
                'onchange': 'toggleOtherGrievanceCategory()'
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
                'class': 'form-control',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your feedback',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your detailed feedback or suggestion',
                'rows': 5,
                'required': True
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make admin_response required in HTML
        self.fields['admin_response'].widget.attrs.update({'required': 'required'})
    
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
                'rows': 4,
                'required': 'required'  # Required field
            })
        }
    
    def clean_admin_response(self):
        admin_response = self.cleaned_data.get('admin_response')
        if not admin_response or not admin_response.strip():
            raise forms.ValidationError("Admin response is required and cannot be empty.")
        # Remove whitespace to check if field is truly empty
        stripped_response = admin_response.strip()
        if len(stripped_response) < 10:
            raise forms.ValidationError("Admin response must be at least 10 characters long for meaningful feedback.")
        return admin_response


class DocumentUploadForm(forms.ModelForm):
    """
    Form for uploading citizen documents
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add other document type field for 'other' option
        self.fields['other_document_type'] = forms.CharField(
            max_length=100,
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify document type',
                'id': 'other_document_type'
            })
        )
    
    class Meta:
        model = CitizenDocument
        fields = ['document_type', 'document_number', 'document_file']
        widgets = {
            'document_type': forms.Select(attrs={
                'class': 'form-control',
                'onchange': 'toggleOtherField(this, "document")'
            }),
            'document_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document number (if applicable)'
            }),
            'document_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_document_type(self):
        document_type = self.cleaned_data.get('document_type')
        if document_type == 'other':
            # If 'other' is selected, we need to validate the custom document type
            other_document_type = self.cleaned_data.get('other_document_type', '').strip()
            if not other_document_type:
                raise forms.ValidationError("When 'Other' is selected, please specify the document type.")
        return document_type