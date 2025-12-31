from django import forms
from .models import CertificateApplication, CertificateDocument, RTIRequest, LandRecordLink


class CertificateApplicationForm(forms.ModelForm):
    """Form for citizens to apply for certificates"""
    
    class Meta:
        model = CertificateApplication
        fields = ['certificate_type', 'full_name', 'father_name', 'mother_name', 
                  'address', 'phone', 'aadhar', 'reason']
        widgets = {
            'certificate_type': forms.Select(attrs={'class': 'form-select'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's name"}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Mother's name"}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'aadhar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12-digit Aadhar number'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for certificate'}),
        }


class CertificateDocumentForm(forms.ModelForm):
    """Form for uploading supporting documents"""
    
    class Meta:
        model = CertificateDocument
        fields = ['document']
        widgets = {
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CertificateStatusUpdateForm(forms.ModelForm):
    """Form for clerk/admin to update certificate status"""
    
    class Meta:
        model = CertificateApplication
        fields = ['status', 'remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add remarks'}),
        }


class ApprovedCertificateUploadForm(forms.Form):
    """Form for uploading approved certificate PDF"""
    certificate_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certificate Number'}))
    certificate_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))


class RTIRequestForm(forms.ModelForm):
    """Form for citizens to submit RTI requests"""
    
    class Meta:
        model = RTIRequest
        fields = ['subject', 'description', 'category', 'address', 'supporting_doc']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RTI Subject', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed description of information requested', 'required': True}),
            'category': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Your address for correspondence', 'required': True}),
            'supporting_doc': forms.FileInput(attrs={'class': 'form-control'}),
        }


class RTIStatusUpdateForm(forms.ModelForm):
    """Form for clerk/admin to update RTI status"""
    
    class Meta:
        model = RTIRequest
        fields = ['status', 'remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add remarks or response summary'}),
        }


class RTIResponseUploadForm(forms.Form):
    """Form for uploading RTI response file"""
    response_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))


class LandRecordLinkForm(forms.ModelForm):
    """Form for citizens to link land records"""
    
    class Meta:
        model = LandRecordLink
        fields = ['survey_number', 'gat_number', 'property_id', 'ownership_proof']
        widgets = {
            'survey_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Survey Number', 'required': True}),
            'gat_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gat Number', 'required': True}),
            'property_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property ID (Optional)'}),
            'ownership_proof': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
        }
        labels = {
            'survey_number': 'Survey Number',
            'gat_number': 'Gat Number',
            'property_id': 'Property ID',
            'ownership_proof': 'Ownership Proof Document',
        }
        help_texts = {
            'property_id': 'Optional - Leave blank if not available',
            'ownership_proof': 'Optional - Upload PDF, JPG, or PNG (Max 5MB)',
        }


class LandRecordSearchForm(forms.Form):
    """Form for searching land records"""
    search_query = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Search by Survey Number, Gat Number, or Property ID'
        })
    )


class LandRecordVerificationForm(forms.ModelForm):
    """Form for clerk/admin to verify land records"""
    
    class Meta:
        model = LandRecordLink
        fields = ['status', 'remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Verification remarks'}),
        }
