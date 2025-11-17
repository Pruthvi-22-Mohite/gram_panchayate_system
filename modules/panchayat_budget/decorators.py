from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse


def admin_or_clerk_required(view_func):
    """
    Decorator that checks if the user is an admin or clerk.
    Redirects to login page if not authenticated.
    Raises PermissionDenied if user is not admin or clerk.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type.upper() not in ['ADMIN', 'CLERK']:
            raise PermissionDenied("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def citizen_required(view_func):
    """
    Decorator that checks if the user is a citizen.
    Redirects to login page if not authenticated.
    Raises PermissionDenied if user is not a citizen.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type.upper() != 'CITIZEN':
            raise PermissionDenied("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    """
    Decorator that checks if the user is an admin.
    Redirects to login page if not authenticated.
    Raises PermissionDenied if user is not an admin.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type.upper() != 'ADMIN':
            raise PermissionDenied("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view