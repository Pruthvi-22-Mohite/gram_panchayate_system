from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gram_panchayate_system.models import CitizenProfile

class Command(BaseCommand):
    help = 'Test citizen registration functionality'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Test data
        test_data = {
            'username': 'test_citizen',
            'mobile_number': '9876543210',
            'password': 'testpassword123',
            'aadhaar_number': '123456789012',
            'address': '123 Test Street, Test City'
        }
        
        # Check if user already exists
        if User.objects.filter(mobile_number=test_data['mobile_number']).exists():
            self.stdout.write(
                self.style.WARNING(f"User with mobile number {test_data['mobile_number']} already exists")
            )
            return
            
        # Create user
        user = User.objects.create_user(
            username=test_data['username'],
            password=test_data['password'],
            user_type='citizen',
            mobile_number=test_data['mobile_number']
        )
        
        # Create citizen profile
        citizen_profile = CitizenProfile(
            user=user,
            aadhaar_number=test_data['aadhaar_number'],
            address=test_data['address']
        )
        citizen_profile.save()
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully created citizen user: {user.username}")
        )
        self.stdout.write(f"Mobile number: {user.mobile_number}")
        self.stdout.write(f"Aadhaar number: {citizen_profile.aadhaar_number}")
        self.stdout.write(f"Address: {citizen_profile.address}")