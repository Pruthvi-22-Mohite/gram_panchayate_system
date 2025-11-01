from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
    """
    Custom login form for Admin and Clerk users
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

class CitizenOTPRequestForm(forms.Form):
    """
    Form for citizen to request OTP
    """
    mobile_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your mobile number',
            'id': 'userId'
        })
    )

class CitizenOTPVerificationForm(forms.Form):
    """
    Form for citizen to verify OTP
    """
    mobile_number = forms.CharField(
        max_length=15,
        widget=forms.HiddenInput()
    )
    otp = forms.CharField(
        max_length=6,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter OTP',
            'id': 'otp'
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
        fields = ('username', 'mobile_number')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your mobile number'
            })
        }
    
    def clean_password2(self):
        """
        Check that the two password entries match
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_mobile_number(self):
        """
        Check that the mobile number is unique
        """
        mobile_number = self.cleaned_data.get("mobile_number")
        if CustomUser.objects.filter(mobile_number=mobile_number).exists():
            raise forms.ValidationError("A user with this mobile number already exists")
        return mobile_number
    
    def clean_aadhaar_number(self):
        """
        Check that the Aadhaar number is unique and valid
        """
        aadhaar_number = self.cleaned_data.get("aadhaar_number")
        if aadhaar_number:
            if len(aadhaar_number) != 12:
                raise forms.ValidationError("Aadhaar number must be 12 digits")
            if not aadhaar_number.isdigit():
                raise forms.ValidationError("Aadhaar number must contain only digits")
        return aadhaar_number
    
    def save(self, commit=True):
        """
        Save the user with the provided password
        """
        user = super().save(commit=False)
        user.user_type = 'citizen'
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user