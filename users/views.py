"""Users views."""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.utils import IntegrityError
from django.views import View

from users.models import Profile


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


class SignupView(View):
    """Signup view."""

    def get(self, request, *args, **kwargs):
        """Handle GET request. Send signup template."""
        return render(request, 'users/signup.html')

    def post(self, request, *args, **kwargs):
        """Handle POST request. Create user."""
        username = request.POST['username']
        passwd = request.POST['passwd']
        passwd_confirmation = request.POST['passwd_confirmation']

        if passwd != passwd_confirmation:
            return render(
                request, 'users/signup.html',
                {'error': 'Password confirmation does not match'})

        try:
            user = User.objects.create_user(username=username, password=passwd)
        except IntegrityError:
            return render(request, 'users/signup.html',
                          {'error': 'Username is already in use'})

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        profile = Profile(user=user)
        profile.save()

        return redirect('login')


@login_required(login_url=reverse_lazy('login'),
                redirect_field_name='redirect_to')
def logout_view(request):
    """Logout user."""
    logout(request)
    return redirect('login')


class UpdateProfileView(View):
    """Update profile view."""

    def get(self, request, *args, **kwargs):
        """Handle GET request. Send update profile template."""
        return render(request, 'users/update_profile.html')
