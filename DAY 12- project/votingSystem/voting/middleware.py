from django.http import HttpResponseForbidden
from django.contrib.auth.models import AnonymousUser
from .models import Voter

class VoterAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            try:
                voter = Voter.objects.get(user=request.user)
                request.voter = voter
            except Voter.DoesNotExist:
                return HttpResponseForbidden("User is not registered as a voter.")
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
