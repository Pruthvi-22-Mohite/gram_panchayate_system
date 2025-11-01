from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import random
import json

from .models import CustomUser, OTP
from .decorators import citizen_required, clerk_required, admin_required

def home(request):
    """Home page view"""
    return render(request, 'index.html')

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
            
            # Generate 6-digit OTP using SMS service
            from authentication.sms import sms_service
            otp_code = sms_service.generate_otp()
            
            # Save OTP to database
            otp_instance = OTP(mobile_number=mobile_number, otp=otp_code)
            otp_instance.save()
            
            # Send OTP via SMS
            if sms_service.send_otp(mobile_number, otp_code):
                return JsonResponse({
                    'success': True, 
                    'message': 'OTP sent successfully.'
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'Failed to send OTP. Please try again.'
                })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})