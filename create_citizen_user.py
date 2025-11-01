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

def create_citizen_user():
    """Create a citizen user with the specified mobile number"""
    User = get_user_model()
    
    # Check if user already exists
    if User.objects.filter(mobile_number='7387505536').exists():
        print("Citizen user with mobile number 7387505536 already exists")
        return
    
    # Create user
    user = User.objects.create_user(
        username='citizen_7387505536',
        password='citizen123',  # Not used for citizen login
        user_type='citizen',
        mobile_number='7387505536'
    )
    
    # Create citizen profile
    citizen_profile = CitizenProfile(
        user=user,
        aadhaar_number='738750553612',
        address='738 Test Address'
    )
    citizen_profile.save()
    
    print("Citizen user created successfully!")
    print(f"Username: {user.username}")
    print(f"Mobile: {user.mobile_number}")

if __name__ == "__main__":
    create_citizen_user()