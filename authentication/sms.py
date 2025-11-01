import random
import logging
# Import requests only when needed to avoid ImportError if not installed
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

class SMSService:
    """
    SMS Service class to handle sending OTPs via SMS
    This implementation supports multiple SMS providers
    """
    
    @staticmethod
    def send_otp(mobile_number, otp):
        """
        Send OTP to the specified mobile number
        Tries multiple SMS providers in order of preference
        """
        try:
            # Try primary SMS provider first
            if hasattr(settings, 'SMS_PROVIDER') and settings.SMS_PROVIDER == 'CUSTOM':
                success = SMSService._send_via_custom_api(mobile_number, otp)
                if success:
                    logger.info(f"OTP {otp} sent to {mobile_number} via custom API")
                    return True
            
            # Try MSG91 as fallback
            if hasattr(settings, 'MSG91_AUTH_KEY'):
                success = SMSService._send_via_msg91(mobile_number, otp)
                if success:
                    logger.info(f"OTP {otp} sent to {mobile_number} via MSG91")
                    return True
            
            # Try Twilio as fallback
            if (hasattr(settings, 'TWILIO_ACCOUNT_SID') and 
                hasattr(settings, 'TWILIO_AUTH_TOKEN') and
                SMSService._is_module_available('twilio')):
                success = SMSService._send_via_twilio(mobile_number, otp)
                if success:
                    logger.info(f"OTP {otp} sent to {mobile_number} via Twilio")
                    return True
            
            # If no providers configured, fall back to mock implementation
            logger.warning(f"No SMS provider configured. Mock sending OTP {otp} to {mobile_number}")
            return True  # Return True to maintain current behavior
            
        except Exception as e:
            logger.error(f"Failed to send OTP to {mobile_number}: {str(e)}")
            return False

    @staticmethod
    def _is_module_available(module_name):
        """
        Check if a module is available
        """
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False

    @staticmethod
    def _send_via_msg91(mobile_number, otp):
        """
        Send OTP via MSG91 API (popular Indian SMS provider)
        """
        try:
            # Import requests only when needed
            import requests
            
            url = "https://api.msg91.com/api/v5/otp"
            headers = {
                "authkey": settings.MSG91_AUTH_KEY,
                "Content-Type": "application/json"
            }
            data = {
                "mobile": mobile_number,
                "otp": otp,
                "otp_length": "6",
                "message": f"Your OTP for Gram Panchayat Portal is: {otp}",
                "sender": getattr(settings, 'MSG91_SENDER_ID', 'GPINFO'),
                "otp_expiry": "10"  # 10 minutes
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"MSG91 OTP send failed for {mobile_number}: {str(e)}")
            return False

    @staticmethod
    def _send_via_twilio(mobile_number, otp):
        """
        Send OTP via Twilio API
        """
        try:
            # Import Twilio only when needed to avoid ImportError if not installed
            import importlib
            twilio_module = importlib.import_module('twilio.rest')
            Client = getattr(twilio_module, 'Client')
            
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your OTP for Gram Panchayat Portal is: {otp}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=mobile_number
            )
            return message.sid is not None
        except Exception as e:
            logger.error(f"Twilio OTP send failed for {mobile_number}: {str(e)}")
            return False

    @staticmethod
    def _send_via_custom_api(mobile_number, otp):
        """
        Send OTP via custom SMS API
        Configure API endpoint and parameters in settings.py
        """
        try:
            # Import requests only when needed
            import requests
            
            if not hasattr(settings, 'CUSTOM_SMS_API_URL'):
                return False
                
            # This is a template - customize based on your SMS provider
            data = {
                "to": mobile_number,
                "message": f"Your OTP for Gram Panchayat Portal is: {otp}",
                "otp": otp
            }
            
            # Add any additional parameters from settings
            if hasattr(settings, 'CUSTOM_SMS_API_PARAMS'):
                data.update(settings.CUSTOM_SMS_API_PARAMS)
            
            response = requests.post(
                settings.CUSTOM_SMS_API_URL,
                data=data,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Custom API OTP send failed for {mobile_number}: {str(e)}")
            return False

    @staticmethod
    def generate_otp():
        """
        Generate a 6-digit OTP
        """
        return str(random.randint(100000, 999999))

# Global instance
sms_service = SMSService()