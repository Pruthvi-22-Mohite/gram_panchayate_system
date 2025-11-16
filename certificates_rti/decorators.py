from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def citizen_required(view_func):
    """Decorator to restrict access to citizens only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to access this page.")
            return redirect('/login/')
        
        if request.user.user_type != 'citizen':
            messages.error(request, "Access denied. This page is for citizens only.")
            return redirect('/')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def clerk_required(view_func):
    """Decorator to restrict access to clerks only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to access this page.")
            return redirect('/login/')
        
        if request.user.user_type != 'clerk':
            messages.error(request, "Access denied. This page is for clerks only.")
            return redirect('/')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator to restrict access to admins only"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to access this page.")
            return redirect('/login/')
        
        if not (request.user.user_type == 'admin' or request.user.is_superuser):
            messages.error(request, "Access denied. This page is for administrators only.")
            return redirect('/')
        
        return view_func(request, *args, **kwargs)
    return wrapper
