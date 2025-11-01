from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import random
import json

from gram_panchayate_system.models import CustomUser, OTP
from gram_panchayate_system.forms import CustomLoginForm, CitizenOTPRequestForm, CitizenOTPVerificationForm
from gram_panchayate_system.decorators import citizen_required, clerk_required, admin_required

def home(request):
    """Home page view"""
    return render(request, 'index.html')

def login_view(request):
    """Main login page view"""
    return render(request, 'login.html')

def admin_login(request):
    """Admin login view"""
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.user_type == 'admin':
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid credentials or not an admin user.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = CustomLoginForm()
    
    return render(request, 'admin_login.html', {'form': form})

def clerk_login(request):
    """Clerk login view"""
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.user_type == 'clerk':
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('clerk_dashboard')
            else:
                messages.error(request, "Invalid credentials or not a clerk user.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = CustomLoginForm()
    
    return render(request, 'clerk_login.html', {'form': form})

def citizen_otp_request(request):
    """Citizen OTP request view"""
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
            
            # Generate 6-digit OTP
            otp_code = str(random.randint(100000, 999999))
            
            # Save OTP to database
            otp_instance = OTP(mobile_number=mobile_number, otp=otp_code)
            otp_instance.save()
            
            # In a real application, you would send the OTP via SMS
            # For demo purposes, we'll just show it in a message
            messages.info(request, f"OTP sent to your mobile number. For demo purposes, OTP is: {otp_code}")
            
            # Redirect to OTP verification page
            return render(request, 'citizen_otp_verify.html', {
                'form': CitizenOTPVerificationForm(initial={'mobile_number': mobile_number}),
                'mobile_number': mobile_number
            })
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
                    return render(request, 'citizen_otp_request.html', {'form': CitizenOTPRequestForm()})
                
                # Mark OTP as used
                otp_record.is_used = True
                otp_record.save()
                
                # Authenticate user
                try:
                    user = CustomUser.objects.get(mobile_number=mobile_number, user_type='citizen')
                    login(request, user)
                    messages.success(request, f"Welcome, {user.username}!")
                    return redirect('citizen_dashboard')
                except ObjectDoesNotExist:
                    messages.error(request, "User account not found.")
                    return render(request, 'citizen_otp_request.html', {'form': CitizenOTPRequestForm()})
                    
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
    
    # If not POST, redirect to OTP request page
    return redirect('citizen_otp_request')

@login_required
def logout_view(request):
    """Logout view for all user types"""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')

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
    return render(request, 'admin_dashboard.html')

def pay_tax(request):
    """Pay tax view"""
    return render(request, 'pay_tax.html')

def lodge_grievance(request):
    """Lodge grievance view"""
    return render(request, 'lodge_grievance.html')

def view_schemes(request):
    """View schemes view"""
    return render(request, 'view_schemes.html')

def emergency_directory(request):
    """Emergency directory view"""
    return render(request, 'emergency_directory.html')

def feedback_suggestions(request):
    """Feedback and suggestions view"""
    return render(request, 'feedback_suggestions.html')

def view_budget(request):
    """View budget view"""
    return render(request, 'view_budget.html')

# API endpoint for sending OTP (for AJAX requests)
@csrf_exempt
def send_otp_api(request):
    """API endpoint to send OTP"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mobile_number = data.get('mobile_number')
            
            if not mobile_number:
                return JsonResponse({'success': False, 'message': 'Mobile number is required.'})
            
            # Check if user with this mobile number exists
            try:
                user = CustomUser.objects.get(mobile_number=mobile_number, user_type='citizen')
            except ObjectDoesNotExist:
                return JsonResponse({'success': False, 'message': 'No citizen account found with this mobile number.'})
            
            # Generate 6-digit OTP
            otp_code = str(random.randint(100000, 999999))
            
            # Save OTP to database
            otp_instance = OTP(mobile_number=mobile_number, otp=otp_code)
            otp_instance.save()
            
            # In a real application, you would send the OTP via SMS
            # For demo purposes, we'll just return success
            return JsonResponse({
                'success': True, 
                'message': 'OTP sent successfully.',
                'demo_otp': otp_code  # For demo purposes only
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})