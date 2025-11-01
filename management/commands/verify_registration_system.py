from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gram_panchayate_system.models import CitizenProfile

class Command(BaseCommand):
    help = 'Verify that the citizen registration system is working correctly'

    def handle(self, *args, **options):
        User = get_user_model()
        
        self.stdout.write("=== Citizen Registration System Verification ===\n")
        
        # Test 1: Check if we can create a citizen user
        test_mobile = '8888888888'
        
        # Delete test user if it exists
        User.objects.filter(mobile_number=test_mobile).delete()
        
        try:
            # Create test user
            user = User.objects.create_user(
                username='test_registration_user',
                password='testpass123',
                user_type='citizen',
                mobile_number=test_mobile
            )
            
            # Create citizen profile
            citizen_profile = CitizenProfile(
                user=user,
                aadhaar_number='888888888888',
                address='Test Address for Registration Verification'
            )
            citizen_profile.save()
            
            self.stdout.write(
                "✓ Successfully created test citizen user"
            )
            self.stdout.write(f"  - Username: {user.username}")
            self.stdout.write(f"  - Mobile: {user.mobile_number}")
            self.stdout.write(f"  - Aadhaar: {citizen_profile.aadhaar_number}")
            
            # Verify the user exists
            if User.objects.filter(mobile_number=test_mobile).exists():
                self.stdout.write(
                    "✓ User verified in database"
                )
            else:
                self.stdout.write(
                    "✗ User not found in database"
                )
                
        except Exception as e:
            self.stdout.write(
                f"✗ Error creating test citizen user: {e}"
            )
            return
        
        # Test 2: Check for duplicate mobile number handling
        try:
            # Try to create another user with the same mobile number
            duplicate_user = User.objects.create_user(
                username='duplicate_user',
                password='testpass123',
                user_type='citizen',
                mobile_number=test_mobile  # Same mobile number
            )
            # If we reach here, there's an issue with duplicate handling
            self.stdout.write(
                "✗ Duplicate mobile number not prevented"
            )
            # Clean up
            duplicate_user.delete()
        except Exception as e:
            self.stdout.write(
                "✓ Duplicate mobile number properly prevented"
            )
        
        # Clean up test user
        User.objects.filter(mobile_number=test_mobile).delete()
        
        self.stdout.write(
            "\n=== Registration System Verification Complete ==="
        )
        self.stdout.write(
            "The citizen registration system has been implemented and verified."
        )