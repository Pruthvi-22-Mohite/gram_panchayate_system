// Initialize language setting flag to prevent infinite loops
window.settingLanguage = false;

const translations = {
    "en": {
        "page_title": "Grampanchayat, Koparde",
        "main_title": "Grampanchayat, Koparde",
        "subtitle": "Gram Panchayat Digital Services | Government of India",
        "welcome_main_title": "Welcome to the Grampanchayat, Koparde",
        "welcome_para_1": "कोपर्डे हे सातारा तालुका, सातारा जिल्ह्यातील एक गाव आहे. गावाची लोकसंख्या सुमारे 1,806 असून साक्षरता दर 90% पेक्षा अधिक आहे. येथील प्रमुख व्यवसाय शेती असून बहुसंख्य नागरिक शेतकरी व शेतमजूर आहेत. सातारा शहराजवळ असल्यामुळे गावाला चांगली रस्ता व बस दळणवळण सुविधा उपलब्ध आहे.",
        "welcome_para_2": "कोपर्डे हे सातारा तालुका, सातारा जिल्ह्यातील एक गाव आहे. गावाची लोकसंख्या सुमारे 1,806 असून साक्षरता दर 90% पेक्षा अधिक आहे. येथील प्रमुख व्यवसाय शेती असून बहुसंख्य नागरिक शेतकरी व शेतमजूर आहेत. सातारा शहराजवळ असल्यामुळे गावाला चांगली रस्ता व बस दळणवळण सुविधा उपलब्ध आहे.",
        "citizen_portal": "Citizen Portal",
        "welcome_citizen": "Welcome, Citizen!",
        "logout": "Logout",
        "sidebar_dashboard": "Dashboard",
        "sidebar_financial": "Financial Services",
        "sidebar_grievance": "Grievance Redressal",
        "sidebar_schemes": "Schemes & Subsidies",
        "sidebar_info": "Information Hub",
        "sidebar_requests": "Certificates & RTI",
        "sidebar_engagement": "Citizen Engagement",
        "summary_pending": "Pending Applications",
        "summary_resolved": "Resolved Grievances",
        "summary_due": "Taxes Due",
        "common_services": "Common Services",
        "action_pay_tax": "Pay Property Tax",
        "action_lodge_grievance": "Lodge Grievance",
        "action_pay_water": "Pay Water Bill",
        "action_view_schemes": "View Schemes",
        "action_notices": "Village Notices",
        "action_meetings": "Meeting Schedules",
        "action_asset_tracker": "Asset & Project Tracker",
        "action_emergency_dir": "Emergency Directory",
        "action_lodge_new": "Lodge New Complaint",
        "action_track_grievance": "Track My Grievances",
        "action_all_schemes": "View All Schemes",
        "action_my_schemes": "My Applied Schemes",
        "action_beneficiary_list": "Beneficiary Lists",
        "action_apply_cert": "Apply Certificate",
        "action_submit_rti": "Submit RTI Request",
        "action_link_land": "Link Land Records",
        "action_evoting": "E-Voting & Polls",
        "action_feedback": "Feedback & Suggestions",
        "login_page_title": "Grampanchayat, Koparde - Login",
        "back_main": "Back to Main Page",
        "login_title": "Login",
        "login_id": "Aadhaar / Mobile Number",
        "login_otp": "OTP",
        "login_send_otp": "Send OTP",
        "login_as": "Login As",
        "role_citizen": "Citizen",
        "role_staff": "Panchayat Staff",
        "role_official": "Higher Official",
        "login_button": "Login",
        "access_guide_title": "How to Access Grampanchayat, Koparde",
        "access_guide_intro": "Follow these simple steps to log in and start using the services:",
        // New translations for citizen dashboard
        "my_applications": "My Applications",
        "my_grievances": "My Grievances",
        "pending_taxes": "Pending Taxes",
        "recent_activity": "Recent Activity & Alerts",
        "recent_applications": "Recent Applications:",
        "recent_grievances": "Recent Grievances:",
        "tax_due": "Tax Due:",
        "is_due_on": "is due on",
        "pay_now": "Pay Now",
        "overdue_tax": "Overdue Tax:",
        "was_due_on": "was due on",
        "property_tax_due": "Property Tax Due:",
        "is_due_status": "is due status",
        "on_date": "on",
        "view_details": "View Details",
        "water_tax_due": "Water Tax Due:",
        "garbage_tax_due": "Garbage Tax Due:",
        "health_tax_due": "Health Tax Due:",
        "latest_village_notices": "Latest Village Notices",
        "view_all": "View All",
        "read_more": "Read More",
        "no_notices_available": "No notices available at the moment.",
        "upcoming_meetings": "Upcoming Meetings",
        "meeting": "Meeting",
        "date_time": "Date & Time",
        "location": "Location",
        "action": "Action",
        "no_meetings_scheduled": "No meetings scheduled at the moment.",
        // New translations for base template
        "select_language": "Select Language",
        "english": "English",
        "marathi": "मराठी",
        "hindi": "हिन्दी",
        "welcome_user": "Welcome, {username}!",
        "login": "Login",
        // New translations for login template
        "admin_login": "Admin Login",
        "clerk_login": "Clerk Login",
        "citizen_login": "Citizen Login",
        "new_citizen": "New citizen?",
        "register_here": "Register here",
        // New translations for citizen login template
        "citizen_login_page_title": "Citizen Login - Grampanchayat, Koparde",
        "citizen_login_title": "Citizen Login",
        "login_username": "Username",
        "login_password": "Password",
        "dont_have_account": "Don't have an account?",
        "pending_applications": "Pending Applications",
        "resolved_grievances": "Resolved Grievances",
        "panchayat_budget": "Panchayat Budget Documents",
        "budget_accessibility": "Access our annual budget documents for transparency and accountability.",
        "no_budget_docs": "No budget documents available.",
        "budget_explanation": "View our budget documents to understand how funds are allocated and spent for village development.",
        // New translations for citizen registration template
        "citizen_registration_title": "Citizen Registration - Grampanchayat, Koparde",
        "back_to_login": "Back to Login",
        "citizen_registration": "Citizen Registration",
        "username": "Username",
        "email_address": "Email Address",
        "mobile_number": "Mobile Number",
        "aadhaar_number": "Aadhaar Number",
        "address": "Address",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "register_button": "Register",
        "already_have_account": "Already have an account?",
        "login_here": "Login here",
        // New translations for admin dashboard
        "admin_dashboard_title": "Admin Dashboard - Grampanchayat, Koparde",
        "admin_portal": "Admin Portal",
        "welcome_admin": "Welcome to the admin portal, {username}!",
        "admin_dashboard": "Admin Dashboard",
        "admin_services": "Admin Services",
        "action_manage_clerks": "Manage Clerks",
                "manage_clerks": "Manage Clerks",
        "action_create_clerk": "Create New Clerk",
        "action_manage_citizens": "Manage Citizens",
        "action_view_grievances": "View Grievances",
        "action_reports": "Reports",
        "action_manage_schemes": "Manage Schemes",
        "action_manage_notices": "Manage Notices",
        "action_manage_meetings": "Manage Meetings",
        "action_emergency_directory": "Emergency Directory",
        "action_manage_certificates": "Manage Certificates",
        "action_manage_rti": "Manage RTI Requests",
        "action_manage_land_records": "Manage Land Records",
        // Certificate management translations
        "certificate_applications_admin": "Certificate Applications - Admin View",
        "total_applications": "Total Applications",
        "pending_review": "Pending Review",
        "approved": "Approved",
        "rejected": "Rejected",
        "all_certificate_applications": "All Certificate Applications",
        "citizen": "Citizen",
        "certificate_type": "Certificate Type",
        "assigned_clerk": "Assigned Clerk",
        "applied_on": "Applied On",
        "status": "Status",
        "action": "Action",
        "view": "View",
        "no_certificate_applications": "No certificate applications found.",
        "back_to_dashboard": "Back to Dashboard",
        "action_manage_feedback": "Manage Feedback",
        "action_manage_assets": "Manage Assets",
        "action_manage_projects": "Manage Projects",
        "action_manage_taxes": "Manage Taxes",
        "action_panchayat_budget": "Panchayat Budget",
        // New translations for clerk dashboard
        "clerk_dashboard_title": "Clerk Dashboard - Grampanchayat, Koparde",
        "clerk_portal": "Clerk Portal",
        "welcome_clerk": "Welcome to the clerk portal, {username}!",
        "clerk_dashboard": "Clerk Dashboard",
        "clerk_services": "Clerk Services",
        "action_handle_grievances": "Handle Grievances",
        // Additional translations for missing elements
        "total_clerks": "Total Clerks",
        "total_citizens": "Total Citizens",
        "active_schemes": "Active Schemes",
        "total_users": "Total Users",
        "pending_applications": "Pending Applications",
        "open_grievances": "Open Grievances",
        "emergency": "Emergency Directory",
        "my_certificates": "My Certificates",
        "my_rti_requests": "My RTI Requests",
        "my_land_records": "My Land Records",
        "view_budget": "View Panchayat Budget",
        "pay_garbage_bill": "Pay Garbage Tax",
        "pay_health_bill": "Pay Health Tax",
        // New translations for access guide
        "access_guide_step1": "Step 1: Go to Login",
        "access_guide_step1_title": "Step 1: Navigate to Login",
        "access_guide_step1_desc": "Click on the 'Login' button in the navigation bar at the top of the page.",
        "access_guide_step2": "Step 2: Select User Role",
        "access_guide_step2_title": "Step 2: Select User Role",
        "access_guide_step2_desc": "Choose your user type: Citizen, Clerk, or Admin from the login options.",
        "access_guide_step3": "Step 3: Sign In",
        "access_guide_step3_title": "Step 3: Sign In",
        "access_guide_step3_desc": "Enter your credentials (username/password) or register as a new citizen if you don't have an account.",
        "access_guide_step4": "Step 4: Access Services",
        "access_guide_step4_title": "Step 4: Access Services",
        "access_guide_step4_desc": "After successful login, access your personalized dashboard to use available services.",
        "access_guide_section": "How to Access LokSevaGram",
        "access_guide_steps": "Access Guide Steps",
// New translations for index page
        "community_engagement_title": "Community Engagement",
        "community_engagement_desc": "Active participation in village development",
        "digital_transformation_title": "Digital Transformation",
        "digital_transformation_desc": "Bringing technology to rural governance",
        "transparent_governance_title": "Transparent Governance",
        "transparent_governance_desc": "Open access to public information and records",
        "latest_announcements": "Latest Announcements",
        "issued_by": "Issued by:",
        "view_all_announcements": "View All Announcements",
        "no_announcements": "No announcements available at the moment.",
        "upcoming_meetings_title": "Upcoming Meetings",
        "organized_by": "Organized by:",
        "view_all_meetings": "View All Meetings",
        "no_meetings": "No upcoming meetings scheduled."
    },
    "mr": {
        "page_title": "ग्रामपंचायत, कोपर्डे",
        "main_title": "ग्रामपंचायत, कोपर्डे",
        "subtitle": "ग्रामपंचायत डिजिटल सेवा | भारत सरकार",
        "welcome_main_title": "ग्रामपंचायत, कोपर्डे मध्ये आपले स्वागत आहे",
        "welcome_para_1": "ग्रामपंचायत, कोपर्डे हे आमच्या गावच्या समुदायाला सक्षम करण्यासाठी डिझाइन केलेले एक डिजिटल व्यासपीठ आहे. आम्ही आवश्यक सार्वजनिक सेवा, सामुदाय सहभाग आणि पारदर्शक प्रशासनासाठी एकच प्रवेश बिंदू प्रदान करतो.",
        "welcome_para_2": "आपत्कालीन संपर्क शोधण्यासाठी, अभिप्राय आणि सुझाव सबमिट करण्यासाठी, स्थानिक प्रकल्पांच्या प्रगतीचा मागोवा घेण्यासाठी आणि महत्त्वाच्या सार्वजनिक नोंदी मिळवण्यासाठी या वेबसाइटचे अन्वेषण करा. प्रत्येक रहिवाशासाठी ग्राम प्रशासन अधिक सुलभ आणि कार्यक्षम बनवणे हे आमचे ध्येय आहे.",
        "citizen_portal": "नागरिक पोर्टल",
        "welcome_citizen": "स्वागत आहे, नागरिक!",
        "logout": "लॉगआउट",
        "sidebar_dashboard": "डॅशबोर्ड",
        "sidebar_financial": "आर्थिक सेवा",
        "sidebar_grievance": "तक्रार निवारण",
        "sidebar_schemes": "योजना आणि अनुदान",
        "sidebar_info": "माहिती केंद्र",
        "sidebar_requests": "प्रमाणपत्रे आणि माहितीचा अधिकार",
        "sidebar_engagement": "नागरिक सहभाग",
        "summary_pending": "प्रलंबित अर्ज",
        "summary_resolved": "निवारण झालेल्या तक्रारी",
        "summary_due": "देय कर",
        "common_services": "सामान्य सेवा",
        "action_pay_tax": "मालमत्ता कर भरा",
        "action_lodge_grievance": "तक्रार नोंदवा",
        "action_pay_water": "पाणी बिल भरा",
        "action_view_schemes": "योजना पहा",
        "action_notices": "गावच्या सूचना",
        "action_meetings": "सभेचे वेळापत्रक",
        "action_asset_tracker": "मालमत्ता आणि प्रकल्प ट्रॅकर",
        "action_emergency_dir": "आपत्कालीन निर्देशिका",
        "action_lodge_new": "नवीन तक्रार नोंदवा",
        "action_track_grievance": "माझ्या तक्रारींचा मागोवा घ्या",
        "action_all_schemes": "सर्व योजना पहा",
        "action_my_schemes": "माझ्या अर्ज केलेल्या योजना",
        "action_beneficiary_list": "लाभार्थी याद्या",
        "action_apply_cert": "प्रमाणपत्रासाठी अर्ज करा",
        "action_submit_rti": "माहितीचा अधिकार अर्ज सादर करा",
        "action_link_land": "जमीन रेकॉर्ड लिंक करा",
        "action_evoting": "ई-मतदान आणि मतदान",
        "action_feedback": "अभिप्राय आणि सूचना",
        "login_page_title": "लोकसेवाग्राम - लॉगिन",
        "back_main": "मुख्य पृष्ठावर परत",
        "login_title": "लॉगिन",
        "login_id": "आधार / मोबाइल क्रमांक",
        "login_otp": "ओटीपी",
        "login_send_otp": "ओटीपी पाठवा",
        "login_as": "म्हणून लॉगिन करा",
        "role_citizen": "नागरिक",
        "role_staff": "पंचायत कर्मचारी",
        "role_official": "वरिष्ठ अधिकारी",
        "login_button": "लॉगिन",
        "access_guide_title": "लोकसेवाग्राममध्ये कसे प्रवेश करावे",
        "access_guide_intro": "लॉगिन करण्यासाठी आणि सेवा वापरणे सुरू करण्यासाठी या सोप्या चरणांचे अनुसरण करा:",
        // New translations for citizen dashboard
        "my_applications": "माझे अर्ज",
        "my_grievances": "माझ्या तक्रारी",
        "pending_taxes": "बाकी कर",
        "recent_activity": "अलीकडील क्रियाकलाप आणि सूचना",
        "recent_applications": "अलीकडील अर्ज:",
        "recent_grievances": "अलीकडील तक्रारी:",
        "tax_due": "देय कर:",
        "is_due_on": "ची पात्रता आहे",
        "pay_now": "आता भरा",
        "overdue_tax": "विलंबित कर:",
        "was_due_on": "ची पात्रता होती",
        "property_tax_due": "मालमत्ता कर देय:",
        "is_due_status": "स्थिती देय आहे",
        "on_date": "वर",
        "view_details": "तपशील पहा",
        "water_tax_due": "पाणी कर देय:",
        "garbage_tax_due": "कचरा कर देय:",
        "health_tax_due": "आरोग्य कर देय:",
        "latest_village_notices": "नवीनतम गावाच्या सूचना",
        "view_all": "सर्व पहा",
        "read_more": "अधिक वाचा",
        "no_notices_available": "सध्या कोणत्याही सूचना उपलब्ध नाहीत.",
        "upcoming_meetings": "आगामी बैठकी",
        "meeting": "बैठक",
        "date_time": "दिनांक आणि वेळ",
        "location": "स्थान",
        "action": "कृती",
        "no_meetings_scheduled": "सध्या कोणत्याही बैठकी निर्धारित नाहीत.",
        // New translations for base template
        "select_language": "भाषा निवडा",
        "english": "English",
        "marathi": "मराठी",
        "hindi": "हिन्दी",
        "welcome_user": "स्वागत आहे, {username}!",
        "login": "लॉगिन",
        // New translations for login template
        "admin_login": "प्रशासक लॉगिन",
        "clerk_login": "कर्मचारी लॉगिन",
        "citizen_login": "नागरिक लॉगिन",
        "new_citizen": "नवीन नागरिक?",
        "register_here": "येथे नोंदणी करा",
        // New translations for citizen login template
        "citizen_login_page_title": "नागरिक लॉगिन - लोकसेवाग्राम",
        "citizen_login_title": "नागरिक लॉगिन",
        "login_username": "वापरकर्तानाव",
        "login_password": "संकेतशब्द",
        "dont_have_account": "खाते नाही?",
        // New translations for citizen registration template
        "citizen_registration_title": "नागरिक नोंदणी - लोकसेवाग्राम",
        "back_to_login": "लॉगिन वर परत जा",
        "citizen_registration": "नागरिक नोंदणी",
        "username": "वापरकर्तानाव",
        "email_address": "ईमेल पत्ता",
        "mobile_number": "मोबाइल क्रमांक",
        "aadhaar_number": "आधार क्रमांक",
        "address": "पत्ता",
        "password": "संकेतशब्द",
        "confirm_password": "संकेतशब्दची पुष्टी करा",
        "register_button": "नोंदणी करा",
        "already_have_account": "आधीपासूनच खाते आहे?",
        "login_here": "येथे लॉगिन करा",
        // New translations for admin dashboard
        "admin_dashboard_title": "प्रशासक डॅशबोर्ड - लोकसेवाग्राम",
        "admin_portal": "प्रशासक पोर्टल",
        "welcome_admin": "प्रशासक पोर्टल मध्ये आपले स्वागत आहे, {username}!",
        "admin_dashboard": "प्रशासक डॅशबोर्ड",
        "admin_services": "प्रशासक सेवा",
        "action_manage_clerks": "कर्मचारी व्यवस्थापित करा",
                "manage_clerks": "कर्मचारी व्यवस्थापित करा",
        "action_create_clerk": "नवीन कर्मचारी तयार करा",
        "action_manage_citizens": "नागरिक व्यवस्थापित करा",
        "action_view_grievances": "तक्रारी पहा",
        "action_reports": "अहवाल",
        "action_manage_schemes": "योजना व्यवस्थापित करा",
        "action_manage_notices": "सूचना व्यवस्थापित करा",
        "action_manage_meetings": "सभा व्यवस्थापित करा",
        "action_emergency_directory": "आपत्कालीन निर्देशिका",
        "action_manage_certificates": "प्रमाणपत्रे व्यवस्थापित करा",
        "action_manage_rti": "माहितीचा अधिकार अर्ज व्यवस्थापित करा",
        "action_manage_land_records": "जमीन रेकॉर्ड व्यवस्थापित करा",
        "action_manage_feedback": "अभिप्राय व्यवस्थापित करा",
        "action_manage_assets": "मालमत्ता व्यवस्थापित करा",
        "action_manage_projects": "प्रकल्प व्यवस्थापित करा",
        "action_manage_taxes": "कर व्यवस्थापित करा",
        "action_panchayat_budget": "पंचायत अर्थसंकल्प",
        // New translations for clerk dashboard
        "clerk_dashboard_title": "कर्मचारी डॅशबोर्ड - लोकसेवाग्राम",
        "clerk_portal": "कर्मचारी पोर्टल",
        "welcome_clerk": "कर्मचारी पोर्टल मध्ये आपले स्वागत आहे, {username}!",
        "clerk_dashboard": "कर्मचारी डॅशबोर्ड",
        "clerk_services": "कर्मचारी सेवा",
        "action_handle_grievances": "तक्रारी सांभाळा",
        // Additional translations for missing elements
        "total_clerks": "एकूण कर्मचारी",
        "total_citizens": "एकूण नागरिक",
        "active_schemes": "सक्रिय योजना",
        "total_users": "एकूण वापरकर्ते",
        "pending_applications": "प्रलंबित अर्ज",
        "resolved_grievances": "निराकरण केलेल्या तक्रारी",
        "panchayat_budget": "पंचायत अर्थसंकल्प दस्तावेज",
        "budget_accessibility": "पारदर्शिता आणि जबाबदारीसाठी आमचे वार्षिक अर्थसंकल्प दस्तावेज पाहा.",
        "no_budget_docs": "कोणतेही अर्थसंकल्प दस्तावेज उपलब्ध नाहीत.",
        "budget_explanation": "गाव विकासासाठी निधी कसे वाटप केले जाते आणि खर्च केला जातो याची माहिती मिळविण्यासाठी आमचे अर्थसंकल्प दस्तावेज पहा.",
        "open_grievances": "उघड्या तक्रारी",
        "action_emergency_directory": "आपत्कालीन निर्देशिका",
        "action_panchayat_budget": "पंचायत अर्थसंकल्प",
        "my_certificates": "माझे प्रमाणपत्र",
        "my_rti_requests": "माझे माहितीचे अधिकार विनंती",
        "my_land_records": "माझे जमिनीचे रेकॉर्ड",
        "pay_garbage_bill": "कचरा कर भरा",
        "pay_health_bill": "आरोग्य कर भरा",
        // New translations for access guide in Marathi
        "access_guide_step1": "पाऊल १: लॉगिनला जा",
        "access_guide_step1_title": "पाऊल १: लॉगिनला नेव्हिगेट करा",
        "access_guide_step1_desc": "पृष्ठाच्या शीर्षावरील नेव्हिगेशन बारमध्ये 'लॉगिन' बटणावर क्लिक करा.",
        "access_guide_step2": "पाऊल २: वापरकर्ता भूमिका निवडा",
        "access_guide_step2_title": "पाऊल २: वापरकर्ता भूमिका निवडा",
        "access_guide_step2_desc": "लॉगिन पर्यायांमधून तुमचा वापरकर्ता प्रकार निवडा: नागरिक, क्लर्क किंवा प्रशासक.",
        "access_guide_step3": "पाऊल ३: साइन इन करा",
        "access_guide_step3_title": "पाऊल ३: साइन इन करा",
        "access_guide_step3_desc": "तुमचे क्रेडेंशियल्स (वापरकर्तानाव/पासवर्ड) प्रविष्ट करा किंवा तुमचे खाते नसेल तर नवीन नागरिक म्हणून नोंदणी करा.",
        "access_guide_step4": "पाऊल ४: सेवांमध्ये प्रवेश करा",
        "access_guide_step4_title": "पाऊल ४: सेवांमध्ये प्रवेश करा",
        "access_guide_step4_desc": "यशस्वीपणे लॉगिन केल्यानंतर, उपलब्ध सेवा वापरण्यासाठी तुमचे वैयक्तिक डॅशबोर्ड उघडा.",
        "access_guide_section": "लोकसेवाग्राममध्ये कसे प्रवेश करावे",
        "access_guide_steps": "प्रवेश मार्गदर्शक पायरी",
// New translations for index page
        "community_engagement_title": "समुदाय सहभाग",
        "community_engagement_desc": "गाव के विकास में सक्रिय भागीदारी",
        "digital_transformation_title": "डिजिटल रूपांतरण",
        "digital_transformation_desc": "ग्रामीण शासन के लिए प्रौद्योगिकी लाना",
        "transparent_governance_title": "पारदर्शी शासन",
        "transparent_governance_desc": "सार्वजनिक जानकारी और रिकॉर्ड में खुला पहुंच",
        "latest_announcements": "नवीनतम घोषणा",
        "issued_by": "जारी करने वाला:",
        "view_all_announcements": "सभी घोषणाएं देखें",
        "no_announcements": "इस समय कोई घोषणाएं उपलब्ध नहीं हैं।",
        "upcoming_meetings_title": "आगामी बैठकी",
        "organized_by": "आयोजित करने वाला:",
        "view_all_meetings": "सभी बैठकी पहा",
        "no_meetings": "इस समय कोई बैठकी निर्धारित नहीं हैं।",

    },
    "hi": {
        "page_title": "ग्रामपंचायत, कोपर्डे",
        "main_title": "ग्रामपंचायत, कोपर्डे",
        "subtitle": "ग्राम पंचायत डिजिटल सेवाएँ | भारत सरकार",
        "welcome_main_title": "ग्रामपंचायत, कोपर्डे में आपका स्वागत है",
        "welcome_para_1": "ग्रामपंचायत, कोपर्डे हमारे गाँव के समुदाय को सशक्त बनाने के लिए डिज़ाइन किया गया एक डिजिटल प्लेटफॉर्म है। हम आवश्यक सार्वजनिक सेवाओं, सामुदायिक जुड़ाव और पारदर्शी शासन के लिए एक ही पहुंच बिंदु प्रदान करते हैं।",
        "welcome_para_2": "आपातकालीन संपर्क खोजने, प्रतिक्रिया और सुझाव प्रस्तुत करने, स्थानीय परियोजनाओं की प्रगति को ट्रैक करने और महत्वपूर्ण सार्वजनिक अभिलेखों तक पहुंचने के लिए इस वेबसाइट का अन्वेषण करें। हमारा लक्ष्य प्रत्येक निवासी के लिए ग्राम प्रशासन को अधिक सुलभ और कुशल बनाना है।",
        "citizen_portal": "नागरिक पोर्टल",
        "welcome_citizen": "आपका स्वागत है, नागरिक!",
        "logout": "लॉगआउट",
        "sidebar_dashboard": "डैशबोर्ड",
        "sidebar_financial": "वित्तीय सेवाएं",
        "sidebar_grievance": "शिकायत निवारण",
        "sidebar_schemes": "योजनाएं और सब्सिडी",
        "sidebar_info": "सूचना केंद्र",
        "sidebar_requests": "प्रमाणपत्र और आरटीआई",
        "sidebar_engagement": "नागरिक सहभागिता",
        "summary_pending": "लंबित आवेदन",
        "summary_resolved": "निवारण की गई शिकायतें",
        "summary_due": "देय कर",
        "common_services": "सामान्य सेवाएँ",
        "action_pay_tax": "संपत्ति कर का भुगतान करें",
        "action_lodge_grievance": "शिकायत दर्ज करें",
        "action_pay_water": "पानी का बिल भरें",
        "action_view_schemes": "योजनाएं देखें",
        "action_notices": "गांव की सूचनाएं",
        "action_meetings": "बैठक का कार्यक्रम",
        "action_asset_tracker": "संपत्ति और परियोजना ट्रैकर",
        "action_emergency_dir": "आपातकालीन निर्देशिका",
        "action_lodge_new": "नई शिकायत दर्ज करें",
        "action_track_grievance": "मेरी शिकायतों को ट्रैक करें",
        "action_all_schemes": "सभी योजनाएं देखें",
        "action_my_schemes": "मेरी लागू की गई योजनाएं",
        "action_beneficiary_list": "लाभार्थी सूची",
        "action_apply_cert": "प्रमाणपत्र के लिए आवेदन करें",
        "action_submit_rti": "आरटीआई अनुरोध सबमिट करें",
        "action_link_land": "भूमि रिकॉर्ड लिंक करें",
        "action_evoting": "ई-वोटिंग और चुनाव",
        "action_feedback": "प्रतिक्रिया और सुझाव",
        "login_page_title": "लोकसेवाग्राम - लॉगिन",
        "back_main": "मुख्य पृष्ठ पर वापस जाएं",
        "login_title": "लॉगिन",
        "login_id": "आधार / मोबाइल नंबर",
        "login_otp": "ओटीपी",
        "login_send_otp": "ओटीपी भेजें",
        "login_as": "के रूप में लॉगिन करें",
        "role_citizen": "नागरिक",
        "role_staff": "पंचायत कर्मचारी",
        "role_official": "उच्च अधिकारी",
        "login_button": "लॉगिन",
        "action_my_schemes": "मेरी लागू की गई योजनाएं",
        "action_beneficiary_list": "लाभार्थी सूची",
        "access_guide_title": "लोकसेवाग्राम में कैसे पहुंचें",
        "access_guide_intro": "लॉग इन करने और सेवाओं का उपयोग शुरू करने के लिए इन सरल चरणों का पालन करें:",
        "access_guide_step1": "चरण 1: लॉगिन पर जाएं",
        "access_guide_step1_title": "चरण 1: लॉगिन पर नेविगेट करें",
        "access_guide_step1_desc": "पृष्ठ के शीर्ष पर नेविगेशन बार में \"लॉगिन\" बटन पर क्लिक करें।",
        "access_guide_step2": "चरण 2: उपयोगकर्ता भूमिका चुनें",
        "access_guide_step2_title": "चरण 2: उपयोगकर्ता भूमिका चुनें",
        "access_guide_step2_desc": "लॉगिन विकल्पों से अपना उपयोगकर्ता प्रकार चुनें: नागरिक, क्लर्क या एडमिन।",
        "access_guide_step3": "चरण 3: साइन इन करें",
        "access_guide_step3_title": "चरण 3: साइन इन करें",
        "access_guide_step3_desc": "अपने क्रेडेंशियल्स (उपयोगकर्ता नाम/पासवर्ड) दर्ज करें या यदि आपके पास खाता नहीं है तो नया नागरिक के रूप में पंजीकरण करें।",
        "access_guide_step4": "चरण 4: सेवाओं तक पहुंचें",
        "access_guide_step4_title": "चरण 4: सेवाओं तक पहुंचें",
        "access_guide_step4_desc": "सफल लॉगिन के बाद, उपलब्ध सेवाओं का उपयोग करने के लिए अपने व्यक्तिगत डैशबोर्ड तक पहुंचें।",
        "access_guide_steps": "पहुंच गाइड चरण",
        "access_guide_section": "लोकसेवाग्राम तक पहुंच कैसे प्राप्त करें",
// New translations for citizen dashboard
        "my_applications": "मेरे आवेदन",
        "my_grievances": "मेरी शिकायतें",
        "pending_taxes": "लंबित कर",
        "recent_activity": "हाल की गतिविधि और अलर्ट",
        "recent_applications": "हाल के आवेदन:",
        "recent_grievances": "हाल की शिकायतें:",
        "tax_due": "कर बकाया:",
        "is_due_on": "की नियत तारीख है",
        "pay_now": "अभी भुगतान करें",
        "overdue_tax": "अतिदेय कर:",
        "was_due_on": "की नियत तारीख थी",
        "property_tax_due": "संपत्ति कर बकाया:",
        "is_due_status": "बकाया है स्थिति",
        "on_date": "पर",
        "view_details": "विवरण देखें",
        "water_tax_due": "पानी कर बकाया:",
        "garbage_tax_due": "कचरा कर बकाया:",
        "health_tax_due": "स्वास्थ्य कर बकाया:",
        "latest_village_notices": "नवीनतम गांव की सूचनाएं",
        "view_all": "सभी देखें",
        "read_more": "और पढ़ें",
        "no_notices_available": "इस समय कोई सूचनाएं उपलब्ध नहीं हैं।",
        "upcoming_meetings": "आगामी बैठकें",
        "meeting": "बैठक",
        "date_time": "दिनांक और समय",
        "location": "स्थान",
        "action": "कार्य",
        "no_meetings_scheduled": "इस समय कोई बैठकें निर्धारित नहीं हैं।",
        // New translations for base template
        "select_language": "भाषा चुनें",
        "english": "English",
        "marathi": "मराठी",
        "hindi": "हिन्दी",
        "welcome_user": "स्वागत है, {username}!",
        "login": "लॉगिन",
        // New translations for login template
        "admin_login": "व्यवस्थापक लॉगिन",
        "clerk_login": "कर्मचारी लॉगिन",
        "citizen_login": "नागरिक लॉगिन",
        "new_citizen": "नया नागरिक?",
        "register_here": "यहाँ पंजीकरण करें",
        // New translations for citizen login template
        "citizen_login_page_title": "नागरिक लॉगिन - लोकसेवाग्राम",
        "citizen_login_title": "नागरिक लॉगिन",
        "login_username": "उपयोगकर्ता नाम",
        "login_password": "पासवर्ड",
        "dont_have_account": "खाता नहीं है?",
        // New translations for citizen registration template
        "citizen_registration_title": "नागरिक पंजीकरण - लोकसेवाग्राम",
        "back_to_login": "लॉगिन पर वापस जाएं",
        "citizen_registration": "नागरिक पंजीकरण",
        "username": "उपयोगकर्ता नाम",
        "email_address": "ईमेल पता",
        "mobile_number": "मोबाइल नंबर",
        "aadhaar_number": "आधार नंबर",
        "address": "पता",
        "password": "पासवर्ड",
        "confirm_password": "पासवर्ड की पुष्टि करें",
        "register_button": "रजिस्टर करें",
        "already_have_account": "पहले से ही एक खाता है?",
        "login_here": "यहाँ लॉगिन करें",
        // New translations for admin dashboard
        "admin_dashboard_title": "व्यवस्थापक डैशबोर्ड - लोकसेवाग्राम",
        "admin_portal": "व्यवस्थापक पोर्टल",
        "welcome_admin": "व्यवस्थापक पोर्टल में आपका स्वागत है, {username}!",
        "admin_dashboard": "व्यवस्थापक डैशबोर्ड",
        "admin_services": "व्यवस्थापक सेवाएँ",
        "action_manage_clerks": "कर्मचारियों का प्रबंधन करें",
                "manage_clerks": "कर्मचारियों का प्रबंधन करें",
        "action_create_clerk": "नया कर्मचारी बनाएं",
        "action_manage_citizens": "नागरिकों का प्रबंधन करें",
        "action_view_grievances": "शिकायतें देखें",
        "action_reports": "रिपोर्ट्स",
        "action_manage_schemes": "योजनाओं का प्रबंधन करें",
        "action_manage_notices": "सूचनाओं का प्रबंधन करें",
        "action_manage_meetings": "बैठकों का प्रबंधन करें",
        "action_emergency_directory": "आपातकालीन निर्देशिका",
        "action_manage_certificates": "प्रमाणपत्रों का प्रबंधन करें",
        "action_manage_rti": "आरटीआई अनुरोधों का प्रबंधन करें",
        "action_manage_land_records": "भूमि रिकॉर्ड का प्रबंधन करें",
        // Certificate management translations
        "certificate_applications_admin": "प्रमाणपत्र आवेदन - व्यवस्थापक दृश्य",
        "total_applications": "कुल आवेदन",
        "pending_review": "समीक्षा लंबित",
        "approved": "अनुमोदित",
        "rejected": "अस्वीकृत",
        "all_certificate_applications": "सभी प्रमाणपत्र आवेदन",
        "citizen": "नागरिक",
        "certificate_type": "प्रमाणपत्र प्रकार",
        "assigned_clerk": "नियुक्त कर्मचारी",
        "applied_on": "आवेदन किया गया",
        "status": "स्थिति",
        "action": "कार्य",
        "view": "देखें",
        "no_certificate_applications": "कोई प्रमाणपत्र आवेदन नहीं मिला।",
        "back_to_dashboard": "डैशबोर्ड पर वापस जाएं",
        "action_manage_feedback": "प्रतिक्रियाओं का प्रबंधन करें",
        "action_manage_assets": "संपत्ति का प्रबंधन करें",
        "action_manage_projects": "परियोजनाओं का प्रबंधन करें",
        "action_manage_taxes": "करों का प्रबंधन करें",
        "action_panchayat_budget": "पंचायत बजट",
        // New translations for clerk dashboard
        "clerk_dashboard_title": "कर्मचारी डैशबोर्ड - लोकसेवाग्राम",
        "clerk_portal": "कर्मचारी पोर्टल",
        "welcome_clerk": "कर्मचारी पोर्टल में आपका स्वागत है, {username}!",
        "clerk_dashboard": "कर्मचारी डैशबोर्ड",
        "clerk_services": "कर्मचारी सेवाएँ",
        "action_handle_grievances": "शिकायतों को संभालें",
        // Additional translations for missing elements
        "total_clerks": "कुल कर्मचारी",
        "total_citizens": "कुल नागरिक",
        "active_schemes": "सक्रिय योजनाएं",
        "total_users": "कुल उपयोगकर्ता",
        "pending_applications": "लंबित आवेदन",
        "resolved_grievances": "निवारित शिकायतें",
        "panchayat_budget": "पंचायत बजट दस्तावेज",
        "budget_accessibility": "पारदर्शिता और जवाबदेही के लिए हमारे वार्षिक बजट दस्तावेज़ देखें.",
        "no_budget_docs": "कोई बजट दस्तावेज़ उपलब्ध नहीं हैं.",
        "budget_explanation": "गांव के विकास के लिए निधि कैसे आवंटित और खर्च की जाती है यह समझने के लिए हमारे बजट दस्तावेज़ देखें.",
        "open_grievances": "खुली शिकायतें",
        "emergency": "आपातकालीन निर्देशिका",
        "my_certificates": "मेरे प्रमाणपत्र",
        "my_rti_requests": "मेरे आरटीआई अनुरोध",
        "my_land_records": "मेरे भूमि रिकॉर्ड",
        "view_budget": "पंचायत बजट देखें",
        "pay_garbage_bill": "कचरा कर भरें",
        "pay_health_bill": "स्वास्थ्य कर भरें",
        // New translations for index page
        "community_engagement_title": "सामुदायिक सहभागिता",
        "community_engagement_desc": "गांव के विकास में सक्रिय भागीदारी",
        "digital_transformation_title": "डिजिटल रूपांतरण",
        "digital_transformation_desc": "ग्रामीण शासन के लिए प्रौद्योगिकी लाना",
        "transparent_governance_title": "पारदर्शी शासन",
        "transparent_governance_desc": "सार्वजनिक जानकारी और रिकॉर्ड में खुला पहुंच",
        "latest_announcements": "नवीनतम घोषणाएं",
        "issued_by": "जारी करने वाला:",
        "view_all_announcements": "सभी घोषणाएं देखें",
        "no_announcements": "इस समय कोई घोषणाएं उपलब्ध नहीं हैं।",
        "upcoming_meetings_title": "आगामी बैठकें",
        "organized_by": "आयोजित करने वाला:",
        "view_all_meetings": "सभी बैठकें देखें",
        "no_meetings": "इस समय कोई बैठकें निर्धारित नहीं हैं।"
    }
};
// Handle dynamic content with placeholders
const interpolate = (str, params) => {
    return str.replace(/\{([^}]+)\}/g, (match, key) => {
        return params[key] || match;
    });
};

// Function to force translate all elements with data-lang-key
const forceTranslateAll = (lang) => {
    document.querySelectorAll('[data-lang-key]').forEach(element => {
        const key = element.getAttribute('data-lang-key');
        if (translations[lang] && translations[lang][key]) {
            let translatedText = translations[lang][key];
            
            // Handle dynamic content
            if (key.includes('welcome') && window.userUsername) {
                translatedText = interpolate(translatedText, { username: window.userUsername });
            }
            
            if (element.tagName === 'TITLE') {
                document.title = translatedText;
            } else {
                element.innerText = translatedText;
            }
        }
    });
};

const setLanguage = async (lang) => {
    // Persist language selection to server
    try {
        const response = await fetch('/common/switch-language/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
            },
            body: `language=${lang}`
        });
        
        if (!response.ok) {
            console.warn('Failed to save language preference to server');
        }
    } catch (error) {
        console.warn('Error saving language preference:', error);
    }
    
    // Apply translations to all elements with data-lang-key attribute
    document.querySelectorAll('[data-lang-key]').forEach(element => {
        let key = element.getAttribute('data-lang-key');
        
        // For title elements, dynamically determine the appropriate translation key based on content
        if (element.tagName === 'TITLE') {
            const titleContent = element.textContent.trim();
            
            // Map specific title content to appropriate translation keys
            if (titleContent.includes('Admin Dashboard')) {
                key = 'admin_dashboard_title';
            } else if (titleContent.includes('Citizen Login')) {
                key = 'citizen_login_page_title';
            } else if (titleContent.includes('Citizen Registration')) {
                key = 'citizen_registration_title';
            } else if (titleContent.includes('Clerk Dashboard')) {
                key = 'clerk_dashboard_title';
            } else {
                // Default to page_title for generic pages
                key = 'page_title';
            }
        }
        
        if (translations[lang] && translations[lang][key]) {
            let translatedText = translations[lang][key];
            
            // Handle dynamic content like welcome messages
            if (key.includes('welcome') && window.userUsername) {
                translatedText = interpolate(translatedText, { username: window.userUsername });
            }
            
            if (element.tagName === 'TITLE') {
                document.title = translatedText;
            } else {
                element.innerText = translatedText;
            }
        }
    });
    

    
    // Store language preference in multiple places for redundancy
    localStorage.setItem('userLanguage', lang);
    sessionStorage.setItem('userLanguage', lang);
    
    // Set HTML lang attribute
    document.documentElement.lang = lang;
    
    const langSwitcher = document.getElementById('language-switcher');
    if (langSwitcher) langSwitcher.value = lang;
    
    // Only call if not already in dashboard context to prevent recursion
    if (document.querySelector('.sidebar') && !window.settingLanguage) {
        // Set flag to prevent recursive calls
        window.settingLanguage = true;
        renderSummaryCards();
        // Reset flag after a delay
        setTimeout(() => {
            window.settingLanguage = false;
        }, 300);
    }
};
// ==========================================================
//  PAGE INITIALIZATION
// ==========================================================
async function initializeLanguage() {
    // First, try to get language from server-side session/cookie
    try {
        const response = await fetch('/common/get-current-language/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.language) {
                // Server has a language preference, use it
                return data.language;
            }
        }
    } catch (error) {
        console.log('Could not fetch server language preference');
    }
    
    // Fallback to client-side storage
    return sessionStorage.getItem('userLanguage') || 
           localStorage.getItem('userLanguage') || 
           document.documentElement.lang || 
           'en';
}

document.addEventListener('DOMContentLoaded', async () => {
    const langSwitcher = document.getElementById('language-switcher');
    if (langSwitcher) {
        langSwitcher.addEventListener('change', (event) => setLanguage(event.target.value));
    }
    
    // Initialize language with server-side preference
    const savedLang = await initializeLanguage();
    await setLanguage(savedLang);

    if (document.querySelector('.sidebar')) {
        renderSummaryCards();
    }
    
    // Listen for Bootstrap tab changes to re-apply translations
    const tabTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tab"]'))
    tabTriggerList.forEach(function (tabTrigger) {
        tabTrigger.addEventListener('shown.bs.tab', function (event) {
            // Small delay to ensure content is fully rendered
            setTimeout(() => {
                const currentLang = sessionStorage.getItem('userLanguage') || 
                                  localStorage.getItem('userLanguage') || 
                                  document.documentElement.lang || 
                                  'en';
                // Only apply language if it's different from current to prevent loop
                if (currentLang !== document.documentElement.lang) {
                    setLanguage(currentLang);
                }
            }, 50);
        });
    });
    
    // ===================================
    // IMAGE SLIDER LOGIC
    // ===================================
    const slides = document.querySelectorAll('.image-slider-container .slide');
    if (slides.length > 0) {
        let currentSlide = 0;

        const nextSlide = () => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        };

        // Set the interval for the automatic slide change (e.g., every 5 seconds)
        setInterval(nextSlide, 5000);
    }
});

// ==========================================================
// MOCK DATA & FUNCTIONS
// ==========================================================
const mockSummaryData = { pendingApplications: 2, resolvedGrievances: 5, taxesDue: 1 };

function handleLogin(event) {
    event.preventDefault();
    const userType = document.getElementById('userType').value;
    if (userType === 'citizen') {
        window.location.href = 'citizen-dashboard.html';
    } else {
        alert('Redirecting to staff/official portal...');
    }
}

function loadCitizenDashboard() {
    renderSummaryCards();
}
function renderSummaryCards() {
    const container = document.getElementById('summary-cards-container');
    if (!container) return;
    
    container.innerHTML = `
        <div class="col-md-4 mb-3">
            <div class="summary-card bg-card-blue">
                <h5 data-lang-key="summary_pending">Pending Applications</h5>
                <div class="summary-number">${mockSummaryData.pendingApplications}</div>
                <div class="summary-icon"><i class="bi bi-folder-symlink-fill"></i></div>
            </div>
        </div>
        <div class="col-md-4 mb-3">
            <div class="summary-card bg-card-green">
                <h5 data-lang-key="summary_resolved">Resolved Grievances</h5>
                <div class="summary-number">${mockSummaryData.resolvedGrievances}</div>
                <div class="summary-icon"><i class="bi bi-check-circle-fill"></i></div>
            </div>
        </div>
        <div class="col-md-4 mb-3">
            <div class="summary-card bg-card-saffron">
                <h5 data-lang-key="summary_due">Taxes Due</h5>
                <div class="summary-number">₹${mockSummaryData.taxesDue}</div>
                <div class="summary-icon"><i class="bi bi-exclamation-triangle-fill"></i></div>
            </div>
        </div>`;
    
    // Translate the newly created elements
    const currentLang = sessionStorage.getItem('userLanguage') || 
                       localStorage.getItem('userLanguage') || 
                       document.documentElement.lang || 
                       'en';
    
    // Only translate if not already in the process of setting language
    if (!window.settingLanguage) {
        // Translate the summary cards elements that have data-lang-key attributes
        container.querySelectorAll('[data-lang-key]').forEach(element => {
            const key = element.getAttribute('data-lang-key');
            if (translations[currentLang] && translations[currentLang][key]) {
                element.innerText = translations[currentLang][key];
            }
        });
    }
    
    // Also update welcome messages dynamically if user data is available
    if (window.userUsername) {
        const welcomeElements = document.querySelectorAll('[data-lang-key*="welcome"]');
        welcomeElements.forEach(element => {
            const key = element.getAttribute('data-lang-key');
            if (translations[currentLang] && translations[currentLang][key]) {
                element.innerText = interpolate(translations[currentLang][key], { username: window.userUsername });
            }
        });
    }
}