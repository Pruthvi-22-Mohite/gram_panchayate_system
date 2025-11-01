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
from gram_panchayate_system.models import CustomUser

def test_login_redirects():
    """Test login redirects for different user types"""
    client = Client()
    
    # Create test users if they don't exist
    User = get_user_model()
    
    # Create admin user
    if not User.objects.filter(username='test_admin').exists():
        admin_user = User.objects.create_user(
            username='test_admin',
            password='admin123',
            user_type='admin',
            mobile_number='9999999991'
        )
        print("Created test admin user")
    
    # Create clerk user
    if not User.objects.filter(username='test_clerk').exists():
        clerk_user = User.objects.create_user(
            username='test_clerk',
            password='clerk123',
            user_type='clerk',
            mobile_number='9999999992'
        )
        print("Created test clerk user")
    
    # Create citizen user
    if not User.objects.filter(username='test_citizen').exists():
        citizen_user = User.objects.create_user(
            username='test_citizen',
            password='citizen123',  # Not used for citizen login
            user_type='citizen',
            mobile_number='9999999993'
        )
        print("Created test citizen user")
    
    print("\nTesting login redirects...")
    
    # Test admin login
    print("1. Testing admin login...")
    response = client.post('/admin-login/', {
        'username': 'test_admin',
        'password': 'admin123'
    })
    print(f"   Admin login response status: {response.status_code}")
    print(f"   Admin login redirect URL: {response.url}")
    
    # Test clerk login
    print("2. Testing clerk login...")
    response = client.post('/clerk-login/', {
        'username': 'test_clerk',
        'password': 'clerk123'
    })
    print(f"   Clerk login response status: {response.status_code}")
    print(f"   Clerk login redirect URL: {response.url}")
    
    print("\nLogin redirect tests completed!")

if __name__ == "__main__":
    test_login_redirects()