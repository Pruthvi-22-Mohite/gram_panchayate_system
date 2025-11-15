from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gram_panchayate_system.models import AdminProfile, ClerkProfile, CitizenProfile

class Command(BaseCommand):
    help = 'Create initial users for testing'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                password='admin123',
                user_type='admin',
                is_staff=True,
                is_superuser=True
            )
            admin_profile = AdminProfile(
                user=admin_user,
                designation='System Administrator',
                department='IT Department'
            )
            admin_profile.save()
            self.stdout.write(
                'Successfully created admin user "admin" with password "admin123"'
            )
        
        # Create clerk user
        if not User.objects.filter(username='clerk').exists():
            clerk_user = User.objects.create_user(
                username='clerk',
                password='clerk123',
                user_type='clerk',
                mobile_number='9876543210'
            )
            clerk_profile = ClerkProfile(
                user=clerk_user,
                panchayat_name='Sample Panchayat',
                designation='Data Entry Operator',
                employee_id='CLK001'
            )
            clerk_profile.save()
            self.stdout.write(
                'Successfully created clerk user "clerk" with password "clerk123"'
            )
        
        # Create citizen user
        if not User.objects.filter(username='citizen').exists():
            citizen_user = User.objects.create_user(
                username='citizen',
                password='citizen123',
                user_type='citizen',
                mobile_number='9876543211'
            )
            citizen_profile = CitizenProfile(
                user=citizen_user,
                aadhaar_number='123456789012',
                address='123, Sample Street, Sample City'
            )
            citizen_profile.save()
            self.stdout.write(
                'Successfully created citizen user "citizen" with password "citizen123"'
            )
        
        self.stdout.write(
            'Initial users created successfully!'
        )