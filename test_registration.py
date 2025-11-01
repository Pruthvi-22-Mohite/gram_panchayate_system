"""
Test script for citizen registration functionality
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('d:/gram_panchayate_system')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_panchayate_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from gram_panchayate_system.models import CitizenProfile

def test_citizen_registration():
    """Test creating a citizen user with mobile number"""
    User = get_user_model()
    
    # Test data
    test_data = {
        'username': 'test_citizen',
        'mobile_number': '9876543210',
        'password': 'testpassword123',
        'aadhaar_number': '123456789012',
        'address': '123 Test Street, Test City'
    }
    
    try:
        # Check if user already exists
        if User.objects.filter(mobile_number=test_data['mobile_number']).exists():
            print(f"User with mobile number {test_data['mobile_number']} already exists")
            return
        
        # Create user
        user = User.objects.create_user(
            username=test_data['username'],
            password=test_data['password'],
            user_type='citizen',
            mobile_number=test_data['mobile_number']
        )
        
        # Create citizen profile
        citizen_profile = CitizenProfile(
            user=user,
            aadhaar_number=test_data['aadhaar_number'],
            address=test_data['address']
        )
        citizen_profile.save()
        
        print(f"Successfully created citizen user: {user.username}")
        print(f"Mobile number: {user.mobile_number}")
        print(f"Aadhaar number: {citizen_profile.aadhaar_number}")
        print(f"Address: {citizen_profile.address}")
        
    except Exception as e:
        print(f"Error creating citizen user: {e}")

if __name__ == "__main__":
    test_citizen_registration()