from django.test import TestCase
from .models import CitizenTaxData
from modules.citizen.models import CitizenProfile
from modules.common.models import CustomUser


class TaxManagementTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_user(
            username='testcitizen',
            password='testpass123',
            mobile_number='9876543210',
            user_type='citizen'
        )
        
        # Create citizen profile with Aadhaar
        self.citizen_profile = CitizenProfile.objects.create(
            user=self.user,
            aadhaar_number='123456789012',
            address='Test Address'
        )
        
        # Create test tax data
        self.tax_data = CitizenTaxData.objects.create(
            aadhaar_number='123456789012',
            property_tax_amount=5000.00,
            property_due_date='2024-03-31',
            property_penalty=0.00,
            property_status='pending',
            water_tax_amount=1200.00,
            water_due_date='2024-04-15',
            water_penalty=100.00,
            water_status='overdue',
            garbage_tax_amount=800.00,
            garbage_due_date='2024-03-20',
            garbage_penalty=50.00,
            garbage_status='overdue',
            health_tax_amount=300.00,
            health_due_date='2024-05-31',
            health_penalty=0.00,
            health_status='pending'
        )
    
    def test_citizen_tax_data_creation(self):
        """Test that citizen tax data is created correctly"""
        self.assertEqual(self.tax_data.aadhaar_number, '123456789012')
        self.assertEqual(self.tax_data.property_tax_amount, 5000.00)
        self.assertEqual(self.tax_data.water_status, 'overdue')
    
    def test_citizen_profile_linked_to_user(self):
        """Test that citizen profile is linked to user correctly"""
        self.assertEqual(self.citizen_profile.user.username, 'testcitizen')
        self.assertEqual(self.citizen_profile.aadhaar_number, '123456789012')
    
    def test_get_status_class_function(self):
        """Test the status class helper function"""
        from .views import get_status_class
        
        self.assertEqual(get_status_class('paid'), 'bg-success')
        self.assertEqual(get_status_class('pending'), 'bg-warning')
        self.assertEqual(get_status_class('overdue'), 'bg-danger')
        self.assertEqual(get_status_class('unknown'), 'bg-secondary')
