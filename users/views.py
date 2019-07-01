"""Users views."""

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View


class LoginView(View):
    """Login view."""

    def get(self, request, *args, **kwargs):
        """Handle GET request. Send login template."""
        return render(request, 'users/login.html')

    def post(self, request, *args, **kwargs):
        """Handle POST request. Login."""
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('posts')
        else:
            return render(request, 'users/login.html',
                          {'error': 'Invalid username and password'})
