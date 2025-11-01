from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class UserRoleRedirectMiddleware:
    """
    Middleware to redirect users based on their role after login
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user just logged in (you might need to adjust this logic)
        # This is a simplified version - in production, you'd want a more robust way to detect login
        
        response = self.get_response(request)
        return response