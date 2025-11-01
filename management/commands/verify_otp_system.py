from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gram_panchayate_system.models import OTP
from gram_panchayate_system.authentication.sms import sms_service

class Command(BaseCommand):
    help = 'Verify OTP system functionality'

    def handle(self, *args, **options):
        self.stdout.write("=== OTP System Verification ===\n")
        
        # Test OTP generation
        self.stdout.write("1. Testing OTP generation...")
        otp = sms_service.generate_otp()
        self.stdout.write(f"   Generated OTP: {otp}")
        self.stdout.write(f"   OTP length: {len(otp)}")
        self.stdout.write(f"   Is numeric: {otp.isdigit()}")
        
        # Test OTP sending (mock)
        self.stdout.write("\n2. Testing OTP sending (mock implementation)...")
        mobile_number = "9876543210"
        success = sms_service.send_otp(mobile_number, otp)
        self.stdout.write(f"   Send result: {'Success' if success else 'Failed'}")
        
        # Test with a real user (if exists)
        self.stdout.write("\n3. Testing with existing user...")
        User = get_user_model()
        try:
            # Try to find a citizen user
            user = User.objects.filter(user_type='citizen').first()
            if user:
                self.stdout.write(f"   Found citizen user: {user.username} ({user.mobile_number})")
                otp2 = sms_service.generate_otp()
                success2 = sms_service.send_otp(user.mobile_number, otp2)
                self.stdout.write(f"   OTP sent to {user.mobile_number}: {'Success' if success2 else 'Failed'}")
            else:
                self.stdout.write("   No citizen users found in database")
        except Exception as e:
            self.stdout.write(f"   Error testing with real user: {e}")
        
        self.stdout.write("\n=== Verification Complete ===")
        self.stdout.write("Note: OTPs are currently only logged, not actually sent.")
        self.stdout.write("To enable real SMS sending, configure an SMS provider in settings.py")