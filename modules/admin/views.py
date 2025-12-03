from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta

from modules.common.models import CustomUser
from modules.common.decorators import admin_required
from .models import AdminProfile, SystemSettings, AuditLog
from .forms import AdminLoginForm, ClerkCreationForm
from modules.clerk.models import ClerkProfile, Grievance, Scheme
from modules.clerk.forms import SchemeForm
from modules.citizen.models import CitizenProfile, FeedbackSuggestion
from modules.citizen.forms import FeedbackResponseForm
from modules.informationhub.models import VillageNotice, MeetingSchedule
from modules.informationhub.forms import VillageNoticeForm, MeetingScheduleForm


def admin_login(request):
    """Admin login view - requires superuser credentials"""
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_module:dashboard')
        
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_superuser:
                login(request, user)
                
                # Ensure user has admin type and profile
                if not hasattr(user, 'user_type') or user.user_type != 'admin':
                    user.user_type = 'admin'
                    user.save()
                
                # Create admin profile if it doesn't exist
                admin_profile, created = AdminProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'designation': 'System Administrator',
                        'department': 'Administration'
                    }
                )
                
                # Log the login action
                AuditLog.objects.create(
                    admin_user=user,
                    action="Admin Login",
                    details=f"Admin {user.username} logged in"
                )
                
                messages.success(request, f"Welcome, Administrator {user.username}!")
                return redirect('admin_module:dashboard')
            else:
                messages.error(request, "Invalid credentials. Admin access requires superuser privileges.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin/login.html', {'form': form})


@admin_required
def admin_dashboard(request):
    """Admin dashboard view with system statistics"""
    
    # Get system statistics
    total_clerks = ClerkProfile.objects.count()
    total_citizens = CitizenProfile.objects.count()
    total_users = CustomUser.objects.count()
    
    # Get recent registrations (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_citizens = CitizenProfile.objects.filter(
        user__created_at__gte=thirty_days_ago
    ).count()
    
    # Get user type distribution
    user_stats = CustomUser.objects.values('user_type').annotate(
        count=Count('user_type')
    )
    
    # Get recent audit logs
    recent_logs = AuditLog.objects.filter(
        admin_user=request.user
    ).order_by('-timestamp')[:10]
    
    context = {
        'total_clerks': total_clerks,
        'total_citizens': total_citizens,
        'total_users': total_users,
        'recent_citizens': recent_citizens,
        'user_stats': user_stats,
        'recent_logs': recent_logs,
        'active_schemes': 18,  # This would come from a schemes model
        'pending_grievances': 42,  # This would come from a grievances model
        'tax_collection': '₹12,45,000',  # This would come from a tax model
        'grievance_resolution_rate': '78%',  # Calculated from grievances
        'scheme_applications': 342  # This would come from applications model
    }
    return render(request, 'admin/dashboard.html', context)


@admin_required
def manage_users(request):
    """View to manage all users in the system"""
    users = CustomUser.objects.all().order_by('-created_at')
    
    context = {
        'users': users,
        'total_users': users.count()
    }
    return render(request, 'admin/manage_users.html', context)


@admin_required
def manage_clerks(request):
    """View to manage clerk users"""
    clerks = ClerkProfile.objects.select_related('user').all()
    
    context = {
        'clerks': clerks,
        'total_clerks': clerks.count()
    }
    return render(request, 'admin/manage_clerks.html', context)


@admin_required
def create_clerk(request):
    """View to create new clerk account"""
    if request.method == 'POST':
        form = ClerkCreationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()
            
            # Create clerk profile
            clerk_profile = ClerkProfile.objects.create(
                user=user,
                panchayat_name=form.cleaned_data['panchayat_name'],
                designation=form.cleaned_data.get('designation', ''),
                employee_id=form.cleaned_data['employee_id']
            )
            
            # Log the action
            AuditLog.objects.create(
                admin_user=request.user,
                action="Clerk Account Created",
                target_model="ClerkProfile",
                target_id=str(clerk_profile.user.id),
                details=f"Created clerk account for {user.username} (Employee ID: {clerk_profile.employee_id})"
            )
            
            messages.success(request, f"Clerk account created successfully! Username: {user.username}")
            return redirect('admin_module:manage_clerks')
    else:
        form = ClerkCreationForm()
    
    context = {
        'form': form
    }
    return render(request, 'admin/create_clerk.html', context)


@admin_required
def manage_citizens(request):
    """View to manage citizen users"""
    citizens = CitizenProfile.objects.select_related('user').all()
    
    context = {
        'citizens': citizens,
        'total_citizens': citizens.count()
    }
    return render(request, 'admin/manage_citizens.html', context)


@admin_required
def audit_logs(request):
    """View to display audit logs"""
    logs = AuditLog.objects.all().order_by('-timestamp')
    
    context = {
        'logs': logs
    }
    return render(request, 'admin/audit_logs.html', context)


@admin_required
def reports(request):
    """View to display various system reports"""
    # User registration trends
    user_trends = CustomUser.objects.extra(
        select={'month': 'EXTRACT(month FROM created_at)'}
    ).values('month').annotate(count=Count('id'))
    
    # Get counts for KPIs
    total_users = CustomUser.objects.count()
    total_clerks = ClerkProfile.objects.count()
    total_citizens = CitizenProfile.objects.count()
    
    # Get recent audit logs
    recent_logs = AuditLog.objects.all().order_by('-timestamp')[:10]
    
    context = {
        'user_trends': user_trends,
        'total_users': total_users,
        'total_clerks': total_clerks,
        'total_citizens': total_citizens,
        'recent_logs': recent_logs
    }
    return render(request, 'admin/reports.html', context)


@admin_required
def reports_data(request):
    """API endpoint for dynamic reports data"""
    data_type = request.GET.get('type', 'summary')
    
    if data_type == 'kpi':
        # KPI data
        total_users = CustomUser.objects.count()
        total_clerks = ClerkProfile.objects.count()
        total_citizens = CitizenProfile.objects.count()
        
        # Calculate growth from last month
        last_month = timezone.now() - timedelta(days=30)
        users_last_month = CustomUser.objects.filter(created_at__lt=last_month).count()
        clerks_last_month = ClerkProfile.objects.filter(user__created_at__lt=last_month).count()
        citizens_last_month = CitizenProfile.objects.filter(user__created_at__lt=last_month).count()
        
        # Calculate percentage changes
        user_growth = round(((total_users - users_last_month) / users_last_month * 100) if users_last_month > 0 else 0, 1)
        clerk_growth = round(((total_clerks - clerks_last_month) / clerks_last_month * 100) if clerks_last_month > 0 else 0, 1)
        citizen_growth = round(((total_citizens - citizens_last_month) / citizens_last_month * 100) if citizens_last_month > 0 else 0, 1)
        
        data = {
            'total_users': total_users,
            'total_clerks': total_clerks,
            'total_citizens': total_citizens,
            'user_growth': user_growth,
            'clerk_growth': clerk_growth,
            'citizen_growth': citizen_growth
        }
    elif data_type == 'charts':
        # Chart data
        user_trends = CustomUser.objects.extra(
            select={'month': 'EXTRACT(month FROM created_at)'}
        ).values('month').annotate(count=Count('id'))
        
        # Format for chart
        months = []
        counts = []
        for item in user_trends:
            months.append(f"Month {int(item['month'])}")
            counts.append(item['count'])
        
        # User distribution
        citizen_count = CitizenProfile.objects.count()
        clerk_count = ClerkProfile.objects.count()
        admin_count = CustomUser.objects.filter(user_type='admin').count()
        
        data = {
            'registration_trends': {
                'labels': months,
                'data': counts
            },
            'user_distribution': {
                'labels': ['Citizens', 'Clerks', 'Admins'],
                'data': [citizen_count, clerk_count, admin_count]
            }
        }
    elif data_type == 'summary':
        # Summary table data
        data = [
            {'metric': 'Total Users', 'current': CustomUser.objects.count(), 'previous': 2567, 'change': '+10.8%'},
            {'metric': 'Total Clerks', 'current': ClerkProfile.objects.count(), 'previous': 38, 'change': '+10.5%'},
            {'metric': 'Total Citizens', 'current': CitizenProfile.objects.count(), 'previous': 2524, 'change': '+10.9%'},
            {'metric': 'Grievances Submitted', 'current': 342, 'previous': 298, 'change': '+14.8%'},
            {'metric': 'Grievances Resolved', 'current': 287, 'previous': 245, 'change': '+17.1%'},
            {'metric': 'Tax Collections (₹)', 'current': '12,45,000', 'previous': '10,87,500', 'change': '+14.5%'}
        ]
        return JsonResponse(data, safe=False)
    elif data_type == 'activity':
        # Recent activity data
        logs = AuditLog.objects.all().order_by('-timestamp')[:10]
        data = []
        for log in logs:
            data.append({
                'activity': log.action,
                'user': log.admin_user.username,
                'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M'),
                'details': log.details,
                'status': 'success' if 'created' in log.action.lower() or 'updated' in log.action.lower() else 'info'
            })
        return JsonResponse(data, safe=False)
    else:
        data = {'error': 'Invalid data type'}
    
    return JsonResponse(data)


@admin_required
def manage_grievances(request):
    """View to manage all citizen grievances"""
    grievances = Grievance.objects.all().order_by('-submitted_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        grievances = grievances.filter(status=status_filter)
    
    context = {
        'grievances': grievances,
        'status_filter': status_filter
    }
    return render(request, 'admin/manage_grievances.html', context)


@admin_required
def manage_schemes(request):
    """View to manage all government schemes"""
    if request.method == 'POST':
        form = SchemeForm(request.POST, request.FILES)
        if form.is_valid():
            scheme = form.save(commit=False)
            scheme.created_by = request.user
            scheme.save()
            messages.success(request, "Scheme created successfully!")
            return redirect('admin_module:manage_schemes')
    else:
        form = SchemeForm()
    
    schemes = Scheme.objects.all().order_by('-created_at')
    
    context = {
        'schemes': schemes,
        'form': form
    }
    return render(request, 'admin/manage_schemes.html', context)


@admin_required
def edit_scheme(request, scheme_id):
    """View to edit an existing scheme"""
    scheme = get_object_or_404(Scheme, id=scheme_id)
    
    if request.method == 'POST':
        form = SchemeForm(request.POST, request.FILES, instance=scheme)
        if form.is_valid():
            form.save()
            messages.success(request, "Scheme updated successfully!")
            return redirect('admin_module:manage_schemes')
    else:
        form = SchemeForm(instance=scheme)
    
    context = {
        'form': form,
        'scheme': scheme
    }
    return render(request, 'admin/edit_scheme.html', context)


@admin_required
def delete_scheme(request, scheme_id):
    """View to delete a scheme"""
    scheme = get_object_or_404(Scheme, id=scheme_id)
    
    if request.method == 'POST':
        scheme.delete()
        messages.success(request, "Scheme deleted successfully!")
        return redirect('admin_module:manage_schemes')
    
    context = {
        'scheme': scheme
    }
    return render(request, 'admin/delete_scheme.html', context)


@admin_required
def toggle_scheme_status(request, scheme_id):
    """View to activate/deactivate a scheme"""
    scheme = get_object_or_404(Scheme, id=scheme_id)
    
    scheme.is_active = not scheme.is_active
    scheme.save()
    
    status = "activated" if scheme.is_active else "deactivated"
    messages.success(request, f"Scheme {status} successfully!")
    return redirect('admin_module:manage_schemes')


# Information Hub Management Views

@admin_required
def manage_notices(request):
    """View to manage village notices"""
    if request.method == 'POST':
        form = VillageNoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save()
            messages.success(request, "Notice created successfully!")
            return redirect('admin_module:manage_notices')
    else:
        form = VillageNoticeForm()
    
    notices = VillageNotice.objects.all().order_by('-date')
    
    context = {
        'form': form,
        'notices': notices
    }
    return render(request, 'admin/manage_notices.html', context)


@admin_required
def edit_notice(request, notice_id):
    """View to edit an existing notice"""
    notice = get_object_or_404(VillageNotice, id=notice_id)
    
    if request.method == 'POST':
        form = VillageNoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, "Notice updated successfully!")
            return redirect('admin_module:manage_notices')
    else:
        form = VillageNoticeForm(instance=notice)
    
    context = {
        'form': form,
        'notice': notice
    }
    return render(request, 'admin/edit_notice.html', context)


@admin_required
def delete_notice(request, notice_id):
    """View to delete a notice"""
    notice = get_object_or_404(VillageNotice, id=notice_id)
    
    if request.method == 'POST':
        notice.delete()
        messages.success(request, "Notice deleted successfully!")
        return redirect('admin_module:manage_notices')
    
    context = {
        'notice': notice
    }
    return render(request, 'admin/delete_notice.html', context)


@admin_required
def manage_meetings(request):
    """View to manage meeting schedules"""
    if request.method == 'POST':
        form = MeetingScheduleForm(request.POST)
        if form.is_valid():
            meeting = form.save()
            messages.success(request, "Meeting created successfully!")
            return redirect('admin_module:manage_meetings')
    else:
        form = MeetingScheduleForm()
    
    meetings = MeetingSchedule.objects.all().order_by('-meeting_date')
    
    context = {
        'form': form,
        'meetings': meetings
    }
    return render(request, 'admin/manage_meetings.html', context)


@admin_required
def edit_meeting(request, meeting_id):
    """View to edit an existing meeting"""
    meeting = get_object_or_404(MeetingSchedule, id=meeting_id)
    
    if request.method == 'POST':
        form = MeetingScheduleForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, "Meeting updated successfully!")
            return redirect('admin_module:manage_meetings')
    else:
        form = MeetingScheduleForm(instance=meeting)
    
    context = {
        'form': form,
        'meeting': meeting
    }
    return render(request, 'admin/edit_meeting.html', context)


@admin_required
def delete_meeting(request, meeting_id):
    """View to delete a meeting"""
    meeting = get_object_or_404(MeetingSchedule, id=meeting_id)
    
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, "Meeting deleted successfully!")
        return redirect('admin_module:manage_meetings')
    
    context = {
        'meeting': meeting
    }
    return render(request, 'admin/delete_meeting.html', context)


# ==================== FEEDBACK & SUGGESTIONS MANAGEMENT ====================

@admin_required
def manage_feedback(request):
    """View and manage all citizen feedback and suggestions"""
    from django.db.models import Q
    
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
    return render(request, 'admin/manage_feedback.html', context)


@admin_required
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
            
            # Log the action
            AuditLog.objects.create(
                admin_user=request.user,
                action="Feedback Response Added",
                target_model="FeedbackSuggestion",
                target_id=str(feedback.id),
                details=f"Responded to feedback: {feedback.subject}"
            )
            
            messages.success(request, "Response added successfully!")
            return redirect('admin_module:manage_feedback')
    else:
        form = FeedbackResponseForm(instance=feedback)
    
    context = {
        'feedback': feedback,
        'form': form
    }
    return render(request, 'admin/feedback_detail.html', context)


@admin_required
def delete_feedback(request, feedback_id):
    """Delete a feedback entry"""
    feedback = get_object_or_404(FeedbackSuggestion, id=feedback_id)
    
    if request.method == 'POST':
        subject = feedback.subject
        feedback.delete()
        
        # Log the action
        AuditLog.objects.create(
            admin_user=request.user,
            action="Feedback Deleted",
            target_model="FeedbackSuggestion",
            target_id=str(feedback_id),
            details=f"Deleted feedback: {subject}"
        )
        
        messages.success(request, "Feedback deleted successfully!")
        return redirect('admin_module:manage_feedback')
    
    context = {
        'feedback': feedback
    }
    return render(request, 'admin/delete_feedback.html', context)
