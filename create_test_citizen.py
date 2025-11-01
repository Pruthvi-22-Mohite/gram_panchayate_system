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

def create_test_citizen():
    """Create a test citizen user with proper mobile number"""
    User = get_user_model()
    
    # Check if test citizen already exists
    if User.objects.filter(username='test_citizen').exists():
        print("Test citizen user already exists")
        user = User.objects.get(username='test_citizen')
        if not user.mobile_number:
            user.mobile_number = '9876543210'
            user.save()
            print("Updated mobile number for test citizen")
        return
    
    # Create test citizen user
    try:
        citizen_user = User.objects.create_user(
            username='test_citizen',
            password='citizen123',  # Not used for citizen login
            user_type='citizen',
            mobile_number='9876543210'
        )
        print("Test citizen user created successfully!")
        print(f"Username: {citizen_user.username}")
        print(f"Mobile: {citizen_user.mobile_number}")
    except Exception as e:
        print(f"Failed to create test citizen user: {e}")

if __name__ == "__main__":
    create_test_citizen()