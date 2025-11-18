from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from .models import Asset, Project
from .forms import AssetForm, ProjectForm


# Public Views
def asset_project_list(request):
    """Public view for assets and projects"""
    # Get filter parameters
    asset_type = request.GET.get('asset_type', '')
    project_status = request.GET.get('project_status', '')
    search_query = request.GET.get('search', '')
    
    # Filter assets
    assets = Asset.objects.filter(is_active=True)
    if asset_type:
        assets = assets.filter(asset_type=asset_type)
    if search_query:
        assets = assets.filter(
            Q(asset_name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Filter projects
    projects = Project.objects.all()
    if project_status:
        projects = projects.filter(status=project_status)
    if search_query:
        projects = projects.filter(
            Q(project_name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Statistics
    total_assets = Asset.objects.filter(is_active=True).count()
    total_projects = Project.objects.count()
    ongoing_projects = Project.objects.filter(status='ongoing').count()
    completed_projects = Project.objects.filter(status='completed').count()
    
    context = {
        'assets': assets[:12],
        'projects': projects[:12],
        'asset_types': Asset.ASSET_TYPE_CHOICES,
        'project_statuses': Project.STATUS_CHOICES,
        'selected_asset_type': asset_type,
        'selected_project_status': project_status,
        'search_query': search_query,
        'total_assets': total_assets,
        'total_projects': total_projects,
        'ongoing_projects': ongoing_projects,
        'completed_projects': completed_projects,
    }
    return render(request, 'asset_project_tracker/public_list.html', context)


def project_detail(request, pk):
    """Public view for project details"""
    project = get_object_or_404(Project, pk=pk)
    context = {'project': project}
    return render(request, 'asset_project_tracker/project_detail.html', context)


def asset_detail(request, pk):
    """Public view for asset details"""
    asset = get_object_or_404(Asset, pk=pk)
    context = {'asset': asset}
    return render(request, 'asset_project_tracker/asset_detail.html', context)


# Admin/Clerk Management Views
@login_required
def manage_assets(request):
    """Admin/Clerk view to manage assets"""
    if request.user.user_type not in ['admin', 'clerk']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('common:index')
    
    assets = Asset.objects.all().order_by('-created_at')
    
    # Apply filters
    asset_type = request.GET.get('asset_type', '')
    condition = request.GET.get('condition', '')
    search_query = request.GET.get('search', '')
    
    if asset_type:
        assets = assets.filter(asset_type=asset_type)
    if condition:
        assets = assets.filter(condition=condition)
    if search_query:
        assets = assets.filter(
            Q(asset_name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {
        'assets': assets,
        'asset_types': Asset.ASSET_TYPE_CHOICES,
        'conditions': Asset.CONDITION_CHOICES,
        'selected_asset_type': asset_type,
        'selected_condition': condition,
        'search_query': search_query,
    }
    return render(request, 'asset_project_tracker/manage_assets.html', context)


@login_required
def add_asset(request):
    """Add new asset"""
    if request.user.user_type not in ['admin', 'clerk']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('common:index')
    
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.created_by = request.user
            asset.save()
            messages.success(request, 'Asset added successfully!')
            return redirect('asset_project_tracker:manage_assets')
    else:
        form = AssetForm()
    
    context = {'form': form, 'title': 'Add New Asset'}
    return render(request, 'asset_project_tracker/asset_form.html', context)


@login_required
def edit_asset(request, pk):
    """Edit existing asset"""
    if request.user.user_type not in ['admin', 'clerk']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('common:index')
    
    asset = get_object_or_404(Asset, pk=pk)
    
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset updated successfully!')
            return redirect('asset_project_tracker:manage_assets')
    else:
        form = AssetForm(instance=asset)
    
    context = {'form': form, 'title': 'Edit Asset', 'asset': asset}
    return render(request, 'asset_project_tracker/asset_form.html', context)


@login_required
def delete_asset(request, pk):
    """Delete asset"""
    if request.user.user_type not in ['admin', 'clerk']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('common:index')
    
    asset = get_object_or_404(Asset, pk=pk)
    
    if request.method == 'POST':
        asset.delete()
        messages.success(request, 'Asset deleted successfully!')
        return redirect('asset_project_tracker:manage_assets')
    
    context = {'asset': asset}
    return render(request, 'asset_project_tracker/delete_asset.html', context)


@login_required
def manage_projects(request):
    """Admin/Clerk view to manage projects"""
    if request.user.user_type not in ['admin', 'clerk']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('common:index')
    
    projects = Project.objects.all().order_by('-created_at')
    
    # Apply filters
    project_type = request.GET.get('project_type', '')
    status = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    if project_type:
        projects = projects.filter(project_type=project_type)
    if status:
        projects = projects.filter(status=status)
    if search_query:
        projects = projects.filter(
            Q(project_name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {
        'projects': projects,
        'project_types': Project.PROJECT_TYPE_CHOICES,
        'statuses': Project.STATUS_CHOICES,
        'selected_project_type': project_type,
        'selected_status': status,
        'search_query': search_query,
    }
    return render(request, 'asset_project_tracker/manage_projects.html', context)


@login_required
def add_project(request):
    """Add new project"""
    if request.user.user_type not in ['admin', 'clerk']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('common:index')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project added successfully!')
            return redirect('asset_project_tracker:manage_projects')
    else:
        form = ProjectForm()
    
    context = {'form': form, 'title': 'Add New Project'}
    return render(request, 'asset_project_tracker/project_form.html', context)


@login_required
def edit_project(request, pk):
    """Edit existing project"""
    if request.user.user_type not in ['admin', 'clerk']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('common:index')
    
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('asset_project_tracker:manage_projects')
    else:
        form = ProjectForm(instance=project)
    
    context = {'form': form, 'title': 'Edit Project', 'project': project}
    return render(request, 'asset_project_tracker/project_form.html', context)


@login_required
def delete_project(request, pk):
    """Delete project"""
    if request.user.user_type not in ['admin', 'clerk']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('common:index')
    
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('asset_project_tracker:manage_projects')
    
    context = {'project': project}
    return render(request, 'asset_project_tracker/delete_project.html', context)
