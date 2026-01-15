#!/usr/bin/env python
"""
Test script to verify the meeting detail template fix
"""

import os
import sys
import django
from django.test import RequestFactory
from django.template import Context, Template
from django.template.loader import get_template

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_panchayate_system.settings')
django.setup()

from modules.informationhub.models import MeetingSchedule
from modules.informationhub.views import meeting_detail
from datetime import date, timedelta
from django.contrib.auth import get_user_model

def test_template_syntax():
    """Test that the meeting_detail template loads without syntax errors"""
    print("Testing template syntax...")
    
    try:
        # Load the template
        template = get_template('informationhub/meeting_detail.html')
        print("✅ SUCCESS: Template loaded without syntax errors")
        return True
    except Exception as e:
        print(f"❌ ERROR: Template syntax error: {e}")
        return False

def test_meeting_status_badge():
    """Test the get_status_badge method functionality"""
    print("\nTesting get_status_badge method...")
    
    # Create a test meeting
    meeting = MeetingSchedule(
        meeting_title="Test Meeting",
        meeting_date=date.today() + timedelta(days=2),
        time="10:00",
        location="Test Location",
        agenda="Test agenda",
        organized_by="Test Organizer"
    )
    
    try:
        badge_class, badge_text = meeting.get_status_badge()
        print(f"✅ SUCCESS: get_status_badge() returned ({badge_class}, {badge_text})")
        return True
    except Exception as e:
        print(f"❌ ERROR: get_status_badge() failed: {e}")
        return False

def test_cancelled_meeting():
    """Test the get_status_badge method for cancelled meeting"""
    print("\nTesting cancelled meeting status...")
    
    # Create a cancelled meeting
    meeting = MeetingSchedule(
        meeting_title="Cancelled Meeting",
        meeting_date=date.today() + timedelta(days=2),
        time="10:00",
        location="Test Location",
        agenda="Test agenda",
        organized_by="Test Organizer",
        is_cancelled=True
    )
    
    try:
        badge_class, badge_text = meeting.get_status_badge()
        if badge_class == 'bg-danger' and badge_text == 'Cancelled':
            print(f"✅ SUCCESS: Cancelled meeting correctly returns ({badge_class}, {badge_text})")
            return True
        else:
            print(f"❌ ERROR: Cancelled meeting returned unexpected values: ({badge_class}, {badge_text})")
            return False
    except Exception as e:
        print(f"❌ ERROR: Cancelled meeting test failed: {e}")
        return False

def test_past_meeting():
    """Test the get_status_badge method for past meeting"""
    print("\nTesting past meeting status...")
    
    # Create a past meeting
    meeting = MeetingSchedule(
        meeting_title="Past Meeting",
        meeting_date=date.today() - timedelta(days=2),
        time="10:00",
        location="Test Location",
        agenda="Test agenda",
        organized_by="Test Organizer"
    )
    
    try:
        badge_class, badge_text = meeting.get_status_badge()
        if badge_class == 'bg-secondary' and badge_text == 'Completed':
            print(f"✅ SUCCESS: Past meeting correctly returns ({badge_class}, {badge_text})")
            return True
        else:
            print(f"❌ ERROR: Past meeting returned unexpected values: ({badge_class}, {badge_text})")
            return False
    except Exception as e:
        print(f"❌ ERROR: Past meeting test failed: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("MEETING DETAIL TEMPLATE FIX VERIFICATION TEST")
    print("=" * 60)
    
    test1 = test_template_syntax()
    test2 = test_meeting_status_badge()
    test3 = test_cancelled_meeting()
    test4 = test_past_meeting()
    
    print("\n" + "=" * 60)
    if all([test1, test2, test3, test4]):
        print("🎉 ALL TESTS PASSED! The template fix is working correctly.")
        print("   Meeting details page should now work on the citizen page.")
    else:
        print("❌ SOME TESTS FAILED! Please check the implementation.")
    print("=" * 60)