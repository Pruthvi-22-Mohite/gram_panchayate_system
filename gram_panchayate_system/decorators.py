from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect
from django.contrib import messages

def citizen_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the user is a citizen,
    redirecting to the login page if necessary.
    """
    def check_citizen(user):
        if user.is_authenticated and user.user_type == 'citizen':
            return True
        elif user.is_authenticated:
            messages.error(None, "Access denied. Citizens only.")
            return False
        else:
            messages.error(None, "Please log in to access this page.")
            return False
    
    if function:
        return user_passes_test(check_citizen, login_url=login_url)(function)
    return user_passes_test(check_citizen, login_url=login_url)

def clerk_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the user is a clerk,
    redirecting to the login page if necessary.
    """
    def check_clerk(user):
        if user.is_authenticated and user.user_type == 'clerk':
            return True
        elif user.is_authenticated:
            messages.error(None, "Access denied. Clerks only.")
            return False
        else:
            messages.error(None, "Please log in to access this page.")
            return False
    
    if function:
        return user_passes_test(check_clerk, login_url=login_url)(function)
    return user_passes_test(check_clerk, login_url=login_url)

def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the user is an admin,
    redirecting to the login page if necessary.
    """
    def check_admin(user):
        if user.is_authenticated and user.user_type == 'admin':
            return True
        elif user.is_authenticated:
            messages.error(None, "Access denied. Admins only.")
            return False
        else:
            messages.error(None, "Please log in to access this page.")
            return False
    
    if function:
        return user_passes_test(check_admin, login_url=login_url)(function)
    return user_passes_test(check_admin, login_url=login_url)