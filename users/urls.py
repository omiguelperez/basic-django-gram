"""Users urls."""

from django.urls import path
from django.views.generic import TemplateView

from users import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('me/profile/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/<str:username>/', views.UserDetailView.as_view(), name='profile'),
]
