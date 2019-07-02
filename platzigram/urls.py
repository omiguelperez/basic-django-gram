"""Platzigram URLs."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from platzigram import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello-world/', views.hello_world, name='hello_world'),
    path('sort-numbers/', views.sort_numbers, name='sort'),
    path('hi/<name>/<int:age>/', views.say_hi, name='hi'),

    path('posts/', include('posts.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
