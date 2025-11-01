from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gram_panchayate_system.models import CitizenProfile
import random
import string

class Command(BaseCommand):
    help = 'Create a citizen user with profile'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the citizen')
        parser.add_argument('mobile_number', type=str, help='Mobile number for the citizen')
        parser.add_argument('aadhaar_number', type=str, help='Aadhaar number for the citizen')
        parser.add_argument('address', type=str, help='Address for the citizen')
        parser.add_argument('--password', type=str, help='Password for the citizen (optional, will be generated if not provided)')
        parser.add_argument('--date_of_birth', type=str, help='Date of birth (YYYY-MM-DD) (optional)')

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check if user already exists
        if User.objects.filter(username=options['username']).exists():
            self.stdout.write(
                self.style.ERROR(f'User with username "{options["username"]}" already exists')
            )
            return
            
        if User.objects.filter(mobile_number=options['mobile_number']).exists():
            self.stdout.write(
                self.style.ERROR(f'User with mobile number "{options["mobile_number"]}" already exists')
            )
            return
            
        if CitizenProfile.objects.filter(aadhaar_number=options['aadhaar_number']).exists():
            self.stdout.write(
                self.style.ERROR(f'Citizen with Aadhaar number "{options["aadhaar_number"]}" already exists')
            )
            return
        
        # Generate password if not provided
        password = options['password']
        if not password:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        # Create user
        user = User.objects.create_user(
            username=options['username'],
            password=password,
            user_type='citizen',
            mobile_number=options['mobile_number']
        )
        
        # Create citizen profile
        citizen_profile = CitizenProfile(
            user=user,
            aadhaar_number=options['aadhaar_number'],
            address=options['address']
        )
        
        # Add date of birth if provided
        if options['date_of_birth']:
            try:
                from datetime import datetime
                citizen_profile.date_of_birth = datetime.strptime(options['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Invalid date format. Please use YYYY-MM-DD')
                )
                user.delete()  # Clean up the user we just created
                return
        
        citizen_profile.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created citizen user "{options["username"]}" with password "{password}"')
        )
        self.stdout.write(
            f'Mobile: {options["mobile_number"]}, Aadhaar: {options["aadhaar_number"]}'
        )