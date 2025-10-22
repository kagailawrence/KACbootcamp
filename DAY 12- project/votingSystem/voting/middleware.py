from django.http import HttpResponseForbidden
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import redirect
from datetime import timedelta
from .models import Voter

class VoterAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            # Only enforce voter registration for users with 'voter' role
            if request.user.role == 'voter':
                try:
                    voter = Voter.objects.get(user=request.user)
                    request.voter = voter
                except Voter.DoesNotExist:
                    return HttpResponseForbidden("User is not registered as a voter.")
            else:
                # For admin and auditor roles, set voter to None
                request.voter = None
        return self.get_response(request)

class SessionSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check session expiry (10 minutes of inactivity)
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity_time = timezone.datetime.fromisoformat(last_activity)
                if timezone.now() - last_activity_time > timedelta(minutes=10):
                    from django.contrib.auth import logout
                    logout(request)
                    return redirect('login')

            # Update last activity
            request.session['last_activity'] = timezone.now().isoformat()

            # Bind session to IP and user-agent
            client_ip = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            stored_ip = request.session.get('client_ip')
            stored_user_agent = request.session.get('user_agent')

            if stored_ip and stored_ip != client_ip:
                from django.contrib.auth import logout
                logout(request)
                return redirect('login')

            if stored_user_agent and stored_user_agent != user_agent:
                from django.contrib.auth import logout
                logout(request)
                return redirect('login')

            # Store IP and user-agent for future requests
            request.session['client_ip'] = client_ip
            request.session['user_agent'] = user_agent

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define role-based access patterns
        role_restrictions = {
            'admin': ['/admin/', '/create-election/', '/manage/', '/results/', '/dashboard/admin/'],
            'auditor': ['/results/', '/dashboard/auditor/', '/auditor/'],
            'voter': ['/election/', '/vote/', '/register/', '/dashboard/voter/', '/voter/'],
        }

        # Allow access to auth pages for all users (authenticated and unauthenticated)
        auth_paths = ['/login/', '/signup/', '/logout/', '/accounts/login/', '/accounts/logout/']
        if any(auth_path in request.path for auth_path in auth_paths):
            return self.get_response(request)

        if request.user.is_authenticated:
            user_role = request.user.role
            path = request.path

            # Check if user has access to the requested path
            allowed = False
            if user_role in role_restrictions:
                for allowed_path in role_restrictions[user_role]:
                    if allowed_path in path:
                        allowed = True
                        break

            # Allow access to general pages for all authenticated users
            if not allowed and any(general_path in path for general_path in ['/', '/election_list', '/logout']):
                allowed = True

            if not allowed:
                from django.contrib import messages
                messages.error(request, "You don't have permission to access this page.")
                return redirect('election_list')

        return self.get_response(request)

class BallotSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add security headers
        response = self.get_response(request)
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response
