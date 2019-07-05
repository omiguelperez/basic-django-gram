"""Posts views."""

from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from posts.forms import PostForm
from posts.models import Post


class PostListView(LoginRequiredMixin, ListView):
    """Posts feed view."""

    template_name = 'posts/feed.html'
    queryset = Post.objects.all().order_by('-created')
    context_object_name = 'posts'
    paginated_by = 30
    

class CreatePostView(LoginRequiredMixin,
                     View):
    """Create post view."""

    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'

    def get_context(self, request, form):
        """Get request context."""
        context = {
            'user': request.user,
            'profile': request.user.profile,
            'form': form
        }
        return context

    def get(self, request, *args, **kwargs):
        """Handle GET request. Send create post form."""
        form = PostForm()
        context = self.get_context(request, form)
        return render(request, 'posts/create.html', context=context)

    def post(self, request, *args, **kwargs):
        """Handle POST request. Create new post."""
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')
        context = self.get_context(request, form)
        return render(request, 'posts/create.html', context=context)
