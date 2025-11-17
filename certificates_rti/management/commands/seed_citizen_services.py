from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from certificates_rti.models import (
    CertificateApplication, CertificateDocument,
    RTIRequest, LandRecordLink, LandParcel
)
from modules.citizen.models import CitizenProfile
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample citizen service data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed citizen services data...'))
        
        # Get or create a citizen user for testing
        citizen_user, created = User.objects.get_or_create(
            username='testcitizen',
            defaults={
                'user_type': 'citizen',
                'first_name': 'Test',
                'last_name': 'Citizen',
                'email': 'citizen@test.com'
            }
        )
        if created:
            citizen_user.set_password('password123')
            citizen_user.save()
            CitizenProfile.objects.create(
                user=citizen_user,
                aadhaar_number='123456789012',
                address='Test Address, Village'
            )
            self.stdout.write(self.style.SUCCESS(f'Created test citizen user: {citizen_user.username}'))
        
        # Create 5 Certificate Applications
        certificate_data = [
            {
                'certificate_type': 'income',
                'full_name': 'Ram Sharma',
                'father_name': 'Mohan Sharma',
                'mother_name': 'Sita Sharma',
                'address': 'Village Rampur, Post Rampur, District Pune',
                'phone': '9876543210',
                'aadhar': '123456789012',
                'reason': 'Required for college admission',
                'status': 'submitted'
            },
            {
                'certificate_type': 'caste',
                'full_name': 'Sunita Patil',
                'father_name': 'Ramesh Patil',
                'mother_name': 'Lata Patil',
                'address': 'Village Sinhagad, Post Sinhagad, District Pune',
                'phone': '9876543211',
                'aadhar': '123456789013',
                'reason': 'Required for government job application',
                'status': 'under_review'
            },
            {
                'certificate_type': 'residence',
                'full_name': 'Vijay Kumar',
                'father_name': 'Suresh Kumar',
                'mother_name': 'Radha Kumar',
                'address': 'Village Bhosari, Post Bhosari, District Pune',
                'phone': '9876543212',
                'aadhar': '123456789014',
                'reason': 'Required for driving license',
                'status': 'approved'
            },
            {
                'certificate_type': 'farmer',
                'full_name': 'Ganesh Desai',
                'father_name': 'Balaji Desai',
                'mother_name': 'Savitri Desai',
                'address': 'Village Lonavala, Post Lonavala, District Pune',
                'phone': '9876543213',
                'aadhar': '123456789015',
                'reason': 'Required for agriculture loan',
                'status': 'submitted'
            },
            {
                'certificate_type': 'senior_citizen',
                'full_name': 'Anant Kulkarni',
                'father_name': 'Dattatraya Kulkarni',
                'mother_name': 'Anusuya Kulkarni',
                'address': 'Village Khadakwasla, Post Khadakwasla, District Pune',
                'phone': '9876543214',
                'aadhar': '123456789016',
                'reason': 'Required for senior citizen benefits',
                'status': 'rejected'
            },
        ]
        
        for data in certificate_data:
            CertificateApplication.objects.create(citizen=citizen_user, **data)
        
        self.stdout.write(self.style.SUCCESS('✅ Created 5 certificate applications'))
        
        # Create 5 RTI Requests
        rti_data = [
            {
                'subject': 'Information about village development funds',
                'description': 'Please provide details about the budget allocation and expenditure for village development in the last financial year.',
                'category': 'general',
                'address': 'Village Rampur, Post Rampur, District Pune',
                'status': 'submitted'
            },
            {
                'subject': 'Details of road construction project',
                'description': 'Requesting information about the tender process and contractor details for the recent road construction project in our village.',
                'category': 'general',
                'address': 'Village Sinhagad, Post Sinhagad, District Pune',
                'status': 'under_review'
            },
            {
                'subject': 'Water supply scheme information',
                'description': 'Please provide information about the proposed water supply scheme, including timeline and budget.',
                'category': 'bpl',
                'address': 'Village Bhosari, Post Bhosari, District Pune',
                'status': 'responded'
            },
            {
                'subject': 'Scholarship scheme details',
                'description': 'Requesting details about scholarship schemes available for SC/ST students in our gram panchayat.',
                'category': 'sc',
                'address': 'Village Lonavala, Post Lonavala, District Pune',
                'status': 'submitted'
            },
            {
                'subject': 'Sanitation project status',
                'description': 'Please provide status update on the sanitation project announced last year.',
                'category': 'general',
                'address': 'Village Khadakwasla, Post Khadakwasla, District Pune',
                'status': 'under_review'
            },
        ]
        
        for data in rti_data:
            RTIRequest.objects.create(citizen=citizen_user, **data)
        
        self.stdout.write(self.style.SUCCESS('✅ Created 5 RTI requests'))
        
        # Create 5 Land Parcels (for search)
        land_parcel_data = [
            {
                'survey_number': '45/2',
                'gat_number': 'G-123',
                'property_id': 'PROP-2025-001',
                'area': Decimal('2.50'),
                'location': 'Village Rampur, Near Temple',
                'ownership_type': 'Private'
            },
            {
                'survey_number': '67/3',
                'gat_number': 'G-456',
                'property_id': 'PROP-2025-002',
                'area': Decimal('1.75'),
                'location': 'Village Sinhagad, Near School',
                'ownership_type': 'Private'
            },
            {
                'survey_number': '89/1',
                'gat_number': 'G-789',
                'property_id': 'PROP-2025-003',
                'area': Decimal('3.00'),
                'location': 'Village Bhosari, Main Road',
                'ownership_type': 'Private'
            },
            {
                'survey_number': '12/4',
                'gat_number': 'G-101',
                'property_id': 'PROP-2025-004',
                'area': Decimal('0.50'),
                'location': 'Village Lonavala, Market Area',
                'ownership_type': 'Government'
            },
            {
                'survey_number': '34/5',
                'gat_number': 'G-202',
                'property_id': 'PROP-2025-005',
                'area': Decimal('4.25'),
                'location': 'Village Khadakwasla, Farmland',
                'ownership_type': 'Private'
            },
        ]
        
        for data in land_parcel_data:
            LandParcel.objects.create(**data)
        
        self.stdout.write(self.style.SUCCESS('✅ Created 5 land parcels'))
        
        # Create 5 Land Record Link Requests
        land_link_data = [
            {
                'survey_number': '45/2',
                'gat_number': 'G-123',
                'property_id': 'PROP-2025-001',
                'status': 'submitted'
            },
            {
                'survey_number': '67/3',
                'gat_number': 'G-456',
                'property_id': 'PROP-2025-002',
                'status': 'verified'
            },
            {
                'survey_number': '89/1',
                'gat_number': 'G-789',
                'property_id': 'PROP-2025-003',
                'status': 'submitted'
            },
            {
                'survey_number': '34/5',
                'gat_number': 'G-202',
                'property_id': 'PROP-2025-005',
                'status': 'rejected',
                'remarks': 'Ownership documents unclear'
            },
            {
                'survey_number': '12/4',
                'gat_number': 'G-101',
                'property_id': 'PROP-2025-004',
                'status': 'verified'
            },
        ]
        
        for data in land_link_data:
            # Note: We can't upload actual files in seed command, so ownership_proof will be None
            LandRecordLink.objects.create(citizen=citizen_user, **data)
        
        self.stdout.write(self.style.SUCCESS('✅ Created 5 land record linking requests'))
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Successfully seeded all citizen services data!'))
        self.stdout.write(self.style.SUCCESS('Test citizen user: testcitizen / password123'))
