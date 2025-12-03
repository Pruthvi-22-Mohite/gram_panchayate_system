from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone

from modules.common.models import CustomUser
from modules.common.decorators import citizen_required
from modules.clerk.models import Scheme, SchemeApplication, Grievance, TaxRecord
from tax_management.models import CitizenTaxData
from modules.informationhub.models import VillageNotice, MeetingSchedule
from modules.emergencydirectory.models import EmergencyContact
from .models import CitizenProfile, CitizenDocument, FeedbackSuggestion, EmergencyContact as CitizenEmergencyContact, BudgetItem
from .forms import CitizenLoginForm, CitizenRegistrationForm, SchemeApplicationForm, GrievanceForm, FeedbackForm, DocumentUploadForm


def citizen_login(request):
    """Citizen login view with username and password"""
    if request.user.is_authenticated and request.user.user_type == 'citizen':
        return redirect('citizen:dashboard')
        
    if request.method == 'POST':
        form = CitizenLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.user_type == 'citizen':
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('citizen:dashboard')
            else:
                messages.error(request, "Invalid credentials or not a citizen user.")
    else:
        form = CitizenLoginForm()
    
    return render(request, 'citizen/login.html', {'form': form})


def citizen_registration(request):
    """Citizen registration view"""
    if request.user.is_authenticated:
        return redirect('citizen:dashboard')
    
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
            
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('citizen:login')
    else:
        form = CitizenRegistrationForm()
    
    return render(request, 'citizen/registration.html', {'form': form})


@citizen_required
def citizen_dashboard(request):
    """Citizen dashboard view"""
    
    # Get citizen's recent activities
    recent_applications = SchemeApplication.objects.filter(
        applicant=request.user
    ).order_by('-applied_at')[:5]
    
    recent_grievances = Grievance.objects.filter(
        submitted_by=request.user
    ).order_by('-submitted_at')[:5]
    
    pending_taxes = TaxRecord.objects.filter(
        taxpayer=request.user,
        status='pending'
    )
    
    # Get overdue taxes as well
    overdue_taxes = TaxRecord.objects.filter(
        taxpayer=request.user,
        status='overdue'
    )
    
    # Get tax data from the Aadhaar-based system
    citizen_tax_data = None
    try:
        citizen_profile = CitizenProfile.objects.get(user=request.user)
        citizen_tax_data = CitizenTaxData.objects.get(aadhaar_number=citizen_profile.aadhaar_number)
    except (CitizenProfile.DoesNotExist, CitizenTaxData.DoesNotExist):
        citizen_tax_data = None
    
    # Information Hub data
    today = timezone.now().date()
    
    # Get latest 5 notices
    latest_notices = VillageNotice.objects.filter(
        is_active=True
    ).order_by('-date')[:5]
    
    # Get next 3 upcoming meetings
    upcoming_meetings = MeetingSchedule.objects.filter(
        meeting_date__gte=today,
        is_cancelled=False
    ).order_by('meeting_date', 'time')[:3]
    
    # Get top 4 emergency contacts
    emergency_contacts = EmergencyContact.objects.filter(
        is_active=True
    ).order_by('-available_24x7', 'contact_type')[:4]
    
    context = {
        'recent_applications': recent_applications,
        'recent_grievances': recent_grievances,
        'pending_taxes': pending_taxes,
        'overdue_taxes': overdue_taxes,
        'citizen_tax_data': citizen_tax_data,
        'total_applications': recent_applications.count(),
        'total_grievances': recent_grievances.count(),
        'pending_tax_amount': sum(tax.amount for tax in pending_taxes),
        # Information Hub
        'latest_notices': latest_notices,
        'upcoming_meetings': upcoming_meetings,
        # Emergency Directory
        'emergency_contacts': emergency_contacts,
    }
    return render(request, 'citizen/dashboard.html', context)


@citizen_required
def view_schemes(request):
    """View available government schemes"""
    schemes = Scheme.objects.filter(is_active=True).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        schemes = schemes.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'schemes': schemes,
        'search_query': search_query
    }
    return render(request, 'citizen/view_schemes.html', context)


@citizen_required
def scheme_detail(request, scheme_id):
    """View details of a specific scheme"""
    scheme = get_object_or_404(Scheme, id=scheme_id, is_active=True)
    
    context = {
        'scheme': scheme
    }
    return render(request, 'citizen/scheme_detail.html', context)


@citizen_required
def apply_scheme(request, scheme_id):
    """Apply for a government scheme"""
    scheme = get_object_or_404(Scheme, id=scheme_id, is_active=True)
    
    # Check if user has already applied
    existing_application = SchemeApplication.objects.filter(
        scheme=scheme,
        applicant=request.user
    ).first()
    
    if existing_application:
        messages.warning(request, "You have already applied for this scheme.")
        return redirect('citizen:my_applications')
    
    if request.method == 'POST':
        form = SchemeApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = SchemeApplication(
                scheme=scheme,
                applicant=request.user,
                application_data=form.cleaned_data
            )
            application.save()
            
            messages.success(request, "Application submitted successfully!")
            return redirect('citizen:my_applications')
    else:
        form = SchemeApplicationForm()
    
    context = {
        'scheme': scheme,
        'form': form
    }
    return render(request, 'citizen/apply_scheme.html', context)


@citizen_required
def my_applications(request):
    """View citizen's scheme applications"""
    applications = SchemeApplication.objects.filter(
        applicant=request.user
    ).order_by('-applied_at')
    
    context = {
        'applications': applications
    }
    return render(request, 'citizen/my_applications.html', context)


@citizen_required
def lodge_grievance(request):
    """Lodge a new grievance"""
    if request.method == 'POST':
        form = GrievanceForm(request.POST, request.FILES)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.submitted_by = request.user
            grievance.save()
            
            messages.success(request, "Grievance submitted successfully!")
            return redirect('citizen:my_grievances')
    else:
        form = GrievanceForm()
    
    context = {
        'form': form
    }
    return render(request, 'citizen/lodge_grievance.html', context)


@citizen_required
def my_grievances(request):
    """View citizen's grievances"""
    grievances = Grievance.objects.filter(
        submitted_by=request.user
    ).order_by('-submitted_at')
    
    context = {
        'grievances': grievances
    }
    return render(request, 'citizen/my_grievances.html', context)


@citizen_required
def pay_tax(request):
    """View and pay property taxes only"""
    # Get property tax records from the clerk system (user-based)
    tax_records = TaxRecord.objects.filter(
        taxpayer=request.user,
        tax_type='property'
    ).order_by('-created_at')
    
    # Get property tax data from the Aadhaar-based system
    citizen_tax_data = None
    property_tax_data = None
    try:
        citizen_profile = CitizenProfile.objects.get(user=request.user)
        citizen_tax_data = CitizenTaxData.objects.get(aadhaar_number=citizen_profile.aadhaar_number)
        if citizen_tax_data.property_tax_amount:
            property_tax_data = {
                'amount': citizen_tax_data.property_tax_amount,
                'due_date': citizen_tax_data.property_due_date,
                'penalty': citizen_tax_data.property_penalty,
                'status': citizen_tax_data.property_status,
            }
    except (CitizenProfile.DoesNotExist, CitizenTaxData.DoesNotExist):
        pass
    
    context = {
        'tax_records': tax_records,
        'property_tax_data': property_tax_data
    }
    return render(request, 'citizen/pay_tax.html', context)


@citizen_required
def pay_water_bill(request):
    """View and pay water bills"""
    # Get water tax records from the clerk system (user-based)
    water_tax_records = TaxRecord.objects.filter(
        taxpayer=request.user,
        tax_type='water'
    ).order_by('-created_at')
    
    # Get water tax data from the Aadhaar-based system
    citizen_tax_data = None
    water_tax_data = None
    try:
        citizen_profile = CitizenProfile.objects.get(user=request.user)
        citizen_tax_data = CitizenTaxData.objects.get(aadhaar_number=citizen_profile.aadhaar_number)
        if citizen_tax_data.water_tax_amount:
            water_tax_data = {
                'amount': citizen_tax_data.water_tax_amount,
                'due_date': citizen_tax_data.water_due_date,
                'penalty': citizen_tax_data.water_penalty,
                'status': citizen_tax_data.water_status,
            }
    except (CitizenProfile.DoesNotExist, CitizenTaxData.DoesNotExist):
        pass
    
    context = {
        'water_tax_records': water_tax_records,
        'water_tax_data': water_tax_data
    }
    return render(request, 'citizen/pay_water_bill.html', context)


@citizen_required
def pay_garbage_bill(request):
    """View and pay garbage bills"""
    # Get garbage tax records from the clerk system (user-based)
    garbage_tax_records = TaxRecord.objects.filter(
        taxpayer=request.user,
        tax_type='garbage'
    ).order_by('-created_at')
    
    # Get garbage tax data from the Aadhaar-based system
    citizen_tax_data = None
    garbage_tax_data = None
    try:
        citizen_profile = CitizenProfile.objects.get(user=request.user)
        citizen_tax_data = CitizenTaxData.objects.get(aadhaar_number=citizen_profile.aadhaar_number)
        if citizen_tax_data.garbage_tax_amount:
            garbage_tax_data = {
                'amount': citizen_tax_data.garbage_tax_amount,
                'due_date': citizen_tax_data.garbage_due_date,
                'penalty': citizen_tax_data.garbage_penalty,
                'status': citizen_tax_data.garbage_status,
            }
    except (CitizenProfile.DoesNotExist, CitizenTaxData.DoesNotExist):
        pass
    
    context = {
        'garbage_tax_records': garbage_tax_records,
        'garbage_tax_data': garbage_tax_data
    }
    return render(request, 'citizen/pay_garbage_bill.html', context)


@citizen_required
def pay_health_bill(request):
    """View and pay health bills"""
    # Get health tax records from the clerk system (user-based)
    health_tax_records = TaxRecord.objects.filter(
        taxpayer=request.user,
        tax_type='health'
    ).order_by('-created_at')
    
    # Get health tax data from the Aadhaar-based system
    citizen_tax_data = None
    health_tax_data = None
    try:
        citizen_profile = CitizenProfile.objects.get(user=request.user)
        citizen_tax_data = CitizenTaxData.objects.get(aadhaar_number=citizen_profile.aadhaar_number)
        if citizen_tax_data.health_tax_amount:
            health_tax_data = {
                'amount': citizen_tax_data.health_tax_amount,
                'due_date': citizen_tax_data.health_due_date,
                'penalty': citizen_tax_data.health_penalty,
                'status': citizen_tax_data.health_status,
            }
    except (CitizenProfile.DoesNotExist, CitizenTaxData.DoesNotExist):
        pass
    
    context = {
        'health_tax_records': health_tax_records,
        'health_tax_data': health_tax_data
    }
    return render(request, 'citizen/pay_health_bill.html', context)


@citizen_required
def view_budget(request):
    """View panchayat budget"""
    budget_items = BudgetItem.objects.all().order_by('category', 'item_name')
    
    # Group by category
    budget_by_category = {}
    for item in budget_items:
        if item.category not in budget_by_category:
            budget_by_category[item.category] = []
        budget_by_category[item.category].append(item)
    
    context = {
        'budget_by_category': budget_by_category,
        'budget_items': budget_items
    }
    return render(request, 'citizen/view_budget.html', context)


@citizen_required
def emergency_directory(request):
    """View emergency contacts directory"""
    contacts = EmergencyContact.objects.filter(
        is_active=True
    ).order_by('contact_type', 'name')
    
    # Group by contact type
    contacts_by_type = {}
    for contact in contacts:
        if contact.contact_type not in contacts_by_type:
            contacts_by_type[contact.contact_type] = []
        contacts_by_type[contact.contact_type].append(contact)
    
    context = {
        'contacts_by_type': contacts_by_type
    }
    return render(request, 'citizen/emergency_directory.html', context)


@citizen_required
def feedback_suggestions(request):
    """Submit feedback and suggestions"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.citizen = request.user
            feedback.save()
            
            messages.success(request, "Thank you for your feedback!")
            return redirect('citizen:feedback_suggestions')
    else:
        form = FeedbackForm()
    
    # Show user's previous feedback
    previous_feedback = FeedbackSuggestion.objects.filter(
        citizen=request.user
    ).order_by('-submitted_at')
    
    context = {
        'form': form,
        'previous_feedback': previous_feedback
    }
    return render(request, 'citizen/feedback_suggestions.html', context)


@citizen_required
def my_documents(request):
    """Manage citizen documents"""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.citizen = request.user
            document.save()
            
            messages.success(request, "Document uploaded successfully!")
            return redirect('citizen:my_documents')
    else:
        form = DocumentUploadForm()
    
    documents = CitizenDocument.objects.filter(
        citizen=request.user
    ).order_by('-uploaded_at')
    
    context = {
        'form': form,
        'documents': documents
    }
    return render(request, 'citizen/my_documents.html', context)