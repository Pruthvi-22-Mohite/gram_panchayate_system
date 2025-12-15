from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.http import JsonResponse
from django.utils import timezone
from modules.informationhub.models import VillageNotice, MeetingSchedule


def home(request):
    """Home page view with public information"""
    # Get latest 5 active village notices
    latest_notices = VillageNotice.objects.filter(is_active=True).order_by('-date')[:5]
    
    # Get upcoming meetings
    today = timezone.now().date()
    upcoming_meetings = MeetingSchedule.objects.filter(
        meeting_date__gte=today,
        is_cancelled=False
    ).order_by('meeting_date', 'time')[:5]
    
    context = {
        'latest_notices': latest_notices,
        'upcoming_meetings': upcoming_meetings,
    }
    
    return render(request, 'common/index.html', context)


def login_view(request):
    """Main login page view - shows options for different user types"""
    # If user is already authenticated, redirect to appropriate dashboard
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.user_type == 'admin':
            return redirect('admin_module:dashboard')
        elif request.user.user_type == 'clerk':
            return redirect('clerk:dashboard')
        elif request.user.user_type == 'citizen':
            return redirect('citizen:dashboard')
    
    return render(request, 'common/login.html')


@login_required
def logout_view(request):
    """Logout view for all user types"""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('common:home')


def about(request):
    """About page view"""
    return render(request, 'common/about.html')


def contact(request):
    """Contact page view"""
    return render(request, 'common/contact.html')


def privacy_policy(request):
    """Privacy policy page view"""
    return render(request, 'common/privacy_policy.html')


def terms_of_service(request):
    """Terms of service page view"""
    return render(request, 'common/terms_of_service.html')


def switch_language(request):
    """View to switch the language"""
    if request.method == 'POST':
        language = request.POST.get('language', 'en')
        
        # Validate language
        if language in ['en', 'hi', 'mr']:
            # Set language in session
            request.session['django_language'] = language
            
            # Also set in cookie for persistence
            response = JsonResponse({'status': 'success'})
            response.set_cookie('django_language', language, max_age=30*24*60*60)  # 30 days
            
            return response
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
