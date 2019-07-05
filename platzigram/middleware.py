"""Platzigram middleware catalog."""

from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware:
    """Profile completion middleware.

    Ensure every user that is interacting with the platform
    have their profile picture and biography.
    """

    def __init__(self, get_response):
        """Middleware initilization."""
        self.get_response = get_response

    def __call__(self, request):
        """Code to be executed for each request before the view is called."""
        if not request.user.is_anonymous:
            profile = request.user.profile if hasattr(request.user, 'profile') else None
            if not request.user.is_staff:
                if not profile or not (profile.picture and profile.biography):
                    excluded_paths = [
                        reverse('users:logout'),
                        reverse('users:update_profile'),
                    ]
                    if request.path not in excluded_paths:
                        return redirect('users:update_profile')

        response = self.get_response(request)
        return response
