import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_panchayate_system.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model
from gram_panchayate_system.models import CitizenProfile
import random
import string

def create_citizen(username, mobile_number, aadhaar_number, address, password=None, date_of_birth=None):
    User = get_user_model()
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f'User with username "{username}" already exists')
        return None
        
    if User.objects.filter(mobile_number=mobile_number).exists():
        print(f'User with mobile number "{mobile_number}" already exists')
        return None
        
    if CitizenProfile.objects.filter(aadhaar_number=aadhaar_number).exists():
        print(f'Citizen with Aadhaar number "{aadhaar_number}" already exists')
        return None
    
    # Generate password if not provided
    if not password:
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    # Create user
    user = User.objects.create_user(
        username=username,
        password=password,
        user_type='citizen',
        mobile_number=mobile_number
    )
    
    # Create citizen profile
    citizen_profile = CitizenProfile(
        user=user,
        aadhaar_number=aadhaar_number,
        address=address
    )
    
    # Add date of birth if provided
    if date_of_birth:
        try:
            from datetime import datetime
            citizen_profile.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            print('Invalid date format. Please use YYYY-MM-DD')
            user.delete()  # Clean up the user we just created
            return None
    
    citizen_profile.save()
    
    print(f'Successfully created citizen user "{username}" with password "{password}"')
    print(f'Mobile: {mobile_number}, Aadhaar: {aadhaar_number}')
    return user

if __name__ == "__main__":
    # Example usage
    create_citizen(
        username="priya_sharma",
        mobile_number="8877665544",
        aadhaar_number="112233445566",
        address="101, Elm Road, Sample City",
        password="priyapass101",
        date_of_birth="1995-06-15"
    )