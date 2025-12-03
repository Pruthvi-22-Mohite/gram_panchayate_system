import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import CitizenTaxData
from modules.common.decorators import admin_required, clerk_required
from modules.common.models import CustomUser
from modules.citizen.models import CitizenProfile

@login_required
def citizen_tax_bills(request):
    """
    Display tax bills for the logged-in citizen based on their Aadhaar number
    """
    try:
        # Get citizen's Aadhaar number from their profile
        citizen_profile = CitizenProfile.objects.get(user=request.user)
        aadhaar_number = citizen_profile.aadhaar_number
        
        # Get tax data for this citizen
        tax_data = CitizenTaxData.objects.get(aadhaar_number=aadhaar_number)
        
        # Prepare tax bills data
        tax_bills = []
        
        # Property Tax
        if tax_data.property_tax_amount:
            tax_bills.append({
                'type': 'Property Tax',
                'amount': tax_data.property_tax_amount,
                'penalty': tax_data.property_penalty,
                'due_date': tax_data.property_due_date,
                'status': tax_data.property_status,
                'status_class': get_status_class(tax_data.property_status)
            })
        
        # Water Tax
        if tax_data.water_tax_amount:
            tax_bills.append({
                'type': 'Water Tax',
                'amount': tax_data.water_tax_amount,
                'penalty': tax_data.water_penalty,
                'due_date': tax_data.water_due_date,
                'status': tax_data.water_status,
                'status_class': get_status_class(tax_data.water_status)
            })
        
        # Garbage Tax
        if tax_data.garbage_tax_amount:
            tax_bills.append({
                'type': 'Garbage Tax',
                'amount': tax_data.garbage_tax_amount,
                'penalty': tax_data.garbage_penalty,
                'due_date': tax_data.garbage_due_date,
                'status': tax_data.garbage_status,
                'status_class': get_status_class(tax_data.garbage_status)
            })
        
        # Health Tax
        if tax_data.health_tax_amount:
            tax_bills.append({
                'type': 'Health Tax',
                'amount': tax_data.health_tax_amount,
                'penalty': tax_data.health_penalty,
                'due_date': tax_data.health_due_date,
                'status': tax_data.health_status,
                'status_class': get_status_class(tax_data.health_status)
            })
        
        # Check if all bills are paid
        all_paid = all(bill['status'] == 'paid' for bill in tax_bills) if tax_bills else True
        
        context = {
            'tax_bills': tax_bills,
            'all_paid': all_paid,
            'tax_data': tax_data
        }
        
        return render(request, 'tax_management/citizen_tax_bills.html', context)
        
    except CitizenProfile.DoesNotExist:
        messages.error(request, "Citizen profile not found. Please contact administrator.")
        return redirect('citizen:dashboard')
    except CitizenTaxData.DoesNotExist:
        # No tax data found for this citizen
        context = {
            'tax_bills': [],
            'all_paid': True
        }
        return render(request, 'tax_management/citizen_tax_bills.html', context)

def get_status_class(status):
    """
    Return CSS class based on status
    """
    status_classes = {
        'paid': 'bg-success',
        'pending': 'bg-warning',
        'overdue': 'bg-danger'
    }
    return status_classes.get(status, 'bg-secondary')

@admin_required
def admin_excel_upload(request):
    """
    Admin view for uploading Excel file with tax data
    """
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        try:
            # Read Excel file
            df = pd.read_excel(excel_file)
            
            # Process each row
            updated_count = 0
            created_count = 0
            
            for _, row in df.iterrows():
                aadhaar_number = str(row['Aadhaar Number']) if pd.notna(row['Aadhaar Number']) else None
                
                if not aadhaar_number:
                    continue
                
                # Prepare data for update or create
                tax_data_defaults = {
                    'updated_at': pd.Timestamp.now()
                }
                
                # Property Tax
                if pd.notna(row.get('Property Tax Amount')):
                    tax_data_defaults['property_tax_amount'] = row['Property Tax Amount']
                if pd.notna(row.get('Property Due Date')):
                    tax_data_defaults['property_due_date'] = row['Property Due Date']
                if pd.notna(row.get('Property Penalty')):
                    tax_data_defaults['property_penalty'] = row['Property Penalty']
                if pd.notna(row.get('Property Status')):
                    tax_data_defaults['property_status'] = row['Property Status']
                
                # Water Tax
                if pd.notna(row.get('Water Tax Amount')):
                    tax_data_defaults['water_tax_amount'] = row['Water Tax Amount']
                if pd.notna(row.get('Water Due Date')):
                    tax_data_defaults['water_due_date'] = row['Water Due Date']
                if pd.notna(row.get('Water Penalty')):
                    tax_data_defaults['water_penalty'] = row['Water Penalty']
                if pd.notna(row.get('Water Status')):
                    tax_data_defaults['water_status'] = row['Water Status']
                
                # Garbage Tax
                if pd.notna(row.get('Garbage Tax Amount')):
                    tax_data_defaults['garbage_tax_amount'] = row['Garbage Tax Amount']
                if pd.notna(row.get('Garbage Due Date')):
                    tax_data_defaults['garbage_due_date'] = row['Garbage Due Date']
                if pd.notna(row.get('Garbage Penalty')):
                    tax_data_defaults['garbage_penalty'] = row['Garbage Penalty']
                if pd.notna(row.get('Garbage Status')):
                    tax_data_defaults['garbage_status'] = row['Garbage Status']
                
                # Health Tax
                if pd.notna(row.get('Health Tax Amount')):
                    tax_data_defaults['health_tax_amount'] = row['Health Tax Amount']
                if pd.notna(row.get('Health Due Date')):
                    tax_data_defaults['health_due_date'] = row['Health Due Date']
                if pd.notna(row.get('Health Penalty')):
                    tax_data_defaults['health_penalty'] = row['Health Penalty']
                if pd.notna(row.get('Health Status')):
                    tax_data_defaults['health_status'] = row['Health Status']
                
                # Update or create record
                obj, created = CitizenTaxData.objects.update_or_create(
                    aadhaar_number=aadhaar_number,
                    defaults=tax_data_defaults
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
            
            messages.success(request, f"Excel file processed successfully. {created_count} new records created, {updated_count} records updated.")
            return redirect('tax_management:admin_excel_upload')
            
        except Exception as e:
            messages.error(request, f"Error processing Excel file: {str(e)}")
            return redirect('tax_management:admin_excel_upload')
    
    return render(request, 'tax_management/admin_excel_upload.html')

@clerk_required
def clerk_excel_upload(request):
    """
    Clerk view for uploading Excel file with tax data
    """
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        try:
            # Read Excel file
            df = pd.read_excel(excel_file)
            
            # Process each row
            updated_count = 0
            created_count = 0
            
            for _, row in df.iterrows():
                aadhaar_number = str(row['Aadhaar Number']) if pd.notna(row['Aadhaar Number']) else None
                
                if not aadhaar_number:
                    continue
                
                # Prepare data for update or create
                tax_data_defaults = {
                    'updated_at': pd.Timestamp.now()
                }
                
                # Property Tax
                if pd.notna(row.get('Property Tax Amount')):
                    tax_data_defaults['property_tax_amount'] = row['Property Tax Amount']
                if pd.notna(row.get('Property Due Date')):
                    tax_data_defaults['property_due_date'] = row['Property Due Date']
                if pd.notna(row.get('Property Penalty')):
                    tax_data_defaults['property_penalty'] = row['Property Penalty']
                if pd.notna(row.get('Property Status')):
                    tax_data_defaults['property_status'] = row['Property Status']
                
                # Water Tax
                if pd.notna(row.get('Water Tax Amount')):
                    tax_data_defaults['water_tax_amount'] = row['Water Tax Amount']
                if pd.notna(row.get('Water Due Date')):
                    tax_data_defaults['water_due_date'] = row['Water Due Date']
                if pd.notna(row.get('Water Penalty')):
                    tax_data_defaults['water_penalty'] = row['Water Penalty']
                if pd.notna(row.get('Water Status')):
                    tax_data_defaults['water_status'] = row['Water Status']
                
                # Garbage Tax
                if pd.notna(row.get('Garbage Tax Amount')):
                    tax_data_defaults['garbage_tax_amount'] = row['Garbage Tax Amount']
                if pd.notna(row.get('Garbage Due Date')):
                    tax_data_defaults['garbage_due_date'] = row['Garbage Due Date']
                if pd.notna(row.get('Garbage Penalty')):
                    tax_data_defaults['garbage_penalty'] = row['Garbage Penalty']
                if pd.notna(row.get('Garbage Status')):
                    tax_data_defaults['garbage_status'] = row['Garbage Status']
                
                # Health Tax
                if pd.notna(row.get('Health Tax Amount')):
                    tax_data_defaults['health_tax_amount'] = row['Health Tax Amount']
                if pd.notna(row.get('Health Due Date')):
                    tax_data_defaults['health_due_date'] = row['Health Due Date']
                if pd.notna(row.get('Health Penalty')):
                    tax_data_defaults['health_penalty'] = row['Health Penalty']
                if pd.notna(row.get('Health Status')):
                    tax_data_defaults['health_status'] = row['Health Status']
                
                # Update or create record
                obj, created = CitizenTaxData.objects.update_or_create(
                    aadhaar_number=aadhaar_number,
                    defaults=tax_data_defaults
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
            
            messages.success(request, f"Excel file processed successfully. {created_count} new records created, {updated_count} records updated.")
            return redirect('tax_management:clerk_excel_upload')
            
        except Exception as e:
            messages.error(request, f"Error processing Excel file: {str(e)}")
            return redirect('tax_management:clerk_excel_upload')
    
    return render(request, 'tax_management/clerk_excel_upload.html')