from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from gram_panchayate_system.models import OTP
from gram_panchayate_system.authentication.sms import sms_service

class Command(BaseCommand):
    help = 'Test OTP delivery functionality'

    def add_arguments(self, parser):
        parser.add_argument('mobile_number', type=str, help='Mobile number to send test OTP')
        parser.add_argument('--create-user', action='store_true', help='Create test user if not exists')

    def handle(self, *args, **options):
        User = get_user_model()
        mobile_number = options['mobile_number']
        
        self.stdout.write(f"Testing OTP delivery to {mobile_number}...")
        
        # Create test user if requested
        if options['create_user']:
            if User.objects.filter(mobile_number=mobile_number).exists():
                self.stdout.write("User already exists with this mobile number")
            else:
                user = User.objects.create_user(
                    username=f'test_user_{mobile_number[-4:]}',
                    password='testpass123',
                    user_type='citizen',
                    mobile_number=mobile_number
                )
                self.stdout.write(f"Created test user: {user.username}")
        
        # Check if user exists
        try:
            user = User.objects.get(mobile_number=mobile_number, user_type='citizen')
            self.stdout.write("✓ User found in database")
        except User.DoesNotExist:
            self.stdout.write("✗ No citizen user found with this mobile number")
            self.stdout.write("  Use --create-user flag to create a test user")
            return
        
        # Generate OTP
        otp_code = sms_service.generate_otp()
        self.stdout.write(f"Generated OTP: {otp_code}")
        
        # Save OTP to database
        otp_instance = OTP(mobile_number=mobile_number, otp=otp_code)
        otp_instance.save()
        self.stdout.write("✓ OTP saved to database")
        
        # Try to send OTP
        self.stdout.write("Attempting to send OTP...")
        success = sms_service.send_otp(mobile_number, otp_code)
        
        if success:
            self.stdout.write(
                "✓ OTP sending process completed successfully"
            )
        else:
            self.stdout.write(
                "✗ Failed to send OTP"
            )
        
        # Show configuration status
        self.stdout.write("\nSMS Provider Configuration Status:")
        try:
            from django.conf import settings
            if hasattr(settings, 'MSG91_AUTH_KEY'):
                self.stdout.write("  MSG91: Configured")
            else:
                self.stdout.write("  MSG91: Not configured")
                
            if (hasattr(settings, 'TWILIO_ACCOUNT_SID') and 
                hasattr(settings, 'TWILIO_AUTH_TOKEN')):
                self.stdout.write("  Twilio: Configured")
            else:
                self.stdout.write("  Twilio: Not configured")
                
            if hasattr(settings, 'CUSTOM_SMS_API_URL'):
                self.stdout.write("  Custom API: Configured")
            else:
                self.stdout.write("  Custom API: Not configured")
        except Exception as e:
            self.stdout.write(f"  Error checking configuration: {e}")
        
        self.stdout.write(
            "\nNote: If no providers are configured, OTPs will only be logged and not actually sent."
        )