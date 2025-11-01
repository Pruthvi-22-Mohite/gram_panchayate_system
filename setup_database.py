import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_panchayate_system.settings')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from gram_panchayate_system.models import CustomUser

def setup_database():
    """Setup database and create initial users"""
    print("Setting up database...")
    
    # Try to run migrations
    try:
        print("Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("Migrations completed successfully!")
    except Exception as e:
        print(f"Migration error: {e}")
        print("Trying to create tables manually...")
        try:
            execute_from_command_line(['manage.py', 'create_tables'])
            print("Manual table creation completed!")
        except Exception as e2:
            print(f"Manual table creation failed: {e2}")
            return False
    
    # Create initial users
    try:
        print("Creating initial users...")
        execute_from_command_line(['manage.py', 'create_initial_users'])
        print("Initial users created successfully!")
    except Exception as e:
        print(f"User creation error: {e}")
        print("Creating users manually...")
        create_users_manually()
    
    return True

def create_users_manually():
    """Create initial users manually if command fails"""
    User = get_user_model()
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        try:
            admin_user = User.objects.create_user(
                username='admin',
                password='admin123',
                user_type='admin',
                mobile_number='9999999999'
            )
            print("Admin user created successfully!")
        except Exception as e:
            print(f"Failed to create admin user: {e}")
    
    # Create clerk user
    if not User.objects.filter(username='clerk').exists():
        try:
            clerk_user = User.objects.create_user(
                username='clerk',
                password='clerk123',
                user_type='clerk',
                mobile_number='8888888888'
            )
            print("Clerk user created successfully!")
        except Exception as e:
            print(f"Failed to create clerk user: {e}")
    
    # Create sample citizen user
    if not User.objects.filter(username='citizen').exists():
        try:
            citizen_user = User.objects.create_user(
                username='citizen',
                password='citizen123',  # Not used for citizen login
                user_type='citizen',
                mobile_number='9876543210'
            )
            print("Sample citizen user created successfully!")
        except Exception as e:
            print(f"Failed to create citizen user: {e}")

if __name__ == "__main__":
    setup_database()