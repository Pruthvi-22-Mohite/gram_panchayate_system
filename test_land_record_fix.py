#!/usr/bin/env python
"""
Test script to verify the land record linking fix
"""

import os
import sys
import django
from django.test import TestCase
from django.core.exceptions import ValidationError

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_panchayate_system.settings')
django.setup()

from certificates_rti.models import LandRecordLink
from modules.common.models import CustomUser

def test_land_record_link_creation():
    """Test that LandRecordLink can be created without area field error"""
    print("Testing LandRecordLink creation...")
    
    # Create a test user
    user = CustomUser.objects.create_user(
        username='testuser_land',
        email='test@example.com',
        password='testpass123',
        user_type='citizen'
    )
    
    # Create LandRecordLink instance
    land_record = LandRecordLink(
        citizen=user,
        survey_number='123',
        gat_number='456',
        property_id='PROP-001'
    )
    
    try:
        # This should not raise an AttributeError anymore
        land_record.full_clean()  # This calls the clean() method
        land_record.save()
        print("✅ SUCCESS: LandRecordLink created successfully!")
        print(f"   Created record with ID: {land_record.id}")
        return True
    except ValidationError as e:
        print(f"❌ VALIDATION ERROR: {e}")
        return False
    except AttributeError as e:
        print(f"❌ ATTRIBUTE ERROR: {e}")
        return False
    except Exception as e:
        print(f"❌ OTHER ERROR: {e}")
        return False
    finally:
        # Clean up
        user.delete()

def test_land_record_with_negative_values():
    """Test that validation still works for required fields"""
    print("\nTesting validation for required fields...")
    
    user = CustomUser.objects.create_user(
        username='testuser_land2',
        email='test2@example.com',
        password='testpass123',
        user_type='citizen'
    )
    
    # Test with empty survey number
    land_record = LandRecordLink(
        citizen=user,
        survey_number='',  # Empty - should fail validation
        gat_number='456',
        property_id='PROP-002'
    )
    
    try:
        land_record.full_clean()
        land_record.save()
        print("❌ UNEXPECTED: Validation should have failed for empty survey number")
        return False
    except ValidationError as e:
        if 'survey_number' in str(e):
            print("✅ SUCCESS: Validation correctly caught empty survey number")
            return True
        else:
            print(f"❌ UNEXPECTED VALIDATION ERROR: {e}")
            return False
    except Exception as e:
        print(f"❌ OTHER ERROR: {e}")
        return False
    finally:
        user.delete()

if __name__ == '__main__':
    print("=" * 50)
    print("LAND RECORD LINKING FIX VERIFICATION TEST")
    print("=" * 50)
    
    success1 = test_land_record_link_creation()
    success2 = test_land_record_with_negative_values()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED! The fix is working correctly.")
        print("   Land record linking should now work on the citizen page.")
    else:
        print("❌ SOME TESTS FAILED! Please check the implementation.")
    print("=" * 50)