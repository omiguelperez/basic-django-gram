"""Users views."""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView, UpdateView

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


class SignupView(FormView):
    """Signup view."""

    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


@login_required(login_url=reverse_lazy('login'),
                redirect_field_name='redirect_to')
def logout_view(request):
    """Logout user."""
    logout(request)
    return redirect('users:login')


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = 'users/update_profile.html'
    fields = ('picture', 'website', 'biography', 'phone_number')
    model = Profile
    
    def get_object(self):
        """Return user's profile."""
        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile."""
        return reverse('users:profile', kwargs={'username': self.request.user.username})

