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
        return user.is_authenticated and user.user_type == 'citizen'
    
    actual_decorator = user_passes_test(
        check_citizen,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator

def clerk_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the user is a clerk,
    redirecting to the login page if necessary.
    """
    def check_clerk(user):
        return user.is_authenticated and user.user_type == 'clerk'
    
    actual_decorator = user_passes_test(
        check_clerk,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator for views that checks that the user is an admin,
    redirecting to the login page if necessary.
    """
    def check_admin(user):
        return user.is_authenticated and user.user_type == 'admin'
    
    actual_decorator = user_passes_test(
        check_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator