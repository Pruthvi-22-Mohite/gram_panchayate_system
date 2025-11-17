from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone

from modules.common.models import CustomUser
from modules.common.decorators import clerk_required
from .models import ClerkProfile, Scheme, SchemeApplication, Grievance, TaxRecord
from .forms import ClerkLoginForm, SchemeForm, GrievanceResponseForm, TaxRecordForm
from modules.informationhub.models import VillageNotice, MeetingSchedule
from modules.informationhub.forms import VillageNoticeForm, MeetingScheduleForm
from modules.citizen.models import FeedbackSuggestion
from modules.citizen.forms import FeedbackResponseForm


def clerk_login(request):
    """Clerk login view"""
    if request.user.is_authenticated and request.user.user_type == 'clerk':
        return redirect('clerk:dashboard')
        
    if request.method == 'POST':
        form = ClerkLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.user_type == 'clerk':
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('clerk:dashboard')
            else:
                messages.error(request, "Invalid credentials or not a clerk user.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = ClerkLoginForm()
    
    return render(request, 'clerk/login.html', {'form': form})


@clerk_required
def clerk_dashboard(request):
    """Clerk dashboard view with work statistics"""
    
    # Get clerk's work statistics
    pending_applications = SchemeApplication.objects.filter(
        status='pending'
    ).count()
    
    open_grievances = Grievance.objects.filter(
        status__in=['open', 'in_progress']
    ).count()
    
    pending_taxes = TaxRecord.objects.filter(
        status='pending'
    ).count()
    
    # Get recent activities
    recent_applications = SchemeApplication.objects.filter(
        status='pending'
    ).order_by('-applied_at')[:5]
    
    recent_grievances = Grievance.objects.filter(
        status__in=['open', 'in_progress']
    ).order_by('-submitted_at')[:5]
    
    context = {
        'pending_applications': pending_applications,
        'open_grievances': open_grievances,
        'pending_taxes': pending_taxes,
        'recent_applications': recent_applications,
        'recent_grievances': recent_grievances,
    }
    return render(request, 'clerk/dashboard.html', context)


@clerk_required
def manage_schemes(request):
    """View to manage government schemes"""
    if request.method == 'POST':
        form = SchemeForm(request.POST, request.FILES)
        if form.is_valid():
            scheme = form.save(commit=False)
            scheme.created_by = request.user
            scheme.save()
            messages.success(request, "Scheme created successfully!")
            return redirect('clerk:manage_schemes')
    else:
        form = SchemeForm()
    
    schemes = Scheme.objects.all().order_by('-created_at')
    
    context = {
        'form': form,
        'schemes': schemes
    }
    return render(request, 'clerk/manage_schemes.html', context)


@clerk_required
def edit_scheme(request, scheme_id):
    """View to edit an existing scheme"""
    scheme = get_object_or_404(Scheme, id=scheme_id)
    
    # Check if the user is the creator or an admin
    if request.user != scheme.created_by and request.user.user_type != 'admin':
        messages.error(request, "You don't have permission to edit this scheme.")
        return redirect('clerk:manage_schemes')
    
    if request.method == 'POST':
        form = SchemeForm(request.POST, request.FILES, instance=scheme)
        if form.is_valid():
            form.save()
            messages.success(request, "Scheme updated successfully!")
            return redirect('clerk:manage_schemes')
    else:
        form = SchemeForm(instance=scheme)
    
    context = {
        'form': form,
        'scheme': scheme
    }
    return render(request, 'clerk/edit_scheme.html', context)


@clerk_required
def delete_scheme(request, scheme_id):
    """View to delete a scheme"""
    scheme = get_object_or_404(Scheme, id=scheme_id)
    
    # Check if the user is the creator or an admin
    if request.user != scheme.created_by and request.user.user_type != 'admin':
        messages.error(request, "You don't have permission to delete this scheme.")
        return redirect('clerk:manage_schemes')
    
    if request.method == 'POST':
        scheme.delete()
        messages.success(request, "Scheme deleted successfully!")
        return redirect('clerk:manage_schemes')
    
    context = {
        'scheme': scheme
    }
    return render(request, 'clerk/delete_scheme.html', context)


@clerk_required
def toggle_scheme_status(request, scheme_id):
    """View to activate/deactivate a scheme"""
    scheme = get_object_or_404(Scheme, id=scheme_id)
    
    # Check if the user is the creator or an admin
    if request.user != scheme.created_by and request.user.user_type != 'admin':
        messages.error(request, "You don't have permission to modify this scheme.")
        return redirect('clerk:manage_schemes')
    
    scheme.is_active = not scheme.is_active
    scheme.save()
    
    status = "activated" if scheme.is_active else "deactivated"
    messages.success(request, f"Scheme {status} successfully!")
    return redirect('clerk:manage_schemes')


@clerk_required
def scheme_applications(request):
    """View to handle scheme applications"""
    applications = SchemeApplication.objects.all().order_by('-applied_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    context = {
        'applications': applications,
        'status_filter': status_filter
    }
    return render(request, 'clerk/scheme_applications.html', context)


@clerk_required
def review_application(request, application_id):
    """View to review a specific scheme application"""
    application = get_object_or_404(SchemeApplication, id=application_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        notes = request.POST.get('review_notes', '')
        
        if status in ['approved', 'rejected']:
            application.status = status
            application.reviewed_by = request.user
            application.review_notes = notes
            application.reviewed_at = timezone.now()
            application.save()
            
            messages.success(request, f"Application {status} successfully!")
            return redirect('clerk:scheme_applications')
    
    context = {
        'application': application
    }
    return render(request, 'clerk/review_application.html', context)


@clerk_required
def manage_grievances(request):
    """View to manage citizen grievances"""
    grievances = Grievance.objects.all().order_by('-submitted_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        grievances = grievances.filter(status=status_filter)
    
    context = {
        'grievances': grievances,
        'status_filter': status_filter
    }
    return render(request, 'clerk/manage_grievances.html', context)


@clerk_required
def respond_grievance(request, grievance_id):
    """View to respond to a specific grievance"""
    grievance = get_object_or_404(Grievance, id=grievance_id)
    
    if request.method == 'POST':
        form = GrievanceResponseForm(request.POST, instance=grievance)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.assigned_to = request.user
            if grievance.status == 'resolved':
                grievance.resolved_at = timezone.now()
            grievance.save()
            
            messages.success(request, "Grievance updated successfully!")
            return redirect('clerk:manage_grievances')
    else:
        form = GrievanceResponseForm(instance=grievance)
    
    context = {
        'grievance': grievance,
        'form': form
    }
    return render(request, 'clerk/respond_grievance.html', context)


@clerk_required
def manage_taxes(request):
    """View to manage tax records"""
    if request.method == 'POST':
        form = TaxRecordForm(request.POST)
        if form.is_valid():
            tax_record = form.save(commit=False)
            tax_record.created_by = request.user
            tax_record.save()
            messages.success(request, "Tax record created successfully!")
            return redirect('clerk:manage_taxes')
    else:
        form = TaxRecordForm()
    
    tax_records = TaxRecord.objects.all().order_by('-created_at')
    
    context = {
        'form': form,
        'tax_records': tax_records
    }
    return render(request, 'clerk/manage_taxes.html', context)


@clerk_required
def reports(request):
    """View to display clerk reports"""
    # Application statistics
    app_stats = SchemeApplication.objects.values('status').annotate(
        count=Count('id')
    )
    
    # Grievance statistics
    grievance_stats = Grievance.objects.values('status').annotate(
        count=Count('id')
    )
    
    # Tax collection statistics
    tax_stats = TaxRecord.objects.values('status').annotate(
        count=Count('id')
    )
    
    context = {
        'app_stats': app_stats,
        'grievance_stats': grievance_stats,
        'tax_stats': tax_stats
    }
    return render(request, 'clerk/reports.html', context)


# Information Hub Management Views

@clerk_required
def manage_notices(request):
    """View to manage village notices"""
    if request.method == 'POST':
        form = VillageNoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save()
            messages.success(request, "Notice created successfully!")
            return redirect('clerk:manage_notices')
    else:
        form = VillageNoticeForm()
    
    notices = VillageNotice.objects.all().order_by('-date')
    
    context = {
        'form': form,
        'notices': notices
    }
    return render(request, 'clerk/manage_notices.html', context)


@clerk_required
def edit_notice(request, notice_id):
    """View to edit an existing notice"""
    notice = get_object_or_404(VillageNotice, id=notice_id)
    
    if request.method == 'POST':
        form = VillageNoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, "Notice updated successfully!")
            return redirect('clerk:manage_notices')
    else:
        form = VillageNoticeForm(instance=notice)
    
    context = {
        'form': form,
        'notice': notice
    }
    return render(request, 'clerk/edit_notice.html', context)


@clerk_required
def delete_notice(request, notice_id):
    """View to delete a notice"""
    notice = get_object_or_404(VillageNotice, id=notice_id)
    
    if request.method == 'POST':
        notice.delete()
        messages.success(request, "Notice deleted successfully!")
        return redirect('clerk:manage_notices')
    
    context = {
        'notice': notice
    }
    return render(request, 'clerk/delete_notice.html', context)


@clerk_required
def manage_meetings(request):
    """View to manage meeting schedules"""
    if request.method == 'POST':
        form = MeetingScheduleForm(request.POST)
        if form.is_valid():
            meeting = form.save()
            messages.success(request, "Meeting created successfully!")
            return redirect('clerk:manage_meetings')
    else:
        form = MeetingScheduleForm()
    
    meetings = MeetingSchedule.objects.all().order_by('-meeting_date')
    
    context = {
        'form': form,
        'meetings': meetings
    }
    return render(request, 'clerk/manage_meetings.html', context)


@clerk_required
def edit_meeting(request, meeting_id):
    """View to edit an existing meeting"""
    meeting = get_object_or_404(MeetingSchedule, id=meeting_id)
    
    if request.method == 'POST':
        form = MeetingScheduleForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, "Meeting updated successfully!")
            return redirect('clerk:manage_meetings')
    else:
        form = MeetingScheduleForm(instance=meeting)
    
    context = {
        'form': form,
        'meeting': meeting
    }
    return render(request, 'clerk/edit_meeting.html', context)


@clerk_required
def delete_meeting(request, meeting_id):  
    """View to delete a meeting"""
    meeting = get_object_or_404(MeetingSchedule, id=meeting_id)
    
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, "Meeting deleted successfully!")
        return redirect('clerk:manage_meetings')
    
    context = {
        'meeting': meeting
    }
    return render(request, 'clerk/delete_meeting.html', context)


# ==================== FEEDBACK & SUGGESTIONS MANAGEMENT ====================

@clerk_required
def manage_feedback(request):
    """View all citizen feedback and suggestions"""
    feedbacks = FeedbackSuggestion.objects.all().select_related('citizen', 'responded_by').order_by('-submitted_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        feedbacks = feedbacks.filter(status=status_filter)
    
    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        feedbacks = feedbacks.filter(feedback_type=type_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        feedbacks = feedbacks.filter(
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(citizen__username__icontains=search_query)
        )
    
    context = {
        'feedbacks': feedbacks,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'search_query': search_query,
    }
    return render(request, 'clerk/manage_feedback.html', context)


@clerk_required
def feedback_detail(request, feedback_id):
    """View and respond to specific feedback"""
    feedback = get_object_or_404(FeedbackSuggestion, id=feedback_id)
    
    if request.method == 'POST':
        form = FeedbackResponseForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback_obj = form.save(commit=False)
            feedback_obj.responded_by = request.user
            feedback_obj.responded_at = timezone.now()
            feedback_obj.save()
            messages.success(request, "Response added successfully!")
            return redirect('clerk:manage_feedback')
    else:
        form = FeedbackResponseForm(instance=feedback)
    
    context = {
        'feedback': feedback,
        'form': form
    }
    return render(request, 'clerk/feedback_detail.html', context)