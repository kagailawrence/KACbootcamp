from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect

def role_required(allowed_roles):
    """
    Decorator to restrict access based on user roles.
    allowed_roles: list of role strings like ['admin', 'auditor']
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect('login')

            if request.user.role not in allowed_roles:
                messages.error(request, "You don't have permission to access this page.")
                return redirect('election_list')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
