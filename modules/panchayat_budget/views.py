from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import PanchayatBudget
from .forms import PanchayatBudgetForm
from .decorators import admin_or_clerk_required, citizen_required, admin_required


# Admin/Clerk Views
@admin_or_clerk_required
def budget_list(request):
    """List all budget entries for admin and clerk users"""
    budgets = PanchayatBudget.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        budgets = budgets.filter(
            Q(budget_head__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(budgets, 10)  # Show 10 budgets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query
    }
    return render(request, 'panchayat_budget/budget_list.html', context)


@admin_or_clerk_required
def budget_add(request):
    """Add a new budget entry"""
    if request.method == 'POST':
        form = PanchayatBudgetForm(request.POST, request.FILES)
        if form.is_valid():
            budget = form.save()
            messages.success(request, 'Budget entry added successfully!')
            return redirect('panchayat_budget:budget_list')
    else:
        form = PanchayatBudgetForm()
    
    context = {
        'form': form,
        'title': 'Add Budget Entry'
    }
    return render(request, 'panchayat_budget/budget_add.html', context)


@admin_or_clerk_required
def budget_edit(request, pk):
    """Edit an existing budget entry"""
    budget = get_object_or_404(PanchayatBudget, pk=pk)
    
    if request.method == 'POST':
        form = PanchayatBudgetForm(request.POST, request.FILES, instance=budget)
        if form.is_valid():
            budget = form.save()
            messages.success(request, 'Budget entry updated successfully!')
            return redirect('panchayat_budget:budget_detail', pk=budget.pk)
    else:
        form = PanchayatBudgetForm(instance=budget)
    
    context = {
        'form': form,
        'budget': budget,
        'title': 'Edit Budget Entry'
    }
    return render(request, 'panchayat_budget/budget_edit.html', context)


@admin_required
def budget_delete(request, pk):
    """Delete a budget entry (admin only)"""
    budget = get_object_or_404(PanchayatBudget, pk=pk)
    
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget entry deleted successfully!')
        return redirect('panchayat_budget:budget_list')
    
    context = {
        'budget': budget,
        'title': 'Delete Budget Entry'
    }
    return render(request, 'panchayat_budget/budget_delete.html', context)


@admin_or_clerk_required
def budget_detail(request, pk):
    """View details of a budget entry"""
    budget = get_object_or_404(PanchayatBudget, pk=pk)
    context = {
        'budget': budget,
        'title': 'Budget Details'
    }
    return render(request, 'panchayat_budget/budget_detail.html', context)


# Citizen Views
@citizen_required
def budget_public_list(request):
    """List all budget entries for citizen users (read-only)"""
    budgets = PanchayatBudget.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        budgets = budgets.filter(
            Q(budget_head__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(budgets, 10)  # Show 10 budgets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query
    }
    return render(request, 'panchayat_budget/budget_public_list.html', context)


@citizen_required
def budget_public_detail(request, pk):
    """View details of a budget entry for citizen users (read-only)"""
    budget = get_object_or_404(PanchayatBudget, pk=pk)
    context = {
        'budget': budget,
        'title': 'Budget Details'
    }
    return render(request, 'panchayat_budget/budget_public_detail.html', context)