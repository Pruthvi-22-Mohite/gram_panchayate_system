import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_panchayate_system.settings')

# Setup Django
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from gram_panchayate_system.models import OTP

def test_citizen_login():
    """Test citizen login flow"""
    client = Client()
    
    # Check if citizen user exists
    User = get_user_model()
    try:
        citizen_user = User.objects.get(mobile_number='9876543210', user_type='citizen')
        print(f"Citizen user found: {citizen_user.username}")
    except User.DoesNotExist:
        print("Creating test citizen user...")
        citizen_user = User.objects.create_user(
            username='test_citizen_flow',
            password='citizen123',
            user_type='citizen',
            mobile_number='9876543210'
        )
        print(f"Created citizen user: {citizen_user.username}")
    
    print("\nTesting citizen login flow...")
    
    # Step 1: Request OTP
    print("1. Requesting OTP...")
    response = client.post('/citizen-otp-request/', {
        'mobile_number': '9876543210'
    })
    print(f"   OTP request status: {response.status_code}")
    
    # Check if OTP was created
    otp_records = OTP._default_manager.filter(mobile_number='9876543210', is_used=False)
    if otp_records.exists():
        otp_record = otp_records.first()
        print(f"   OTP created: {otp_record.otp}")
        
        # Step 2: Verify OTP
        print("2. Verifying OTP...")
        response = client.post('/citizen-otp-verify/', {
            'mobile_number': '9876543210',
            'otp': otp_record.otp
        })
        print(f"   OTP verification status: {response.status_code}")
        print(f"   OTP verification redirect: {getattr(response, 'url', 'No URL')}")
        
        # Check if user is authenticated
        session_auth = client.session.get('_auth_user_id')
        if session_auth:
            print("   User is authenticated!")
        else:
            print("   User is NOT authenticated!")
    else:
        print("   No OTP record found!")
    
    print("\nCitizen login test completed!")

if __name__ == "__main__":
    test_citizen_login()