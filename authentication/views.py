from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import random
import json

from gram_panchayate_system.models import CustomUser, OTP, CitizenProfile
from .forms import CustomLoginForm, CitizenOTPRequestForm, CitizenOTPVerificationForm, CitizenRegistrationForm
from .sms import sms_service
from gram_panchayate_system.decorators import citizen_required, clerk_required, admin_required

def login_view(request):
    """Main login page view - shows options for different user types"""
    # If user is already authenticated, redirect to appropriate dashboard
    if request.user.is_authenticated:
        if request.user.user_type == 'admin':
            return redirect('auth:admin_dashboard')
        elif request.user.user_type == 'clerk':
            return redirect('auth:clerk_dashboard')
        elif request.user.user_type == 'citizen':
            return redirect('auth:citizen_dashboard')
    
    return render(request, 'login.html')

def admin_login(request):
    """Admin login view"""
    # If user is already authenticated and is admin, redirect to admin dashboard
    if request.user.is_authenticated and request.user.user_type == 'admin':
        return redirect('auth:admin_dashboard')
        
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.user_type == 'admin':
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('auth:admin_dashboard')
            else:
                messages.error(request, "Invalid credentials or not an admin user.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = CustomLoginForm()
    
    return render(request, 'admin_login.html', {'form': form})

def clerk_login(request):
    """Clerk login view"""
    # If user is already authenticated and is clerk, redirect to clerk dashboard
    if request.user.is_authenticated and request.user.user_type == 'clerk':
        return redirect('auth:clerk_dashboard')
        
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.user_type == 'clerk':
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('auth:clerk_dashboard')
            else:
                messages.error(request, "Invalid credentials or not a clerk user.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = CustomLoginForm()
    
    return render(request, 'clerk_login.html', {'form': form})

def citizen_otp_request(request):
    """Citizen OTP request view"""
    # If user is already authenticated and is citizen, redirect to citizen dashboard
    if request.user.is_authenticated and request.user.user_type == 'citizen':
        return redirect('auth:citizen_dashboard')
        
    if request.method == 'POST':
        form = CitizenOTPRequestForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            
            # Check if user with this mobile number exists
            try:
                user = CustomUser.objects.get(mobile_number=mobile_number, user_type='citizen')
            except ObjectDoesNotExist:
                messages.error(request, "No citizen account found with this mobile number.")
                return render(request, 'citizen_otp_request.html', {'form': form})
            
            # Generate 6-digit OTP using SMS service
            otp_code = sms_service.generate_otp()
            
            # Save OTP to database
            otp_instance = OTP(mobile_number=mobile_number, otp=otp_code)
            otp_instance.save()
            
            # Send OTP via SMS
            if sms_service.send_otp(mobile_number, otp_code):
                messages.success(request, "OTP sent to your mobile number.")
            else:
                messages.error(request, "Failed to send OTP. Please try again.")
            
            # Redirect to OTP verification page with mobile number in session
            request.session['otp_mobile_number'] = mobile_number
            return redirect('auth:citizen_otp_verify')
    else:
        form = CitizenOTPRequestForm()
    
    return render(request, 'citizen_otp_request.html', {'form': form})

def citizen_otp_verify(request):
    """Citizen OTP verification view"""
    if request.method == 'POST':
        form = CitizenOTPVerificationForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            otp_code = form.cleaned_data['otp']
            
            # Check if OTP exists and is valid
            try:
                # Get all OTPs for this mobile number that are not used
                otp_records = OTP._default_manager.filter(
                    mobile_number=mobile_number, 
                    is_used=False
                ).order_by('-created_at')
                
                if not otp_records.exists():
                    raise ObjectDoesNotExist
                
                otp_record = otp_records.first()
                
                # Check if OTP matches
                if otp_record.otp != otp_code:
                    raise ObjectDoesNotExist
                
                # Check if OTP is expired
                if otp_record.is_expired():
                    messages.error(request, "OTP has expired. Please request a new one.")
                    return redirect('auth:citizen_otp_request')
                
                # Mark OTP as used
                otp_record.is_used = True
                otp_record.save()
                
                # Authenticate user
                try:
                    user = CustomUser.objects.get(mobile_number=mobile_number, user_type='citizen')
                    login(request, user)
                    messages.success(request, f"Welcome, {user.username}!")
                    return redirect('auth:citizen_dashboard')
                except ObjectDoesNotExist:
                    messages.error(request, "User account not found.")
                    return redirect('auth:citizen_otp_request')
                    
            except ObjectDoesNotExist:
                messages.error(request, "Invalid OTP. Please try again.")
                return render(request, 'citizen_otp_verify.html', {
                    'form': CitizenOTPVerificationForm(initial={'mobile_number': mobile_number}),
                    'mobile_number': mobile_number
                })
        else:
            # Get mobile number from form data to pass it back
            mobile_number = request.POST.get('mobile_number', '')
            return render(request, 'citizen_otp_verify.html', {
                'form': form,
                'mobile_number': mobile_number
            })
    else:
        # For GET requests, get mobile number from session
        mobile_number = request.session.get('otp_mobile_number', '')
        if not mobile_number:
            # If no mobile number in session, redirect to OTP request page
            return redirect('auth:citizen_otp_request')
        
        form = CitizenOTPVerificationForm(initial={'mobile_number': mobile_number})
        return render(request, 'citizen_otp_verify.html', {
            'form': form,
            'mobile_number': mobile_number
        })
    
    # If not POST, redirect to OTP request page
    return redirect('auth:citizen_otp_request')

def citizen_aadhaar_otp_request(request):
    """Citizen Aadhaar OTP request view - alternative to mobile OTP"""
    # If user is already authenticated and is citizen, redirect to citizen dashboard
    if request.user.is_authenticated and request.user.user_type == 'citizen':
        return redirect('auth:citizen_dashboard')
        
    if request.method == 'POST':
        aadhaar_number = request.POST.get('aadhaar_number')
        
        if not aadhaar_number:
            messages.error(request, "Aadhaar number is required.")
            return render(request, 'citizen_aadhaar_otp_request.html')
        
        # Validate Aadhaar number format (12 digits)
        if len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
            messages.error(request, "Please enter a valid 12-digit Aadhaar number.")
            return render(request, 'citizen_aadhaar_otp_request.html')
        
        # Check if user with this Aadhaar number exists
        try:
            user = CustomUser.objects.get(citizenprofile__aadhaar_number=aadhaar_number, user_type='citizen')
        except ObjectDoesNotExist:
            messages.error(request, "No citizen account found with this Aadhaar number.")
            return render(request, 'citizen_aadhaar_otp_request.html')
        
        # Note: In a real implementation, you would integrate with UIDAI's Aadhaar OTP API here
        # For now, we'll generate a system OTP and store it
        otp_code = sms_service.generate_otp()
        
        # Save OTP to database (using Aadhaar number as identifier)
        otp_instance = OTP(mobile_number=aadhaar_number, otp=otp_code)
        otp_instance.save()
        
        # In a real implementation, you would call UIDAI API to send OTP to user's registered mobile
        # For demo purposes, we'll just show a message
        messages.info(request, "In a real implementation, an OTP would be sent to your registered mobile number via UIDAI. For demo purposes, please use the system-generated OTP.")
        messages.success(request, f"Demo OTP (for testing only): {otp_code}")
        
        # Redirect to Aadhaar OTP verification page with Aadhaar number in session
        request.session['otp_aadhaar_number'] = aadhaar_number
        return redirect('auth:citizen_aadhaar_otp_verify')
    
    return render(request, 'citizen_aadhaar_otp_request.html')

def citizen_aadhaar_otp_verify(request):
    """Citizen Aadhaar OTP verification view"""
    if request.method == 'POST':
        aadhaar_number = request.POST.get('aadhaar_number')
        otp_code = request.POST.get('otp')
        
        if not aadhaar_number or not otp_code:
            messages.error(request, "Aadhaar number and OTP are required.")
            return render(request, 'citizen_aadhaar_otp_verify.html', {
                'aadhaar_number': aadhaar_number
            })
        
        # Check if OTP exists and is valid
        try:
            # Get all OTPs for this Aadhaar number that are not used
            otp_records = OTP._default_manager.filter(
                mobile_number=aadhaar_number, 
                is_used=False
            ).order_by('-created_at')
            
            if not otp_records.exists():
                raise ObjectDoesNotExist
            
            otp_record = otp_records.first()
            
            # Check if OTP matches
            if otp_record.otp != otp_code:
                raise ObjectDoesNotExist
            
            # Check if OTP is expired
            if otp_record.is_expired():
                messages.error(request, "OTP has expired. Please request a new one.")
                return redirect('auth:citizen_aadhaar_otp_request')
            
            # Mark OTP as used
            otp_record.is_used = True
            otp_record.save()
            
            # Authenticate user
            try:
                user = CustomUser.objects.get(citizenprofile__aadhaar_number=aadhaar_number, user_type='citizen')
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('auth:citizen_dashboard')
            except ObjectDoesNotExist:
                messages.error(request, "User account not found.")
                return redirect('auth:citizen_aadhaar_otp_request')
                
        except ObjectDoesNotExist:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, 'citizen_aadhaar_otp_verify.html', {
                'aadhaar_number': aadhaar_number
            })
    else:
        # For GET requests, get Aadhaar number from session
        aadhaar_number = request.session.get('otp_aadhaar_number', '')
        if not aadhaar_number:
            # If no Aadhaar number in session, redirect to OTP request page
            return redirect('auth:citizen_aadhaar_otp_request')
        
        return render(request, 'citizen_aadhaar_otp_verify.html', {
            'aadhaar_number': aadhaar_number
        })

def citizen_registration(request):
    """Citizen registration view - allows new citizens to register with mobile number"""
    # If user is already authenticated, redirect to appropriate dashboard
    if request.user.is_authenticated:
        if request.user.user_type == 'admin':
            return redirect('auth:admin_dashboard')
        elif request.user.user_type == 'clerk':
            return redirect('auth:clerk_dashboard')
        elif request.user.user_type == 'citizen':
            return redirect('auth:citizen_dashboard')
    
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()
            
            # Create citizen profile with additional fields
            citizen_profile = CitizenProfile(
                user=user,
                aadhaar_number=form.cleaned_data['aadhaar_number'],
                address=form.cleaned_data.get('address', 'Not provided')
            )
            citizen_profile.save()
            
            messages.success(request, "Registration successful! You can now log in using your mobile number.")
            return redirect('auth:citizen_otp_request')
    else:
        form = CitizenRegistrationForm()
    
    return render(request, 'citizen_registration.html', {'form': form})

@citizen_required
def citizen_dashboard(request):
    """Citizen dashboard view"""
    return render(request, 'citizen_dashboard.html')

@clerk_required
def clerk_dashboard(request):
    """Clerk dashboard view"""
    return render(request, 'clerk_dashboard.html')

@admin_required
def admin_dashboard(request):
    """Admin dashboard view"""
    # Additional context for the admin dashboard
    context = {
        'total_clerks': 12,
        'total_citizens': 2458,
        'active_schemes': 18,
        'pending_grievances': 42,
        'tax_collection': '₹12,45,000',
        'grievance_resolution_rate': '78%',
        'scheme_applications': 342
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def logout_view(request):
    """Logout view for all user types"""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')