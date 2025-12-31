from django import forms
from django.contrib.auth.forms import AuthenticationForm
from modules.common.models import CustomUser
from modules.clerk.models import ClerkProfile

class AdminLoginForm(AuthenticationForm):
    """
    Custom login form for Admin users
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


class ClerkCreationForm(forms.ModelForm):
    """
    Form for creating clerk accounts by admin
    """
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password for clerk',
            'required': 'required',
            'minlength': '8'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
            'required': 'required'
        })
    )
    
    # Clerk profile fields
    panchayat_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Panchayat name'
        })
    )
    designation = forms.CharField(
        max_length=100,
        required=True,  # Required field
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter designation (e.g., Junior Clerk)'
        })
    )
    employee_id = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter employee ID'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile_number')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose username for clerk'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name',
                'required': 'required'  # Required attribute
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name',
                'required': 'required'  # Required attribute
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
                'required': 'required'  # Required attribute
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile number',
                'required': 'required'  # Required attribute
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
        
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\"\\|,.<>\/?]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
        
        return password
    
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
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or not email.strip():
            raise forms.ValidationError("Email is required.")
        return email
    
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number or not mobile_number.strip():
            raise forms.ValidationError("Mobile number is required.")
        # Remove any spaces or hyphens
        mobile_number_clean = mobile_number.replace(' ', '').replace('-', '')
        if len(mobile_number_clean) != 10 or not mobile_number_clean.isdigit():
            raise forms.ValidationError("Mobile number must be exactly 10 digits.")
        return mobile_number
    
    def clean_designation(self):
        designation = self.cleaned_data.get('designation')
        if not designation or not designation.strip():
            raise forms.ValidationError("Designation is required.")
        return designation
    
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get("employee_id")
        if ClerkProfile.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError("A clerk with this employee ID already exists")
        return employee_id
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        if password1:
            self.validate_password_strength(password1)
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'clerk'
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ClerkEditForm(forms.ModelForm):
    """
    Form for editing clerk accounts by admin
    """
    # Clerk profile fields
    panchayat_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Panchayat name'
        })
    )
    designation = forms.CharField(
        max_length=100,
        required=True,  # Required field
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter designation (e.g., Junior Clerk)'
        })
    )
    employee_id = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter employee ID'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'mobile_number')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose username for clerk'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile number'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If we're editing an existing clerk, populate the profile fields
        if self.instance and self.instance.pk:
            try:
                clerk_profile = self.instance.clerkprofile
                self.fields['panchayat_name'].initial = clerk_profile.panchayat_name
                self.fields['designation'].initial = clerk_profile.designation
                self.fields['employee_id'].initial = clerk_profile.employee_id
            except ClerkProfile.DoesNotExist:
                pass
    
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get("employee_id")
        # Check if another clerk already has this employee ID
        if self.instance and self.instance.pk:
            if ClerkProfile.objects.filter(employee_id=employee_id).exclude(user=self.instance).exists():
                raise forms.ValidationError("A clerk with this employee ID already exists")
        elif ClerkProfile.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError("A clerk with this employee ID already exists")
        return employee_id
        
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
            
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
            
        return password
        
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
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or not email.strip():
            raise forms.ValidationError("Email is required.")
        return email
        
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number or not mobile_number.strip():
            raise forms.ValidationError("Mobile number is required.")
        # Remove any spaces or hyphens
        mobile_number_clean = mobile_number.replace(' ', '').replace('-', '')
        if len(mobile_number_clean) != 10 or not mobile_number_clean.isdigit():
            raise forms.ValidationError("Mobile number must be exactly 10 digits.")
        return mobile_number
    
    def clean_designation(self):
        designation = self.cleaned_data.get('designation')
        if not designation or not designation.strip():
            raise forms.ValidationError("Designation is required.")
        return designation
    
    def clean(self):
        cleaned_data = super().clean()
        # Add password validation if password fields are present
        password1 = self.data.get('password1')
        password2 = self.data.get('password2')
        
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        if password1:
            self.validate_password_strength(password1)
        
        return cleaned_data
    

class UserManagementForm(forms.Form):
    """
    Form for user management actions
    """
    ACTION_CHOICES = [
        ('activate', 'Activate User'),
        ('deactivate', 'Deactivate User'),
        ('delete', 'Delete User'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    user_ids = forms.CharField(
        widget=forms.HiddenInput()
    )