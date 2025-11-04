#!/usr/bin/env python
"""
Migration script to update the project to use the new modular structure
"""
import os
import sys
import shutil
from pathlib import Path

def update_settings():
    """Update Django settings to include module paths"""
    settings_path = "gram_panchayate_system/settings.py"
    
    # Read current settings
    with open(settings_path, 'r') as f:
        content = f.read()
    
    # Add modules to INSTALLED_APPS if not already present
    if 'modules.admin' not in content:
        # Find INSTALLED_APPS and add modules
        installed_apps_start = content.find('INSTALLED_APPS = [')
        if installed_apps_start != -1:
            # Find the end of INSTALLED_APPS
            bracket_count = 0
            pos = installed_apps_start + len('INSTALLED_APPS = [')
            while pos < len(content):
                if content[pos] == '[':
                    bracket_count += 1
                elif content[pos] == ']':
                    if bracket_count == 0:
                        break
                    bracket_count -= 1
                pos += 1
            
            # Insert modules before the closing bracket
            modules_to_add = """    # Modular structure
    'modules.common',
    'modules.admin',
    'modules.clerk',
    'modules.citizen',
"""
            content = content[:pos] + modules_to_add + content[pos:]
    
    # Update AUTH_USER_MODEL if not already set
    if 'AUTH_USER_MODEL' not in content:
        content += "\n# Custom User Model\nAUTH_USER_MODEL = 'common.CustomUser'\n"
    
    # Write updated settings
    with open(settings_path, 'w') as f:
        f.write(content)
    
    print("✅ Updated Django settings")

def update_main_urls():
    """Update main URLs to include module URLs"""
    urls_path = "gram_panchayate_system/urls.py"
    
    # Read current URLs
    with open(urls_path, 'r') as f:
        content = f.read()
    
    # Replace old URL patterns with module URLs
    new_urlpatterns = """urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('modules.urls')),
]"""
    
    # Find and replace urlpatterns
    start = content.find('urlpatterns = [')
    if start != -1:
        # Find the end of urlpatterns
        bracket_count = 0
        pos = start + len('urlpatterns = [')
        while pos < len(content):
            if content[pos] == '[':
                bracket_count += 1
            elif content[pos] == ']':
                if bracket_count == 0:
                    pos += 1
                    break
                bracket_count -= 1
            pos += 1
        
        content = content[:start] + new_urlpatterns + content[pos:]
    
    # Write updated URLs
    with open(urls_path, 'w') as f:
        f.write(content)
    
    print("✅ Updated main URLs")

def move_templates():
    """Move existing templates to module directories"""
    template_mappings = {
        'admin_login.html': 'modules/admin/templates/admin/login.html',
        'admin_dashboard.html': 'modules/admin/templates/admin/dashboard.html',
        'clerk_login.html': 'modules/clerk/templates/clerk/login.html',
        'clerk_dashboard.html': 'modules/clerk/templates/clerk/dashboard.html',
        'citizen_login.html': 'modules/citizen/templates/citizen/login.html',
        'citizen_dashboard.html': 'modules/citizen/templates/citizen/dashboard.html',
        'citizen_registration.html': 'modules/citizen/templates/citizen/registration.html',
        'index.html': 'modules/common/templates/common/index.html',
        'login.html': 'modules/common/templates/common/login.html',
        'base.html': 'modules/common/templates/common/base.html',
    }
    
    for old_path, new_path in template_mappings.items():
        old_full_path = f"templates/{old_path}"
        if os.path.exists(old_full_path):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            # Copy file
            shutil.copy2(old_full_path, new_path)
            print(f"✅ Moved {old_path} to {new_path}")

def create_module_apps():
    """Create apps.py files for each module"""
    modules = ['admin', 'clerk', 'citizen', 'common']
    
    for module in modules:
        apps_path = f"modules/{module}/apps.py"
        
        apps_content = f"""from django.apps import AppConfig


class {module.title()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.{module}'
    verbose_name = '{module.title()} Module'
"""
        
        with open(apps_path, 'w') as f:
            f.write(apps_content)
        
        print(f"✅ Created apps.py for {module} module")

def backup_old_files():
    """Backup old files before migration"""
    backup_dir = "backup_old_structure"
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Backup important files
    files_to_backup = [
        'models.py',
        'views.py',
        'forms.py',
        'decorators.py',
        'authentication/views.py',
        'authentication/forms.py',
        'authentication/urls.py',
    ]
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            backup_path = os.path.join(backup_dir, file_path.replace('/', '_'))
            shutil.copy2(file_path, backup_path)
            print(f"✅ Backed up {file_path}")

def main():
    """Main migration function"""
    print("🚀 Starting migration to modular structure...")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: Please run this script from the Django project root directory")
        sys.exit(1)
    
    try:
        # Step 1: Backup old files
        print("\n📦 Backing up old files...")
        backup_old_files()
        
        # Step 2: Create module apps.py files
        print("\n📝 Creating module apps.py files...")
        create_module_apps()
        
        # Step 3: Update Django settings
        print("\n⚙️ Updating Django settings...")
        update_settings()
        
        # Step 4: Update main URLs
        print("\n🔗 Updating main URLs...")
        update_main_urls()
        
        # Step 5: Move templates
        print("\n📁 Moving templates to module directories...")
        move_templates()
        
        print("\n✅ Migration completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Test the application: python manage.py runserver")
        print("4. Update any remaining import statements in your code")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()