from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import PanchayatBudget
from .forms import PanchayatBudgetForm
import os

def public_budget_list(request):
    """Display all budget PDFs for public users (before login)"""
    # Get all budget PDFs ordered by financial year
    budgets = PanchayatBudget.objects.all().order_by('-financial_year')
    
    context = {
        'budgets': budgets,
    }
    return render(request, 'panchayat_budget/public_list.html', context)

def citizen_budget_list(request):
    """Display all budget PDFs for citizen users (after login)"""
    # Get all budget PDFs ordered by financial year
    budgets = PanchayatBudget.objects.all().order_by('-financial_year')
    
    context = {
        'budgets': budgets,
    }
    return render(request, 'panchayat_budget/citizen_list.html', context)

def budget_pdf_view(request, financial_year):
    """View a specific budget PDF for all users"""
    budget = get_object_or_404(PanchayatBudget, financial_year=financial_year)
    
    if budget.pdf_file:
        # Serve the file
        response = HttpResponse(budget.pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{budget.filename()}"'
        return response
    else:
        raise Http404("PDF file not found.")

@login_required
def manage_budget_pdfs(request):
    """Manage budget PDFs (admin and clerk only)"""
    # Check if user is admin or clerk
    if not (request.user.is_superuser or request.user.user_type == 'clerk'):
        messages.error(request, "Access denied. Admin or Clerk access required.")
        return redirect('common:home')
    
    # Get all budget PDFs
    budgets = PanchayatBudget.objects.all().order_by('-financial_year')
    
    context = {
        'budgets': budgets,
    }
    return render(request, 'panchayat_budget/manage_pdfs.html', context)

@login_required
def upload_budget_pdf(request):
    """Upload a budget PDF (admin and clerk only)"""
    # Check if user is admin or clerk
    if not (request.user.is_superuser or request.user.user_type == 'clerk'):
        messages.error(request, "Access denied. Admin or Clerk access required.")
        return redirect('common:home')
    
    if request.method == 'POST':
        form = PanchayatBudgetForm(request.POST, request.FILES)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.uploaded_by = request.user
            budget.save()
            messages.success(request, 'Budget PDF uploaded successfully!')
            return redirect('panchayat_budget:manage_budget_pdfs')
    else:
        form = PanchayatBudgetForm()
    
    context = {
        'form': form,
    }
    return render(request, 'panchayat_budget/upload_form.html', context)

@login_required
def edit_budget_pdf(request, financial_year):
    """Edit a budget PDF (admin and clerk only)"""
    # Check if user is admin or clerk
    if not (request.user.is_superuser or request.user.user_type == 'clerk'):
        messages.error(request, "Access denied. Admin or Clerk access required.")
        return redirect('common:home')
    
    budget = get_object_or_404(PanchayatBudget, financial_year=financial_year)
    
    if request.method == 'POST':
        form = PanchayatBudgetForm(request.POST, request.FILES, instance=budget)
        if form.is_valid():
            budget = form.save()
            messages.success(request, 'Budget PDF updated successfully!')
            return redirect('panchayat_budget:manage_budget_pdfs')
    else:
        form = PanchayatBudgetForm(instance=budget)
    
    context = {
        'form': form,
        'budget': budget,
    }
    return render(request, 'panchayat_budget/edit_form.html', context)

@login_required
def delete_budget_pdf(request, financial_year):
    """Delete a budget PDF (admin and clerk only)"""
    # Check if user is admin or clerk
    if not (request.user.is_superuser or request.user.user_type == 'clerk'):
        messages.error(request, "Access denied. Admin or Clerk access required.")
        return redirect('common:home')
    
    budget = get_object_or_404(PanchayatBudget, financial_year=financial_year)
    
    if request.method == 'POST':
        # Delete the file from storage
        if budget.pdf_file:
            if os.path.isfile(budget.pdf_file.path):
                os.remove(budget.pdf_file.path)
        budget.delete()
        messages.success(request, 'Budget PDF deleted successfully!')
        return redirect('panchayat_budget:manage_budget_pdfs')
    
    context = {
        'budget': budget,
    }
    return render(request, 'panchayat_budget/delete_confirm.html', context)