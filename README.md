# Gram Panchayate System

A comprehensive digital platform for Gram Panchayat administration and citizen services.

## 🏗️ Project Structure

```
gram_panchayate_system/
├── 📁 docs/                           # Project documentation
│   ├── MODULAR_STRUCTURE_README.md    # Architecture documentation
│   ├── SYSTEM_READY.md               # Quick start guide
│   └── CITIZEN_REGISTRATION_README.md # Registration guide
├── 📁 gram_panchayate_system/         # Django project settings
│   ├── settings.py                   # Project configuration
│   ├── urls.py                       # Main URL routing
│   └── wsgi.py                       # WSGI configuration
├── 📁 modules/                        # Modular application structure
│   ├── 📁 admin/                     # Admin module
│   │   ├── models.py                 # Admin models
│   │   ├── views.py                  # Admin views
│   │   ├── forms.py                  # Admin forms
│   │   ├── urls.py                   # Admin URLs
│   │   └── templates/admin/          # Admin templates
│   ├── 📁 clerk/                     # Clerk module
│   │   ├── models.py                 # Clerk models
│   │   ├── views.py                  # Clerk views
│   │   ├── forms.py                  # Clerk forms
│   │   ├── urls.py                   # Clerk URLs
│   │   └── templates/clerk/          # Clerk templates
│   ├── 📁 citizen/                   # Citizen module
│   │   ├── models.py                 # Citizen models
│   │   ├── views.py                  # Citizen views
│   │   ├── forms.py                  # Citizen forms
│   │   ├── urls.py                   # Citizen URLs
│   │   └── templates/citizen/        # Citizen templates
│   └── 📁 common/                    # Shared functionality
│       ├── models.py                 # Base models
│       ├── views.py                  # Common views
│       ├── decorators.py             # Auth decorators
│       ├── urls.py                   # Common URLs
│       └── templates/common/         # Shared templates
├── 📁 scripts/                       # Utility scripts
│   └── migrate_to_modular.py         # Migration script
├── 📁 static/                        # Static files (CSS, JS, images)
├── 📁 templates/                     # Legacy templates (to be moved)
└── manage.py                         # Django management script
```

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install django mysqlclient
   ```

2. **Database Setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## 👥 User Types

### 🔧 Admin
- **Access**: Django admin panel or custom admin interface
- **Features**: User management, system settings, audit logs, reports

### 📋 Clerk
- **Access**: Clerk login portal
- **Features**: Scheme management, application processing, grievance handling

### 👤 Citizen
- **Access**: Citizen portal
- **Features**: Scheme applications, grievance lodging, tax payments, document management

## 🔗 Key URLs

- **Home**: `/`
- **Admin**: `/admin/`
- **Clerk**: `/clerk/`
- **Citizen**: `/citizen/`

## 📚 Documentation

For detailed information, see the `docs/` directory:
- [Modular Structure Guide](docs/MODULAR_STRUCTURE_README.md)
- [System Ready Guide](docs/SYSTEM_READY.md)
- [Citizen Registration Guide](docs/CITIZEN_REGISTRATION_README.md)

## 🛠️ Development

This project uses a modular architecture where each user type (Admin, Clerk, Citizen) has its own dedicated module. This structure provides:

- **Separation of Concerns**: Each module handles its specific domain
- **Scalability**: Easy to add features or convert to Django apps
- **Maintainability**: Clear organization and isolated changes
- **Team Collaboration**: Different teams can work on different modules

## 📄 License

This project is developed for Gram Panchayat administration and citizen services.