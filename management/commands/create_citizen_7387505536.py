from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gram_panchayate_system.models import CitizenProfile

class Command(BaseCommand):
    help = 'Create a citizen user with mobile number 7387505536'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check if user already exists
        if User.objects.filter(mobile_number='7387505536').exists():
            self.stdout.write(
                'User with mobile number "7387505536" already exists'
            )
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
        
        self.stdout.write(
            'Successfully created citizen user with mobile number "7387505536"'
        )