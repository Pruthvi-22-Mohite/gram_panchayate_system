from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import VillageNotice, MeetingSchedule


def notices_list(request):
    """
    Display all village notices with filtering options
    """
    notices = VillageNotice.objects.filter(is_active=True)
    
    # Filter by notice type
    notice_type = request.GET.get('notice_type', '')
    if notice_type:
        notices = notices.filter(notice_type=notice_type)
    
    # Filter by date range
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if date_from:
        notices = notices.filter(date__gte=date_from)
    if date_to:
        notices = notices.filter(date__lte=date_to)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        notices = notices.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(issued_by__icontains=search_query)
        )
    
    context = {
        'notices': notices,
        'notice_type': notice_type,
        'date_from': date_from,
        'date_to': date_to,
        'search_query': search_query,
        'notice_types': VillageNotice.NOTICE_TYPE_CHOICES,
    }
    
    return render(request, 'informationhub/notices_list.html', context)


def notice_detail(request, notice_id):
    """
    Display detailed view of a single notice
    """
    notice = get_object_or_404(VillageNotice, id=notice_id, is_active=True)
    
    # Get related notices (same type)
    related_notices = VillageNotice.objects.filter(
        notice_type=notice.notice_type,
        is_active=True
    ).exclude(id=notice.id)[:3]
    
    context = {
        'notice': notice,
        'related_notices': related_notices,
    }
    
    return render(request, 'informationhub/notice_detail.html', context)


def meetings_list(request):
    """
    Display all meeting schedules with filtering options
    """
    today = timezone.now().date()
    
    # Get upcoming and past meetings
    upcoming_meetings = MeetingSchedule.objects.filter(
        meeting_date__gte=today,
        is_cancelled=False
    ).order_by('meeting_date', 'time')
    
    past_meetings = MeetingSchedule.objects.filter(
        meeting_date__lt=today
    ).order_by('-meeting_date', '-time')
    
    # Filter by organizer
    organizer = request.GET.get('organizer', '')
    if organizer:
        upcoming_meetings = upcoming_meetings.filter(organized_by__icontains=organizer)
        past_meetings = past_meetings.filter(organized_by__icontains=organizer)
    
    # Filter by date range
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if date_from:
        upcoming_meetings = upcoming_meetings.filter(meeting_date__gte=date_from)
        past_meetings = past_meetings.filter(meeting_date__gte=date_from)
    
    if date_to:
        upcoming_meetings = upcoming_meetings.filter(meeting_date__lte=date_to)
        past_meetings = past_meetings.filter(meeting_date__lte=date_to)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        upcoming_meetings = upcoming_meetings.filter(
            Q(meeting_title__icontains=search_query) |
            Q(agenda__icontains=search_query) |
            Q(location__icontains=search_query)
        )
        past_meetings = past_meetings.filter(
            Q(meeting_title__icontains=search_query) |
            Q(agenda__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {
        'upcoming_meetings': upcoming_meetings,
        'past_meetings': past_meetings,
        'organizer': organizer,
        'date_from': date_from,
        'date_to': date_to,
        'search_query': search_query,
    }
    
    return render(request, 'informationhub/meetings_list.html', context)


def meeting_detail(request, meeting_id):
    """
    Display detailed view of a single meeting
    """
    meeting = get_object_or_404(MeetingSchedule, id=meeting_id)
    
    # Get related meetings (by same organizer)
    related_meetings = MeetingSchedule.objects.filter(
        organized_by=meeting.organized_by,
        is_cancelled=False
    ).exclude(id=meeting.id).order_by('-meeting_date')[:3]
    
    context = {
        'meeting': meeting,
        'related_meetings': related_meetings,
    }
    
    return render(request, 'informationhub/meeting_detail.html', context)
