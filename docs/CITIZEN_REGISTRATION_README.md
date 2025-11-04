# Gram Panchayate System - Simplified Authentication

## Overview
This Gram Panchayate System has been simplified to remove all OTP-related functionality. The system now uses traditional username/password authentication for all user types.

## User Types and Access

### 1. Admin Access
- **Access Method**: Django superuser login
- **Login URL**: `/django-admin/` or `/auth/admin-login/`
- **Test Credentials**: 
  - Username: `admin`
  - Password: `admin123`

### 2. Clerk Access
- **Access Method**: Username and password login
- **Login URL**: `/auth/clerk-login/`
- **Test Credentials**:
  - Username: `testclerk`
  - Password: `clerk123`

### 3. Citizen Access
- **Registration**: Citizens must first register at `/auth/citizen-register/`
- **Login**: After registration, login at `/auth/citizen-login/`
- **Test Credentials**:
  - Username: `testcitizen`
  - Password: `citizen123`

## Features Implemented

1. **Simple Authentication** - Username/password login for all user types
2. **Citizen Registration** - New citizens can register with username, password, mobile number, Aadhaar, and address
3. **Role-based Access** - Different dashboards for admin, clerk, and citizen users
4. **Clean Database** - Removed all OTP-related tables and functionality

## Setup Instructions

1. **Database Migration**:
   ```bash
   cd gram_panchayate_system
   python manage.py migrate
   ```

2. **Create Test Users** (Optional):
   ```bash
   python create_test_users.py
   ```

3. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## Changes Made

### Removed Files:
- All OTP-related documentation files
- SMS configuration files
- OTP verification templates
- SMS service implementation
- OTP model from database

### Updated Files:
- `models.py`: Removed OTP model
- `views.py`: Removed OTP-related views, added simple citizen login
- `forms.py`: Removed OTP forms, added citizen login form
- `urls.py`: Updated URL patterns to remove OTP routes
- Templates: Updated login flow to use username/password

## How It Works

### Citizen Registration Flow:
1. Citizens visit `/auth/citizen-register/`
2. Fill in registration form with:
   - Username
   - Mobile number
   - Password (twice for confirmation)
   - Aadhaar number
   - Address
3. System creates user account and citizen profile
4. Redirect to login page

### Login Flow:
1. **Admin**: Login at `/auth/admin-login/` or `/django-admin/`
2. **Clerk**: Login at `/auth/clerk-login/`
3. **Citizen**: Login at `/auth/citizen-login/`

## Database Schema

The system uses these models:
- `CustomUser` - Base user with username, mobile number, user type
- `CitizenProfile` - Citizen-specific data (Aadhaar, address)
- `ClerkProfile` - Clerk-specific data (panchayat, employee ID)
- `AdminProfile` - Admin-specific data (designation, department)

## Security Notes
- All passwords are hashed using Django's built-in authentication
- Session-based authentication for all user types
- Role-based access control maintained through user types
- CSRF protection enabled for all forms
- Unique constraints on mobile numbers and Aadhaar numbers