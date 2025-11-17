"""
Dashboard Integration for Panchayat Budget Module

This file contains the code snippet to integrate budget information
into the citizen dashboard view.
"""

# Add this to your citizen dashboard view function
def citizen_dashboard_view(request):
    
    # Import the model
    from .models import PanchayatBudget
    
    # Get latest budgets for dashboard display
    latest_budgets = PanchayatBudget.objects.order_by('-created_at')[:5]
    
    context = {
        # ... existing context variables ...
        'latest_budgets': latest_budgets,
    }
    
    return render(request, 'citizen/dashboard.html', context)


# Add this to your citizen dashboard template (citizen/dashboard.html)
"""
<!-- Latest Budget Entries Section -->
<div class="card mt-4">
    <div class="card-header">
        <h5 class="mb-0">Latest Budget Updates</h5>
    </div>
    <div class="card-body">
        {% if latest_budgets %}
            <div class="row">
                {% for budget in latest_budgets %}
                <div class="col-md-6 col-lg-4 mb-3">
                    <div class="card budget-card">
                        <div class="card-header">
                            <h6 class="mb-0">{{ budget.budget_head|truncatechars:20 }}</h6>
                        </div>
                        <div class="card-body">
                            <p class="mb-1"><strong>Total Amount:</strong></p>
                            <p class="mb-2 h5 text-primary">₹{{ budget.total_amount|floatformat:2 }}</p>
                            <p class="mb-1"><strong>Updated:</strong></p>
                            <p class="mb-0 text-muted">{{ budget.updated_at|date:"d M Y" }}</p>
                        </div>
                        <div class="card-footer">
                            <a href="{% url 'panchayat_budget:budget_public_detail' budget.pk %}" 
                               class="btn btn-sm btn-primary w-100">
                                View Details
                            </a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        {% else %}
            <p class="text-muted text-center">No budget information available at this time.</p>
        {% endif %}
    </div>
</div>
"""