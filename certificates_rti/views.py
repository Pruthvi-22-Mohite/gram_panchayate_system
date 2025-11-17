from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.db.models import Q
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

from .models import (
    CertificateApplication, CertificateDocument, ApprovedCertificate,
    RTIRequest, LandRecordLink, LandParcel
)
from .forms import (
    CertificateApplicationForm, CertificateStatusUpdateForm, ApprovedCertificateUploadForm,
    RTIRequestForm, RTIStatusUpdateForm, RTIResponseUploadForm,
    LandRecordLinkForm, LandRecordSearchForm, LandRecordVerificationForm
)
from .decorators import citizen_required, clerk_required, admin_required


# ===========================
# CITIZEN VIEWS - CERTIFICATES
# ===========================

@citizen_required
def citizen_certificate_list(request):
    """List all certificate applications for logged-in citizen"""
    applications = CertificateApplication.objects.filter(citizen=request.user)
    
    context = {
        'applications': applications,
        'total_count': applications.count(),
        'pending_count': applications.filter(status='submitted').count(),
        'approved_count': applications.filter(status='approved').count(),
    }
    return render(request, 'certificates_rti/citizen/certificate_list.html', context)


@citizen_required
def citizen_certificate_apply(request):
    """Apply for a new certificate"""
    if request.method == 'POST':
        form = CertificateApplicationForm(request.POST)
        documents = request.FILES.getlist('documents')
        
        if form.is_valid():
            application = form.save(commit=False)
            application.citizen = request.user
            application.save()
            
            # Save multiple documents
            for doc in documents:
                CertificateDocument.objects.create(
                    application=application,
                    document=doc
                )
            
            messages.success(request, "Certificate application submitted successfully!")
            return redirect('certificates_rti:citizen_certificate_detail', pk=application.pk)
    else:
        form = CertificateApplicationForm()
    
    return render(request, 'certificates_rti/citizen/certificate_apply.html', {'form': form})


@citizen_required
def citizen_certificate_detail(request, pk):
    """View certificate application details"""
    application = get_object_or_404(CertificateApplication, pk=pk, citizen=request.user)
    
    context = {
        'application': application,
        'documents': application.documents.all(),
    }
    return render(request, 'certificates_rti/citizen/certificate_detail.html', context)


@citizen_required
def citizen_certificate_download(request, pk):
    """Download approved certificate PDF"""
    application = get_object_or_404(CertificateApplication, pk=pk, citizen=request.user)
    
    if application.status != 'approved':
        messages.error(request, "Certificate not yet approved.")
        return redirect('certificates_rti:citizen_certificate_detail', pk=pk)
    
    try:
        approved_cert = application.approved_certificate
        return FileResponse(approved_cert.certificate_file, as_attachment=True)
    except ApprovedCertificate.DoesNotExist:
        # Generate dummy PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Add content to PDF
        p.drawString(100, 750, "GRAM PANCHAYAT CERTIFICATE")
        p.drawString(100, 720, f"Certificate Type: {application.get_certificate_type_display()}")
        p.drawString(100, 690, f"Name: {application.full_name}")
        p.drawString(100, 660, f"Father's Name: {application.father_name}")
        p.drawString(100, 630, f"Mother's Name: {application.mother_name}")
        p.drawString(100, 600, f"Address: {application.address}")
        p.drawString(100, 570, f"Certificate No: CERT-{application.pk:06d}")
        p.drawString(100, 540, f"Date: {timezone.now().strftime('%d-%m-%Y')}")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'certificate_{application.pk}.pdf')


# ===========================
# CITIZEN VIEWS - RTI
# ===========================

@citizen_required
def citizen_rti_list(request):
    """List all RTI requests for logged-in citizen"""
    rti_requests = RTIRequest.objects.filter(citizen=request.user)
    
    context = {
        'rti_requests': rti_requests,
        'total_count': rti_requests.count(),
        'pending_count': rti_requests.filter(status__in=['submitted', 'under_review']).count(),
        'responded_count': rti_requests.filter(status='responded').count(),
    }
    return render(request, 'certificates_rti/citizen/rti_list.html', context)


@citizen_required
def citizen_rti_submit(request):
    """Submit a new RTI request"""
    if request.method == 'POST':
        form = RTIRequestForm(request.POST, request.FILES)
        if form.is_valid():
            rti = form.save(commit=False)
            rti.citizen = request.user
            rti.save()
            
            messages.success(request, "RTI request submitted successfully!")
            return redirect('certificates_rti:citizen_rti_detail', pk=rti.pk)
    else:
        form = RTIRequestForm()
    
    return render(request, 'certificates_rti/citizen/rti_submit.html', {'form': form})


@citizen_required
def citizen_rti_detail(request, pk):
    """View RTI request details"""
    rti = get_object_or_404(RTIRequest, pk=pk, citizen=request.user)
    
    return render(request, 'certificates_rti/citizen/rti_detail.html', {'rti': rti})


@citizen_required
def citizen_rti_download_response(request, pk):
    """Download RTI response file"""
    rti = get_object_or_404(RTIRequest, pk=pk, citizen=request.user)
    
    if not rti.response_file:
        messages.error(request, "Response file not available yet.")
        return redirect('certificates_rti:citizen_rti_detail', pk=pk)
    
    return FileResponse(rti.response_file, as_attachment=True)


# ===========================
# CITIZEN VIEWS - LAND RECORDS
# ===========================

@citizen_required
def citizen_land_search(request):
    """Search for land records"""
    results = []
    query = request.GET.get('search_query', '')
    
    if query:
        results = LandParcel.objects.filter(
            Q(survey_number__icontains=query) |
            Q(gat_number__icontains=query) |
            Q(property_id__icontains=query)
        )
    
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'certificates_rti/citizen/land_search.html', context)


@citizen_required
def citizen_land_link_request(request, property_id=None):
    """Submit land record linking request"""
    land_parcel = None
    if property_id:
        land_parcel = get_object_or_404(LandParcel, property_id=property_id)
    
    if request.method == 'POST':
        form = LandRecordLinkForm(request.POST, request.FILES)
        if form.is_valid():
            link = form.save(commit=False)
            link.citizen = request.user
            link.save()
            
            messages.success(request, "Land record linking request submitted successfully!")
            return redirect('certificates_rti:citizen_land_status')
    else:
        initial_data = {}
        if land_parcel:
            initial_data = {
                'survey_number': land_parcel.survey_number,
                'gat_number': land_parcel.gat_number,
                'property_id': land_parcel.property_id,
            }
        form = LandRecordLinkForm(initial=initial_data)
    
    context = {
        'form': form,
        'land_parcel': land_parcel,
    }
    return render(request, 'certificates_rti/citizen/land_link_request.html', context)


@citizen_required
def citizen_land_status(request):
    """View land record linking status"""
    land_records = LandRecordLink.objects.filter(citizen=request.user)
    
    context = {
        'land_records': land_records,
        'total_count': land_records.count(),
        'verified_count': land_records.filter(status='verified').count(),
    }
    return render(request, 'certificates_rti/citizen/land_status.html', context)


# Continue to clerk and admin views...


# ===========================
# CLERK VIEWS - CERTIFICATES
# ===========================

@clerk_required
def clerk_certificate_list(request):
    """List all certificate applications for clerk review"""
    status_filter = request.GET.get('status', '')
    
    applications = CertificateApplication.objects.all()
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    context = {
        'applications': applications,
        'total_count': applications.count(),
        'pending_count': CertificateApplication.objects.filter(status='submitted').count(),
        'under_review_count': CertificateApplication.objects.filter(status='under_review').count(),
        'status_filter': status_filter,
    }
    return render(request, 'certificates_rti/clerk/certificate_list.html', context)


@clerk_required
def clerk_certificate_detail(request, pk):
    """View and update certificate application"""
    application = get_object_or_404(CertificateApplication, pk=pk)
    
    if request.method == 'POST':
        form = CertificateStatusUpdateForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Certificate status updated successfully!")
            return redirect('certificates_rti:clerk_certificate_detail', pk=pk)
    else:
        form = CertificateStatusUpdateForm(instance=application)
    
    context = {
        'application': application,
        'documents': application.documents.all(),
        'form': form,
    }
    return render(request, 'certificates_rti/clerk/certificate_detail.html', context)


@clerk_required
def clerk_certificate_upload(request, pk):
    """Upload approved certificate PDF"""
    application = get_object_or_404(CertificateApplication, pk=pk)
    
    if request.method == 'POST':
        form = ApprovedCertificateUploadForm(request.POST, request.FILES)
        if form.is_valid():
            ApprovedCertificate.objects.create(
                application=application,
                certificate_number=form.cleaned_data['certificate_number'],
                certificate_file=form.cleaned_data['certificate_file'],
                approved_by=request.user
            )
            application.status = 'approved'
            application.save()
            
            messages.success(request, "Certificate uploaded successfully!")
            return redirect('certificates_rti:clerk_certificate_detail', pk=pk)
    else:
        form = ApprovedCertificateUploadForm()
    
    context = {
        'application': application,
        'form': form,
    }
    return render(request, 'certificates_rti/clerk/certificate_upload.html', context)


# ===========================
# CLERK VIEWS - RTI
# ===========================

@clerk_required
def clerk_rti_list(request):
    """List all RTI requests for clerk review"""
    status_filter = request.GET.get('status', '')
    
    rti_requests = RTIRequest.objects.all()
    if status_filter:
        rti_requests = rti_requests.filter(status=status_filter)
    
    context = {
        'rti_requests': rti_requests,
        'total_count': rti_requests.count(),
        'pending_count': RTIRequest.objects.filter(status='submitted').count(),
        'status_filter': status_filter,
    }
    return render(request, 'certificates_rti/clerk/rti_list.html', context)


@clerk_required
def clerk_rti_detail(request, pk):
    """View and respond to RTI request"""
    rti = get_object_or_404(RTIRequest, pk=pk)
    
    if request.method == 'POST':
        status_form = RTIStatusUpdateForm(request.POST, instance=rti)
        if status_form.is_valid():
            status_form.save()
            messages.success(request, "RTI status updated successfully!")
            return redirect('certificates_rti:clerk_rti_detail', pk=pk)
    else:
        status_form = RTIStatusUpdateForm(instance=rti)
    
    context = {
        'rti': rti,
        'status_form': status_form,
    }
    return render(request, 'certificates_rti/clerk/rti_detail.html', context)


@clerk_required
def clerk_rti_upload_response(request, pk):
    """Upload RTI response file"""
    rti = get_object_or_404(RTIRequest, pk=pk)
    
    if request.method == 'POST':
        form = RTIResponseUploadForm(request.POST, request.FILES)
        if form.is_valid():
            rti.response_file = form.cleaned_data['response_file']
            rti.status = 'under_review'
            rti.save()
            
            messages.success(request, "Response uploaded successfully!")
            return redirect('certificates_rti:clerk_rti_detail', pk=pk)
    else:
        form = RTIResponseUploadForm()
    
    context = {
        'rti': rti,
        'form': form,
    }
    return render(request, 'certificates_rti/clerk/rti_upload_response.html', context)


# ===========================
# CLERK VIEWS - LAND RECORDS
# ===========================

@clerk_required
def clerk_land_list(request):
    """List all land record linking requests"""
    status_filter = request.GET.get('status', '')
    
    land_records = LandRecordLink.objects.all()
    if status_filter:
        land_records = land_records.filter(status=status_filter)
    
    context = {
        'land_records': land_records,
        'total_count': land_records.count(),
        'pending_count': LandRecordLink.objects.filter(status='submitted').count(),
        'status_filter': status_filter,
    }
    return render(request, 'certificates_rti/clerk/land_list.html', context)


@clerk_required
def clerk_land_detail(request, pk):
    """Verify land record linking request"""
    land_record = get_object_or_404(LandRecordLink, pk=pk)
    
    if request.method == 'POST':
        form = LandRecordVerificationForm(request.POST, instance=land_record)
        if form.is_valid():
            record = form.save(commit=False)
            record.verified_by = request.user
            record.save()
            
            messages.success(request, "Land record verification updated!")
            return redirect('certificates_rti:clerk_land_detail', pk=pk)
    else:
        form = LandRecordVerificationForm(instance=land_record)
    
    context = {
        'land_record': land_record,
        'form': form,
    }
    return render(request, 'certificates_rti/clerk/land_detail.html', context)


# ===========================
# ADMIN VIEWS - CERTIFICATES
# ===========================

@admin_required
def admin_certificate_list(request):
    """Admin view of all certificate applications"""
    status_filter = request.GET.get('status', '')
    
    applications = CertificateApplication.objects.all()
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    context = {
        'applications': applications,
        'total_count': applications.count(),
        'pending_count': CertificateApplication.objects.filter(status='submitted').count(),
        'approved_count': CertificateApplication.objects.filter(status='approved').count(),
        'rejected_count': CertificateApplication.objects.filter(status='rejected').count(),
        'status_filter': status_filter,
    }
    return render(request, 'certificates_rti/admin/certificate_list.html', context)


@admin_required
def admin_certificate_detail(request, pk):
    """Admin detailed view with override capability"""
    application = get_object_or_404(CertificateApplication, pk=pk)
    
    if request.method == 'POST':
        form = CertificateStatusUpdateForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Certificate status updated successfully!")
            return redirect('certificates_rti:admin_certificate_detail', pk=pk)
    else:
        form = CertificateStatusUpdateForm(instance=application)
    
    context = {
        'application': application,
        'documents': application.documents.all(),
        'form': form,
    }
    return render(request, 'certificates_rti/admin/certificate_detail.html', context)


# ===========================
# ADMIN VIEWS - RTI
# ===========================

@admin_required
def admin_rti_list(request):
    """Admin view of all RTI requests"""
    status_filter = request.GET.get('status', '')
    
    rti_requests = RTIRequest.objects.all()
    if status_filter:
        rti_requests = rti_requests.filter(status=status_filter)
    
    context = {
        'rti_requests': rti_requests,
        'total_count': rti_requests.count(),
        'pending_count': RTIRequest.objects.filter(status__in=['submitted', 'under_review']).count(),
        'responded_count': RTIRequest.objects.filter(status='responded').count(),
        'status_filter': status_filter,
    }
    return render(request, 'certificates_rti/admin/rti_list.html', context)


@admin_required
def admin_rti_detail(request, pk):
    """Admin RTI management with final approval"""
    rti = get_object_or_404(RTIRequest, pk=pk)
    
    if request.method == 'POST':
        form = RTIStatusUpdateForm(request.POST, instance=rti)
        if form.is_valid():
            form.save()
            messages.success(request, "RTI status updated!")
            return redirect('certificates_rti:admin_rti_detail', pk=pk)
    else:
        form = RTIStatusUpdateForm(instance=rti)
    
    context = {
        'rti': rti,
        'form': form,
    }
    return render(request, 'certificates_rti/admin/rti_detail.html', context)


# ===========================
# ADMIN VIEWS - LAND RECORDS
# ===========================

@admin_required
def admin_land_list(request):
    """Admin view of all land record links"""
    status_filter = request.GET.get('status', '')
    
    land_records = LandRecordLink.objects.all()
    if status_filter:
        land_records = land_records.filter(status=status_filter)
    
    context = {
        'land_records': land_records,
        'total_count': land_records.count(),
        'verified_count': LandRecordLink.objects.filter(status='verified').count(),
        'status_filter': status_filter,
    }
    return render(request, 'certificates_rti/admin/land_list.html', context)


@admin_required
def admin_land_detail(request, pk):
    """Admin land record management"""
    land_record = get_object_or_404(LandRecordLink, pk=pk)
    
    if request.method == 'POST':
        form = LandRecordVerificationForm(request.POST, instance=land_record)
        if form.is_valid():
            record = form.save(commit=False)
            record.verified_by = request.user
            record.save()
            
            messages.success(request, "Land record updated!")
            return redirect('certificates_rti:admin_land_detail', pk=pk)
    else:
        form = LandRecordVerificationForm(instance=land_record)
    
    context = {
        'land_record': land_record,
        'form': form,
    }
    return render(request, 'certificates_rti/admin/land_detail.html', context)
