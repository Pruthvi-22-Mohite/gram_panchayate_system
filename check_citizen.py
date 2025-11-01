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

def check_citizen_users():
    """Check if citizen user with mobile number 7387505536 exists"""
    User = get_user_model()
    
    print("Checking for citizen users...")
    citizens = User.objects.filter(user_type='citizen')
    print(f"Total citizen users: {citizens.count()}")
    
    # Check specifically for the mobile number
    citizen_with_mobile = User.objects.filter(mobile_number='7387505536')
    if citizen_with_mobile.exists():
        user = citizen_with_mobile.first()
        print(f"Found citizen user with mobile 7387505536: {user.username}")
    else:
        print("No citizen user found with mobile number 7387505536")
        
    # List all citizen users
    print("\nAll citizen users:")
    for citizen in citizens:
        print(f"  - {citizen.username} ({citizen.mobile_number})")

if __name__ == "__main__":
    check_citizen_users()