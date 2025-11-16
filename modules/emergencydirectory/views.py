from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import EmergencyContact
from .forms import EmergencyContactForm


def is_admin_or_clerk(user):
    """Check if user is admin or clerk"""
    return user.is_authenticated and user.user_type in ['admin', 'clerk']


# Citizen Views (Read-Only)

def emergency_list(request):
    """
    Public view to list all emergency contacts
    Accessible to all users (including citizens)
    """
    contacts = EmergencyContact.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        contacts = contacts.filter(
            Q(contact_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    # Filter by type
    contact_type = request.GET.get('type', '')
    if contact_type:
        contacts = contacts.filter(contact_type=contact_type)
    
    # Filter by availability
    available_24x7 = request.GET.get('available_24x7', '')
    if available_24x7 == 'true':
        contacts = contacts.filter(available_24x7=True)
    
    context = {
        'contacts': contacts,
        'search_query': search_query,
        'contact_type': contact_type,
        'available_24x7': available_24x7,
        'contact_types': EmergencyContact.CONTACT_TYPE_CHOICES,
    }
    
    return render(request, 'emergencydirectory/emergency_list.html', context)


def emergency_detail(request, contact_id):
    """
    Public view to show detailed emergency contact information
    Accessible to all users
    """
    contact = get_object_or_404(EmergencyContact, id=contact_id, is_active=True)
    
    # Get related contacts (same type)
    related_contacts = EmergencyContact.objects.filter(
        contact_type=contact.contact_type,
        is_active=True
    ).exclude(id=contact.id)[:3]
    
    context = {
        'contact': contact,
        'related_contacts': related_contacts,
    }
    
    return render(request, 'emergencydirectory/emergency_detail.html', context)


# Admin/Clerk Views (CRUD Operations)

@user_passes_test(is_admin_or_clerk, login_url='/login/')
def manage_contacts(request):
    """
    Management view for admin and clerk to add/view contacts
    Protected: Only admin and clerk can access
    """
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f"Emergency contact '{contact.contact_name}' added successfully!")
            return redirect('emergencydirectory:manage_contacts')
    else:
        form = EmergencyContactForm()
    
    contacts = EmergencyContact.objects.all().order_by('-last_updated')
    
    context = {
        'form': form,
        'contacts': contacts,
    }
    
    # Render different templates based on user type
    if request.user.user_type == 'admin':
        return render(request, 'emergencydirectory/admin_manage.html', context)
    else:
        return render(request, 'emergencydirectory/clerk_manage.html', context)


@user_passes_test(is_admin_or_clerk, login_url='/login/')
def add_contact(request):
    """
    Add new emergency contact
    Protected: Only admin and clerk can access
    """
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f"Emergency contact '{contact.contact_name}' created successfully!")
            return redirect('emergencydirectory:manage_contacts')
    else:
        form = EmergencyContactForm()
    
    context = {
        'form': form,
        'action': 'Add'
    }
    
    return render(request, 'emergencydirectory/contact_form.html', context)


@user_passes_test(is_admin_or_clerk, login_url='/login/')
def edit_contact(request, contact_id):
    """
    Edit existing emergency contact
    Protected: Only admin and clerk can access
    """
    contact = get_object_or_404(EmergencyContact, id=contact_id)
    
    if request.method == 'POST':
        form = EmergencyContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, f"Emergency contact '{contact.contact_name}' updated successfully!")
            return redirect('emergencydirectory:manage_contacts')
    else:
        form = EmergencyContactForm(instance=contact)
    
    context = {
        'form': form,
        'contact': contact,
        'action': 'Edit'
    }
    
    return render(request, 'emergencydirectory/contact_form.html', context)


@user_passes_test(is_admin_or_clerk, login_url='/login/')
def delete_contact(request, contact_id):
    """
    Delete emergency contact
    Protected: Only admin and clerk can access
    """
    contact = get_object_or_404(EmergencyContact, id=contact_id)
    
    if request.method == 'POST':
        contact_name = contact.contact_name
        contact.delete()
        messages.success(request, f"Emergency contact '{contact_name}' deleted successfully!")
        return redirect('emergencydirectory:manage_contacts')
    
    context = {
        'contact': contact
    }
    
    return render(request, 'emergencydirectory/confirm_delete.html', context)


# Dashboard Widget View Helper
@login_required
def dashboard_widget_data(request):
    """
    Helper function to get emergency contacts for dashboard widget
    Returns top 4 important contacts
    """
    contacts = EmergencyContact.objects.filter(is_active=True).order_by('-available_24x7', 'contact_type')[:4]
    return contacts
