from django import forms
from .models import PanchayatBudget

class PanchayatBudgetForm(forms.ModelForm):
    """Form for uploading panchayat budget PDFs"""
    
    class Meta:
        model = PanchayatBudget
        fields = ['financial_year', 'title', 'description', 'pdf_file']
        widgets = {
            'financial_year': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_pdf_file(self):
        """Validate that only PDF files are uploaded"""
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            if not pdf_file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
        return pdf_file
