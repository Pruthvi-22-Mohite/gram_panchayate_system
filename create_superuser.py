import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_panchayate_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created successfully with password 'admin123'")
    else:
        print("Superuser 'admin' already exists")
except Exception as e:
    print(f"Error creating superuser: {e}")