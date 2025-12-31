from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import PanchayatBudget, BudgetEntry
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


# Views for BudgetEntry model (numeric budget entries)
@login_required
def budget_list(request):
    """Display all budget entries for admin and clerk users"""
    # Check if user is admin or clerk
    if not (request.user.is_superuser or request.user.user_type == 'clerk'):
        messages.error(request, "Access denied. Admin or Clerk access required.")
        return redirect('common:home')
    
    # Get all budget entries
    budgets = BudgetEntry.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        budgets = budgets.filter(budget_head__icontains=search_query)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(budgets, 10)  # Show 10 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'panchayat_budget/budget_list.html', context)


@login_required
def budget_detail(request, pk):
    """Display details of a specific budget entry"""
    budget = get_object_or_404(BudgetEntry, pk=pk)
    
    context = {
        'budget': budget,
    }
    return render(request, 'panchayat_budget/budget_detail.html', context)


@login_required
def budget_add(request):
    """Add a new budget entry"""
    # Check if user is admin or clerk
    if not (request.user.is_superuser or request.user.user_type == 'clerk'):
        messages.error(request, "Access denied. Admin or Clerk access required.")
        return redirect('common:home')
    
    from .forms import BudgetEntryForm
    
    if request.method == 'POST':
        form = BudgetEntryForm(request.POST)
        if form.is_valid():
            budget = form.save()
            messages.success(request, 'Budget entry added successfully!')
            return redirect('panchayat_budget:budget_list')
    else:
        form = BudgetEntryForm()
    
    context = {
        'form': form,
    }
    return render(request, 'panchayat_budget/budget_add.html', context)



@login_required
def budget_edit(request, pk):
    """Edit an existing budget entry"""
    # Check if user is admin or clerk
    if not (request.user.is_superuser or request.user.user_type == 'clerk'):
        messages.error(request, "Access denied. Admin or Clerk access required.")
        return redirect('common:home')
    
    budget = get_object_or_404(BudgetEntry, pk=pk)
    from .forms import BudgetEntryForm
    
    if request.method == 'POST':
        form = BudgetEntryForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget entry updated successfully!')
            return redirect('panchayat_budget:budget_list')
    else:
        form = BudgetEntryForm(instance=budget)
    
    context = {
        'form': form,
        'budget': budget,
    }
    return render(request, 'panchayat_budget/budget_edit.html', context)


@login_required
def budget_delete(request, pk):
    """Delete a budget entry"""
    # Check if user is admin or clerk
    if not (request.user.is_superuser or request.user.user_type == 'clerk'):
        messages.error(request, "Access denied. Admin or Clerk access required.")
        return redirect('common:home')
    
    budget = get_object_or_404(BudgetEntry, pk=pk)
    
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget entry deleted successfully!')
        return redirect('panchayat_budget:budget_list')
    
    context = {
        'budget': budget,
    }
    return render(request, 'panchayat_budget/budget_delete.html', context)


def public_budget_entry_list(request):
    """Display all budget entries for public users (before login)"""
    # Get all budget entries ordered by creation date
    budgets = BudgetEntry.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        budgets = budgets.filter(budget_head__icontains=search_query)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(budgets, 10)  # Show 10 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'panchayat_budget/budget_public_list.html', context)


def budget_entry_detail(request, pk):
    """View a specific budget entry for all users"""
    budget = get_object_or_404(BudgetEntry, pk=pk)
    
    context = {
        'budget': budget,
    }
    return render(request, 'panchayat_budget/budget_public_detail.html', context)