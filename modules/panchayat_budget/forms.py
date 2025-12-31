from django import forms
from .models import PanchayatBudget, BudgetEntry


class PanchayatBudgetForm(forms.ModelForm):
    """Form for uploading panchayat budget PDFs"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make required fields required in HTML
        self.fields['financial_year'].widget.attrs.update({'required': 'required'})
        self.fields['title'].widget.attrs.update({'required': 'required'})
        self.fields['description'].widget.attrs.update({'required': 'required'})
        self.fields['pdf_file'].widget.attrs.update({'required': 'required'})
    
    class Meta:
        model = PanchayatBudget
        fields = ['financial_year', 'title', 'description', 'pdf_file']
        widgets = {
            'financial_year': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': 'required'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'required': 'required'}),
        }
    
    def clean_financial_year(self):
        financial_year = self.cleaned_data.get('financial_year')
        if not financial_year or not financial_year.strip():
            raise forms.ValidationError("Financial year is required.")
        return financial_year
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise forms.ValidationError("Title is required.")
        return title
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or not description.strip():
            raise forms.ValidationError("Description is required.")
        return description
    
    def clean_pdf_file(self):
        """Validate that only PDF files are uploaded and file is not empty"""
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            if not pdf_file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            if pdf_file.size == 0:
                raise forms.ValidationError("Budget file cannot be empty.")
        return pdf_file


class BudgetEntryForm(forms.ModelForm):
    """
    Form for managing budget entries with numeric fields
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add other budget head field for 'other' option
        self.fields['other_budget_head'] = forms.CharField(
            max_length=100,
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify budget head',
                'id': 'other_budget_head'
            })
        )
    
    class Meta:
        model = BudgetEntry
        fields = ['budget_head', 'previous_year_amount', 'revenue_income', 'revenue_collection', 
                  'expenditure_allotted', 'expenditure_spent']
        widgets = {
            'budget_head': forms.Select(attrs={'class': 'form-control', 'onchange': 'toggleOtherField(this, "budget")', 'required': 'required'}),
            'previous_year_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required'}),
            'revenue_income': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required'}),
            'revenue_collection': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required'}),
            'expenditure_allotted': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required'}),
            'expenditure_spent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': 'required'}),
        }
    
    def clean_budget_head(self):
        budget_head = self.cleaned_data.get('budget_head')
        if budget_head == 'other':
            # If 'other' is selected, we need to validate the custom budget head
            other_budget_head = self.cleaned_data.get('other_budget_head', '').strip()
            if not other_budget_head:
                raise forms.ValidationError("When 'Other' is selected, please specify the budget head.")
        return budget_head

    def clean_previous_year_amount(self):
        previous_year_amount = self.cleaned_data.get('previous_year_amount')
        if previous_year_amount is not None and previous_year_amount < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return previous_year_amount
    
    def clean_revenue_income(self):
        revenue_income = self.cleaned_data.get('revenue_income')
        if revenue_income is not None and revenue_income < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return revenue_income
    
    def clean_revenue_collection(self):
        revenue_collection = self.cleaned_data.get('revenue_collection')
        if revenue_collection is not None and revenue_collection < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return revenue_collection
    
    def clean_expenditure_allotted(self):
        expenditure_allotted = self.cleaned_data.get('expenditure_allotted')
        if expenditure_allotted is not None and expenditure_allotted < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return expenditure_allotted
    
    def clean_expenditure_spent(self):
        expenditure_spent = self.cleaned_data.get('expenditure_spent')
        if expenditure_spent is not None and expenditure_spent < 0:
            raise forms.ValidationError("Negative values are not allowed.")
        return expenditure_spent