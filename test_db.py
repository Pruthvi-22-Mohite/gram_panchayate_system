import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_panchayate_system.settings')

# Setup Django
django.setup()

# Test database connection
from django.db import connection

try:
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    print("Database connection successful!")
    print(f"Test result: {result}")
except Exception as e:
    print(f"Database connection failed: {e}")

# Try to import models
try:
    from gram_panchayate_system.models import CustomUser
    print("Models imported successfully!")
except Exception as e:
    print(f"Model import failed: {e}")