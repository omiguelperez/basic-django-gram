"""Users views."""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.utils import IntegrityError
from django.views import View
from django.views.generic import DetailView

from posts.models import Post
from users.forms import ProfileForm, SignupForm
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
            return redirect('posts:feed')
        else:
            return render(request, 'users/login.html',
                          {'error': 'Invalid username and password'})


class UserDetailView(LoginRequiredMixin, DetailView):
    """User's detail view."""

    template_name = 'users/detail.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    
    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context


class SignupView(View):
    """Signup view."""

    def get(self, request, *args, **kwargs):
        """Handle GET request. Send signup template."""
        form = SignupForm()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """Handle POST request. Create user."""
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('users:login')

        return render(request, 'users/signup.html', {'form': form})


@login_required(login_url=reverse_lazy('login'),
                redirect_field_name='redirect_to')
def logout_view(request):
    """Logout user."""
    logout(request)
    return redirect('users:login')


class UpdateProfileView(View):
    """Update profile view."""

    def get_context(self, request, form):
        """Get form context."""
        context = {
            'user': request.user,
            'profile': request.user.profile,
            'form': form
        }
        return context

    def get(self, request, *args, **kwargs):
        """Handle GET request. Send update profile template."""
        form = ProfileForm()
        context = self.get_context(request, form)
        return render(request, 'users/update_profile.html', context=context)

    def post(self, request, *args, **kwargs):
        """Handle POST request. Update user profile."""
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            profile = request.user.profile

            profile.website = data['website']
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            profile.picture = data['picture']
            profile.save()

            return redirect('users:update_profile')
        context = self.get_context(request, form)
        return render(request, 'users/update_profile.html', context=context)
