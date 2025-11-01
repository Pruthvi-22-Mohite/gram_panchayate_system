// Language translation functionality
const translations = {
    "en": {
        "main_title": "Gram Panchayat Portal",
        "subtitle": "Digital Services | Government of India",
        "login_button": "Login",
        "logout": "Logout",
        "welcome_citizen": "Welcome, Citizen!",
        "citizen_portal": "Citizen Portal",
        "clerk_portal": "Clerk Portal",
        "admin_portal": "Admin Portal",
        "sidebar_dashboard": "Dashboard",
        "sidebar_financial": "Financial Services",
        "sidebar_grievance": "Grievance Redressal",
        "sidebar_schemes": "Schemes & Subsidies",
        "sidebar_info": "Information Hub",
        "sidebar_requests": "Certificates & RTI",
        "sidebar_engagement": "Citizen Engagement",
        "sidebar_management": "Management",
        "sidebar_reports": "Reports & Analytics",
        "common_services": "Common Services",
        "recent_activity": "Recent Activity & Alerts",
        "summary_pending": "Pending Applications",
        "summary_resolved": "Resolved Grievances",
        "summary_due": "Taxes Due",
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
        "action_feedback": "Feedback & Suggestions"
    },
    "hi": {
        "main_title": "ग्राम पंचायत पोर्टल",
        "subtitle": "डिजिटल सेवाएँ | भारत सरकार",
        "login_button": "लॉगिन",
        "logout": "लॉगआउट",
        "welcome_citizen": "आपका स्वागत है, नागरिक!",
        "citizen_portal": "नागरिक पोर्टल",
        "clerk_portal": "लिपिक पोर्टल",
        "admin_portal": "व्यवस्थापक पोर्टल",
        "sidebar_dashboard": "डैशबोर्ड",
        "sidebar_financial": "वित्तीय सेवाएं",
        "sidebar_grievance": "शिकायत निवारण",
        "sidebar_schemes": "योजनाएं और सब्सिडी",
        "sidebar_info": "सूचना केंद्र",
        "sidebar_requests": "प्रमाणपत्र और आरटीआई",
        "sidebar_engagement": "नागरिक सहभागिता",
        "sidebar_management": "प्रबंधन",
        "sidebar_reports": "रिपोर्ट और विश्लेषण",
        "common_services": "सामान्य सेवाएँ",
        "recent_activity": "हाल की गतिविधि और चेतावनी",
        "summary_pending": "लंबित आवेदन",
        "summary_resolved": "निवारण की गई शिकायतें",
        "summary_due": "देय कर",
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
        "action_feedback": "प्रतिक्रिया और सुझाव"
    },
    "mr": {
        "main_title": "ग्रामपंचायत पोर्टल",
        "subtitle": "डिजिटल सेवा | भारत सरकार",
        "login_button": "लॉगिन",
        "logout": "लॉगआउट",
        "welcome_citizen": "स्वागत आहे, नागरिक!",
        "citizen_portal": "नागरिक पोर्टल",
        "clerk_portal": "क्लर्क पोर्टल",
        "admin_portal": "प्रशासक पोर्टल",
        "sidebar_dashboard": "डॅशबोर्ड",
        "sidebar_financial": "आर्थिक सेवा",
        "sidebar_grievance": "तक्रार निवारण",
        "sidebar_schemes": "योजना आणि अनुदान",
        "sidebar_info": "माहिती केंद्र",
        "sidebar_requests": "प्रमाणपत्रे आणि माहितीचा अधिकार",
        "sidebar_engagement": "नागरिक सहभाग",
        "sidebar_management": "व्यवस्थापन",
        "sidebar_reports": "अहवाल आणि विश्लेषण",
        "common_services": "सामान्य सेवा",
        "recent_activity": "अलीकडील क्रियाकलाप आणि सूचना",
        "summary_pending": "प्रलंबित अर्ज",
        "summary_resolved": "निवारण झालेल्या तक्रारी",
        "summary_due": "देय कर",
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
        "action_feedback": "अभिप्राय आणि सूचना"
    }
};

// Set language function
const setLanguage = (lang) => {
    document.querySelectorAll('[data-lang-key]').forEach(element => {
        const key = element.getAttribute('data-lang-key');
        if (translations[lang] && translations[lang][key]) {
            element.innerText = translations[lang][key];
        }
    });
    localStorage.setItem('userLanguage', lang);
    const langSwitcher = document.getElementById('language-switcher');
    if (langSwitcher) langSwitcher.value = lang;
};

// Initialize language on page load
document.addEventListener('DOMContentLoaded', function() {
    const savedLang = localStorage.getItem('userLanguage') || 'en';
    setLanguage(savedLang);
    
    const langSwitcher = document.getElementById('language-switcher');
    if (langSwitcher) {
        langSwitcher.value = savedLang;
        langSwitcher.addEventListener('change', function() {
            setLanguage(this.value);
        });
    }
});

// Image slider functionality
document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    if (slides.length > 0) {
        let currentSlide = 0;
        
        const showSlide = (index) => {
            slides.forEach((slide, i) => {
                slide.classList.toggle('active', i === index);
            });
        };
        
        const nextSlide = () => {
            currentSlide = (currentSlide + 1) % slides.length;
            showSlide(currentSlide);
        };
        
        // Show first slide
        showSlide(currentSlide);
        
        // Change slide every 5 seconds
        setInterval(nextSlide, 5000);
    }
});

// Chatbot functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatbotToggle = document.querySelector('.chatbot-toggle');
    const chatbotWindow = document.querySelector('.chatbot-window');
    const chatbotInput = document.querySelector('.chatbot-input input');
    const chatbotSend = document.querySelector('.chatbot-input button');
    const chatbotMessages = document.querySelector('.chatbot-messages');
    
    if (chatbotToggle && chatbotWindow) {
        chatbotToggle.addEventListener('click', function() {
            chatbotWindow.classList.toggle('active');
        });
        
        const addMessage = (message, isUser = false) => {
            const messageElement = document.createElement('div');
            messageElement.classList.add('chatbot-message');
            messageElement.classList.add(isUser ? 'user' : 'bot');
            messageElement.textContent = message;
            chatbotMessages.appendChild(messageElement);
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        };
        
        const respondToUser = (message) => {
            // Simple responses for demo purposes
            const responses = [
                "Thank you for your message. Our team will get back to you shortly.",
                "For more information, please visit the citizen services section.",
                "You can track your grievances in the 'Track My Grievances' section.",
                "For urgent matters, please contact the emergency helpline.",
                "I've noted your query. A representative will contact you soon."
            ];
            
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            setTimeout(() => {
                addMessage(randomResponse);
            }, 1000);
        };
        
        const sendMessage = () => {
            const message = chatbotInput.value.trim();
            if (message) {
                addMessage(message, true);
                chatbotInput.value = '';
                respondToUser(message);
            }
        };
        
        chatbotSend.addEventListener('click', sendMessage);
        
        chatbotInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Initial bot message
        setTimeout(() => {
            addMessage("Hello! How can I assist you today?");
        }, 1000);
    }
});

// Handle login form submission
function handleLogin(event) {
    event.preventDefault();
    // In a real application, this would send the data to the server
    alert("Login functionality would be implemented in the backend.");
}

// Handle form submissions
function handleFormSubmit(event, formName) {
    event.preventDefault();
    // In a real application, this would send the data to the server
    alert(formName + " form submitted successfully!");
}