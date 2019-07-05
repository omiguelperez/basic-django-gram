"""Posts URLs."""

from django.urls import path

from posts import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='feed'),
    path('posts/new/', views.CreatePostView.as_view(), name='create'),
]
