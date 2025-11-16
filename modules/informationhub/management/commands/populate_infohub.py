from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from modules.informationhub.models import VillageNotice, MeetingSchedule


class Command(BaseCommand):
    help = 'Populate the Information Hub with sample data (Notices and Meetings)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to populate Information Hub data...'))
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        VillageNotice.objects.all().delete()
        MeetingSchedule.objects.all().delete()
        
        # Create Village Notices
        self.create_notices()
        
        # Create Meeting Schedules
        self.create_meetings()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated Information Hub data!'))
    
    def create_notices(self):
        """Create sample village notices"""
        today = timezone.now().date()
        
        notices = [
            {
                'title': 'Water Supply Maintenance - Schedule Update',
                'description': '''Dear Residents,

Please be informed that routine water supply maintenance will be conducted in the following areas:
- Ward 1: November 20-21, 2025
- Ward 2: November 22-23, 2025
- Ward 3: November 24-25, 2025

Water supply will be temporarily interrupted from 9:00 AM to 5:00 PM during these days.

We request all residents to store sufficient water in advance. Tanker services will be available on request.

For emergencies, contact: 1800-XXX-XXXX

Thank you for your cooperation.''',
                'notice_type': 'general',
                'issued_by': 'Public Works Department',
                'date': today - timedelta(days=2),
            },
            {
                'title': 'URGENT: Village Health Camp - Free Medical Checkup',
                'description': '''URGENT ANNOUNCEMENT

A FREE Health Camp will be organized on November 18-19, 2025, at the Village Community Center.

Services Available:
✓ General Health Checkup
✓ Blood Pressure & Sugar Testing
✓ Eye Examination
✓ Free Medicines
✓ Dental Checkup
✓ Women & Child Health Consultation

Timing: 9:00 AM to 6:00 PM

Supported by: District Health Department & Gram Panchayat

All villagers are requested to participate and benefit from this free service.

Contact: Village Health Officer - 9876543210''',
                'notice_type': 'emergency',
                'issued_by': 'Health & Sanitation Department',
                'date': today - timedelta(days=1),
            },
            {
                'title': 'Swachh Bharat Mission - Cleanliness Drive',
                'description': '''Cleanliness Drive Announcement

As part of the Swachh Bharat Mission, a village-wide cleanliness drive will be conducted on November 17, 2025.

All residents are encouraged to participate in cleaning their surroundings and public spaces.

Activities:
- Waste collection and segregation
- Cleaning of drainage systems
- Plantation drive
- Awareness programs

Meeting Point: Village Square
Time: 7:00 AM

Let's work together for a cleaner and healthier village!

Gram Panchayat Office''',
                'notice_type': 'announcement',
                'issued_by': 'Gram Panchayat Office',
                'date': today - timedelta(days=5),
            },
            {
                'title': 'New Street Lights Installation - Ward 4 & 5',
                'description': '''Infrastructure Development Update

We are pleased to announce the installation of new LED street lights in Ward 4 and Ward 5.

Installation Schedule:
- Ward 4: November 25-28, 2025
- Ward 5: November 29 - December 2, 2025

This project is funded under the MGNREGA scheme and will enhance safety and visibility in these areas.

Expected Benefits:
• Better visibility at night
• Reduced crime rate
• Energy-efficient LED technology
• Lower electricity costs

For queries, contact the Electrical Department.''',
                'notice_type': 'general',
                'issued_by': 'Electrical Department',
                'date': today - timedelta(days=7),
            },
            {
                'title': 'Property Tax Payment Deadline Extended',
                'description': '''Important Notice for Property Owners

The deadline for property tax payment has been extended to December 15, 2025.

Payment Methods:
1. Online through Gram Panchayat portal
2. At Panchayat Office (Mon-Fri, 10 AM - 5 PM)
3. Authorized collection centers

Benefits of Early Payment:
- 5% discount if paid before November 30, 2025
- Avoid penalty charges
- Get property tax receipt instantly

For assistance with online payment, visit our office or call: 1800-123-4567

Gram Panchayat Revenue Department''',
                'notice_type': 'announcement',
                'issued_by': 'Revenue Department',
                'date': today - timedelta(days=10),
            },
            {
                'title': 'Ration Distribution Schedule - December 2025',
                'description': '''Public Distribution System - December 2025

Ration distribution for December 2025 will be conducted as per the following schedule:

White Card Holders: Dec 1-5, 2025
Pink Card Holders: Dec 6-10, 2025
Yellow Card Holders: Dec 11-15, 2025

Distribution Timings: 9:00 AM to 1:00 PM and 2:00 PM to 5:00 PM

Documents Required:
• Ration Card (Original)
• Aadhaar Card
• Previous receipt (if applicable)

Please maintain social distancing and wear masks.

Fair Price Shop, Village Center''',
                'notice_type': 'general',
                'issued_by': 'Food & Supply Department',
                'date': today - timedelta(days=12),
            },
            {
                'title': 'EMERGENCY: Flood Alert & Safety Measures',
                'description': '''URGENT FLOOD ALERT

Due to heavy rainfall in the upstream areas, there is a possibility of flooding in low-lying areas.

Safety Measures:
⚠ Evacuate low-lying areas if water level rises
⚠ Keep emergency kit ready (food, water, medicines, torch)
⚠ Do not cross flooded roads or bridges
⚠ Keep livestock in safe places
⚠ Monitor local announcements

Emergency Contacts:
• Disaster Management: 1077
• Gram Panchayat Control Room: 9876543210
• Ambulance: 108
• Police: 100

Relief camps will be set up at:
1. Primary School Building
2. Community Hall
3. Panchayat Office

Stay Safe. Stay Alert.''',
                'notice_type': 'emergency',
                'issued_by': 'Disaster Management Cell',
                'date': today,
            },
            {
                'title': 'Scholarship Applications Open for Students',
                'description': '''Educational Scholarship Announcement

Applications are invited for merit-based scholarships for students from economically weaker sections.

Eligibility:
• Students from Class 8 to Class 12
• Family income below ₹2,00,000 per annum
• Minimum 60% marks in previous class
• Resident of the village

Scholarship Amount:
- Class 8-10: ₹5,000 per year
- Class 11-12: ₹8,000 per year

Documents Required:
1. School certificates
2. Income certificate
3. Aadhaar card copy
4. Bank account details
5. Recent photograph

Last Date: November 30, 2025

Apply at Gram Panchayat Office or download form from website.

Education Department
Gram Panchayat''',
                'notice_type': 'announcement',
                'issued_by': 'Education Department',
                'date': today - timedelta(days=15),
            },
        ]
        
        for notice_data in notices:
            notice = VillageNotice.objects.create(**notice_data)
            self.stdout.write(f'Created notice: {notice.title}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(notices)} village notices'))
    
    def create_meetings(self):
        """Create sample meeting schedules"""
        today = timezone.now().date()
        
        meetings = [
            {
                'meeting_title': 'Monthly Gram Sabha Meeting',
                'meeting_date': today + timedelta(days=5),
                'time': '10:00',
                'location': 'Village Panchayat Hall',
                'agenda': '''1. Review of previous month's activities and resolutions
2. Budget discussion for ongoing development projects
3. Approval of new infrastructure proposals
4. Water supply and sanitation issues
5. Discussion on village road maintenance
6. MGNREGA work implementation review
7. Any other matter with permission of the chair

All villagers are invited to participate and raise their concerns.''',
                'organized_by': 'Gram Panchayat',
            },
            {
                'meeting_title': 'Women Self Help Group Meeting',
                'meeting_date': today + timedelta(days=3),
                'time': '14:00',
                'location': 'Community Center, Main Road',
                'agenda': '''1. Review of savings and internal lending activities
2. Discussion on new micro-enterprise initiatives
3. Training program on organic farming
4. Health and nutrition awareness session
5. Planning for skill development workshops
6. Loan repayment status review
7. Next quarter planning

All SHG members are requested to attend.''',
                'organized_by': 'Women Development Department',
            },
            {
                'meeting_title': 'Village Education Committee Meeting',
                'meeting_date': today + timedelta(days=7),
                'time': '11:00',
                'location': 'Primary School Building',
                'agenda': '''1. Review of student attendance and dropout rates
2. Mid-day meal program quality assessment
3. Discussion on infrastructure needs (classrooms, toilets)
4. Teacher vacancy and recruitment status
5. Planning for annual sports and cultural activities
6. Parent-teacher engagement strategies
7. Digital literacy program implementation

Parents and teachers are encouraged to participate.''',
                'organized_by': 'Education Committee',
            },
            {
                'meeting_title': 'Health & Sanitation Committee Meeting',
                'meeting_date': today + timedelta(days=10),
                'time': '15:30',
                'location': 'Primary Health Center',
                'agenda': '''1. Review of village health statistics
2. Vaccination coverage and immunization drive
3. Water quality testing results
4. Waste management and segregation progress
5. Toilet construction under Swachh Bharat Mission
6. Planning for health awareness campaigns
7. Discussion on vector-borne disease prevention

Health workers and volunteers requested to attend.''',
                'organized_by': 'Health Department',
            },
            {
                'meeting_title': 'Agriculture Development Discussion',
                'meeting_date': today + timedelta(days=12),
                'time': '09:00',
                'location': 'Krishi Vigyan Kendra',
                'agenda': '''1. Crop insurance scheme awareness
2. Discussion on organic farming techniques
3. Soil health card distribution
4. Water conservation and drip irrigation
5. Marketing of agricultural produce
6. Subsidies and government schemes for farmers
7. Pest control and seasonal advisory

All farmers are welcome to participate and share their experiences.''',
                'organized_by': 'Agriculture Department',
            },
            {
                'meeting_title': 'Youth Welfare and Sports Meeting',
                'meeting_date': today + timedelta(days=15),
                'time': '16:00',
                'location': 'Village Sports Ground',
                'agenda': '''1. Planning for annual sports tournament
2. Formation of youth clubs
3. Career guidance and skill development programs
4. Sports infrastructure development
5. Cultural activities and talent shows
6. Drug abuse awareness campaign
7. Volunteer recruitment for community service

All youth are encouraged to participate and contribute ideas.''',
                'organized_by': 'Youth Welfare Committee',
            },
            # Past meetings
            {
                'meeting_title': 'Road Construction Review Meeting',
                'meeting_date': today - timedelta(days=10),
                'time': '10:30',
                'location': 'Panchayat Office',
                'agenda': '''1. Progress review of ongoing road construction
2. Quality inspection reports
3. Budget utilization analysis
4. Timeline for completion
5. Addressing contractor concerns
6. Planning for next phase''',
                'organized_by': 'Public Works Department',
            },
            {
                'meeting_title': 'Annual Budget Planning Meeting',
                'meeting_date': today - timedelta(days=25),
                'time': '11:00',
                'location': 'Village Panchayat Hall',
                'agenda': '''1. Review of previous year's budget
2. Revenue collection analysis
3. Proposed budget for next fiscal year
4. Priority projects discussion
5. Fund allocation for different departments
6. Approval and finalization''',
                'organized_by': 'Gram Panchayat',
            },
        ]
        
        for meeting_data in meetings:
            meeting = MeetingSchedule.objects.create(**meeting_data)
            self.stdout.write(f'Created meeting: {meeting.meeting_title}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(meetings)} meeting schedules'))
