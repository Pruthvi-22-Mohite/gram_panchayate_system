from django.core.management.base import BaseCommand
from modules.emergencydirectory.models import EmergencyContact


class Command(BaseCommand):
    help = 'Populate Emergency Directory with sample contacts'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to populate Emergency Directory...'))
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        EmergencyContact.objects.all().delete()
        
        # Create emergency contacts
        contacts = [
            {
                'contact_name': 'Police Control Room',
                'contact_type': 'police',
                'phone_number': '100',
                'address': 'Police Station, Main Road, Village Center',
                'email': 'police.station@village.gov.in',
                'available_24x7': True,
                'icon': 'bi-shield-fill',
            },
            {
                'contact_name': 'Fire Brigade',
                'contact_type': 'fire_brigade',
                'phone_number': '101',
                'address': 'Fire Station, Industrial Area, Near Highway',
                'email': 'fire.brigade@village.gov.in',
                'available_24x7': True,
                'icon': 'bi-fire',
            },
            {
                'contact_name': 'Ambulance Service',
                'contact_type': 'ambulance',
                'phone_number': '102',
                'address': 'Government Hospital, Medical Road',
                'email': 'ambulance@village.health.gov.in',
                'available_24x7': True,
                'icon': 'bi-plus-square-fill',
            },
            {
                'contact_name': 'Disaster Management Cell',
                'contact_type': 'disaster',
                'phone_number': '108',
                'address': 'Collectorate Building, Administrative Block',
                'email': 'disaster@district.gov.in',
                'available_24x7': True,
                'icon': 'bi-exclamation-triangle-fill',
            },
            {
                'contact_name': 'Government Hospital',
                'contact_type': 'hospital',
                'phone_number': '02345-234567',
                'address': 'Government Civil Hospital, Medical Road, Taluka Headquarters',
                'email': 'gh.hospital@health.maharashtra.gov.in',
                'available_24x7': True,
                'icon': 'bi-hospital-fill',
            },
            {
                'contact_name': 'Electricity Department Helpline',
                'contact_type': 'electricity',
                'phone_number': '1912',
                'address': 'MSEDCL Office, Power House Complex, Near Bus Stand',
                'email': 'help.electricity@msedcl.co.in',
                'available_24x7': False,
                'icon': 'bi-lightning-fill',
            },
            {
                'contact_name': 'Water Supply Department',
                'contact_type': 'water',
                'phone_number': '02345-234590',
                'address': 'Public Works Department, Zilla Parishad Building',
                'email': 'water.supply@village.gov.in',
                'available_24x7': False,
                'icon': 'bi-droplet-fill',
            },
            {
                'contact_name': 'Village Sarpanch - Shri Ramesh Patil',
                'contact_type': 'sarpanch',
                'phone_number': '9876543210',
                'address': 'Gram Panchayat Office, Village Center',
                'email': 'sarpanch@village.grampanchayat.gov.in',
                'available_24x7': False,
                'icon': 'bi-person-badge-fill',
            },
            {
                'contact_name': 'Village Talathi - Shri Suresh Kumar',
                'contact_type': 'talathi',
                'phone_number': '9876543211',
                'address': 'Talathi Kacheri, Near Gram Panchayat Office',
                'email': 'talathi@village.grampanchayat.gov.in',
                'available_24x7': False,
                'icon': 'bi-person-fill',
            },
            {
                'contact_name': 'Women Helpline',
                'contact_type': 'others',
                'phone_number': '1091',
                'address': 'District Police Headquarters, Collectorate Road',
                'email': 'women.helpline@police.maharashtra.gov.in',
                'available_24x7': True,
                'icon': 'bi-telephone-fill',
            },
            {
                'contact_name': 'Child Helpline',
                'contact_type': 'others',
                'phone_number': '1098',
                'address': 'Childline India Foundation, Taluka Office',
                'email': 'childline@district.in',
                'available_24x7': True,
                'icon': 'bi-telephone-fill',
            },
            {
                'contact_name': 'PHC Primary Health Center',
                'contact_type': 'hospital',
                'phone_number': '02345-234580',
                'address': 'Primary Health Center, Village Medical Complex',
                'email': 'phc@village.health.gov.in',
                'available_24x7': False,
                'icon': 'bi-hospital',
            },
        ]
        
        for contact_data in contacts:
            contact = EmergencyContact.objects.create(**contact_data)
            self.stdout.write(f'Created: {contact.contact_name}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(contacts)} emergency contacts!'))
