from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def user_type_required(user_type):
    """
    Decorator to check if user has the required user type
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.user_type == user_type:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, f"Access denied. {user_type.title()} access required.")
                return redirect('home')
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """
    Decorator to require superuser access for admin functions
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Admin access denied. Superuser privileges required.")
            return redirect('common:home')
    return _wrapped_view


def clerk_required(view_func):
    """
    Decorator to require clerk user type
    """
    return user_type_required('clerk')(view_func)


def citizen_required(view_func):
    """
    Decorator to require citizen user type
    """
    return user_type_required('citizen')(view_func)


def superuser_required(view_func):
    """
    Decorator to require superuser access
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Superuser access required.")
            return redirect('home')
    return _wrapped_view