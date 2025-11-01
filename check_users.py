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

def check_users():
    """Check users in the database"""
    User = get_user_model()
    
    print("Users in database:")
    users = User.objects.all()
    for user in users:
        print(f"- {user.username} ({user.user_type}) - {user.mobile_number}")
    
    print("\nCitizen users:")
    citizens = User.objects.filter(user_type='citizen')
    for citizen in citizens:
        print(f"- {citizen.username} - {citizen.mobile_number}")

if __name__ == "__main__":
    check_users()