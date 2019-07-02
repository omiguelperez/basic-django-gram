"""Posts URLs."""

from django.urls import path

from posts import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='posts'),
    path('new/', views.CreatePostView.as_view(), name='create_post'),
]
