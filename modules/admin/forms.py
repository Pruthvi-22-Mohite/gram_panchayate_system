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
            'placeholder': 'Enter password for clerk'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
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
        required=False,
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
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_employee_id(self):
        employee_id = self.cleaned_data.get("employee_id")
        if ClerkProfile.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError("A clerk with this employee ID already exists")
        return employee_id
    
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
        required=False,
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