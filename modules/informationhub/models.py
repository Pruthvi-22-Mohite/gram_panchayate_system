from django.db import models
from django.utils import timezone


class VillageNotice(models.Model):
    """
    Model to store village notices and announcements
    """
    NOTICE_TYPE_CHOICES = [
        ('general', 'General'),
        ('emergency', 'Emergency'),
        ('announcement', 'Announcement'),
    ]
    
    title = models.CharField(max_length=200, help_text="Notice title")
    description = models.TextField(help_text="Detailed description of the notice")
    notice_type = models.CharField(
        max_length=20,
        choices=NOTICE_TYPE_CHOICES,
        default='general',
        help_text="Type of notice"
    )
    issued_by = models.CharField(max_length=100, help_text="Name of the issuing authority")
    date = models.DateField(default=timezone.now, help_text="Date of issuance")
    attachment = models.FileField(
        upload_to='notices/attachments/',
        blank=True,
        null=True,
        help_text="Optional attachment (PDF, Image, etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Is this notice active?")
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Village Notice'
        verbose_name_plural = 'Village Notices'
    
    def __str__(self):
        return f"{self.title} - {self.get_notice_type_display()}"
    
    def get_badge_class(self):
        """Return Bootstrap badge class based on notice type"""
        badge_map = {
            'general': 'bg-primary',
            'emergency': 'bg-danger',
            'announcement': 'bg-success',
        }
        return badge_map.get(self.notice_type, 'bg-secondary')


class MeetingSchedule(models.Model):
    """
    Model to store meeting schedules for the Gram Panchayat
    """
    meeting_title = models.CharField(max_length=200, help_text="Title of the meeting")
    meeting_date = models.DateField(help_text="Date of the meeting")
    time = models.TimeField(help_text="Time of the meeting")
    location = models.CharField(max_length=200, help_text="Venue/Location of the meeting")
    agenda = models.TextField(help_text="Meeting agenda and topics")
    organized_by = models.CharField(max_length=100, help_text="Organizer name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_cancelled = models.BooleanField(default=False, help_text="Is this meeting cancelled?")
    
    class Meta:
        ordering = ['meeting_date', 'time']
        verbose_name = 'Meeting Schedule'
        verbose_name_plural = 'Meeting Schedules'
    
    def __str__(self):
        return f"{self.meeting_title} - {self.meeting_date}"
    
    def is_upcoming(self):
        """Check if the meeting is in the future"""
        from datetime import datetime
        today = timezone.now().date()
        return self.meeting_date >= today and not self.is_cancelled
    
    def is_past(self):
        """Check if the meeting is in the past"""
        today = timezone.now().date()
        return self.meeting_date < today
    
    def get_status_badge(self):
        """Return status badge class"""
        if self.is_cancelled:
            return 'bg-danger', 'Cancelled'
        elif self.is_upcoming():
            return 'bg-success', 'Upcoming'
        else:
            return 'bg-secondary', 'Completed'
