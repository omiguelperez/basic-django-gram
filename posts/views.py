"""Posts views."""

from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from posts.forms import PostForm
from posts.models import Post


class PostListView(LoginRequiredMixin, ListView):
    """Posts feed view."""

    template_name = 'posts/feed.html'
    queryset = Post.objects.all().order_by('-created')
    context_object_name = 'posts'
    paginated_by = 30


class PostDetailView(LoginRequiredMixin, DetailView):
    """Post detail view."""

    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'
    

class CreatePostView(LoginRequiredMixin, CreateView):
    """Post create view."""

    template_name = 'posts/create.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context

