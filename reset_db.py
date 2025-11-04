#!/usr/bin/env python
"""
Script to reset the database for the new modular structure
"""
import os
import sys
import django
from django.conf import settings

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gram_panchayate_system.settings')
    django.setup()
    
    from django.db import connection
    
    # Drop all tables
    with connection.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    
    print("✅ Database tables dropped successfully!")
    print("Now run:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser")