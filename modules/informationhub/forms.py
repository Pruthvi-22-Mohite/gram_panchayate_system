from django import forms
from modules.informationhub.models import VillageNotice, MeetingSchedule


class VillageNoticeForm(forms.ModelForm):
    """Form for creating and editing village notices"""
    
    class Meta:
        model = VillageNotice
        fields = ['title', 'description', 'notice_type', 'issued_by', 'date', 'attachment', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter notice title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter detailed description'
            }),
            'notice_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'issued_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter issuing authority'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class MeetingScheduleForm(forms.ModelForm):
    """Form for creating and editing meeting schedules"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make meeting_date required in HTML
        self.fields['meeting_date'].widget.attrs.update({'required': 'required'})
    
    class Meta:
        model = MeetingSchedule
        fields = ['meeting_title', 'meeting_date', 'time', 'location', 'agenda', 'organized_by', 'is_cancelled']
        widgets = {
            'meeting_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter meeting title'
            }),
            'meeting_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required'  # Required field
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter meeting location'
            }),
            'agenda': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter meeting agenda'
            }),
            'organized_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter organizer name'
            }),
            'is_cancelled': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_meeting_date(self):
        meeting_date = self.cleaned_data.get('meeting_date')
        if not meeting_date:
            raise forms.ValidationError("Meeting date is required.")
        from django.utils import timezone
        if meeting_date < timezone.now().date():
            raise forms.ValidationError("Meeting date cannot be in the past.")
        return meeting_date
