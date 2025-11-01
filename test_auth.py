import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_panchayate_system.settings')

# Setup Django
django.setup()

from django.contrib.auth import authenticate, login
from gram_panchayate_system.models import CustomUser

def test_user_creation():
    """Test creating a user"""
    try:
        # Check if admin user exists
        if CustomUser.objects.filter(username='admin').exists():
            print("Admin user already exists")
            user = CustomUser.objects.get(username='admin')
        else:
            # Create admin user
            user = CustomUser.objects.create_user(
                username='admin',
                password='admin123',
                user_type='admin',
                mobile_number='9999999999'
            )
            print("Created admin user")
        
        print(f"User details: {user.username}, {user.user_type}, {user.mobile_number}")
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def test_authentication(username, password):
    """Test authenticating a user"""
    try:
        user = authenticate(username=username, password=password)
        if user:
            print(f"Authentication successful for {username}")
            print(f"User type: {user.user_type}")
            return True
        else:
            print(f"Authentication failed for {username}")
            return False
    except Exception as e:
        print(f"Error during authentication: {e}")
        return False

if __name__ == "__main__":
    print("Testing authentication system...")
    
    # Test user creation
    user = test_user_creation()
    
    if user:
        # Test authentication
        test_authentication('admin', 'admin123')
        test_authentication('admin', 'wrongpassword')