from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from modules.common.models import CustomUser
from modules.common.decorators import admin_required
from .models import AdminProfile, SystemSettings, AuditLog
from .forms import AdminLoginForm, SystemSettingsForm, ClerkCreationForm
from modules.clerk.models import ClerkProfile
from modules.citizen.models import CitizenProfile


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
def system_settings(request):
    """View to manage system settings"""
    if request.method == 'POST':
        form = SystemSettingsForm(request.POST)
        if form.is_valid():
            setting = form.save()
            
            # Log the settings change
            AuditLog.objects.create(
                admin_user=request.user,
                action="System Settings Updated",
                target_model="SystemSettings",
                target_id=str(setting.id),
                details=f"Updated setting: {setting.setting_key}"
            )
            
            messages.success(request, "Settings updated successfully!")
            return redirect('admin_module:system_settings')
    else:
        form = SystemSettingsForm()
    
    settings = SystemSettings.objects.all().order_by('setting_key')
    
    context = {
        'form': form,
        'settings': settings
    }
    return render(request, 'admin/system_settings.html', context)


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
    
    context = {
        'user_trends': user_trends
    }
    return render(request, 'admin/reports.html', context)